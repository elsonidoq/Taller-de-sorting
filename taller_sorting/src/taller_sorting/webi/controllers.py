from __future__ import with_statement
from collections import defaultdict
import json
import random
from mako.template import Template
from mako.lookup import TemplateLookup
import os
import cherrypy

here= os.path.dirname(os.path.abspath(__file__))
lookup= TemplateLookup(os.path.join(here, 'templates'), disable_unicode=True, input_encoding='utf-8')

from taller_sorting.list_algorithms import find_sorting_algorithms
from taller_sorting.list import List

class Root(object):
    @cherrypy.expose
    def index(self):
        template= lookup.get_template('index.mako')
        all_algorithms= set()
        algorithms_per_group= {}
        for group_name, group_algorithms in find_sorting_algorithms().items():
            all_algorithms.update(x[0] for x in group_algorithms)
            algorithms_per_group[group_name]= [x[0] for x in group_algorithms]
        return template.render(all_algorithms=all_algorithms, algorithms_per_group=algorithms_per_group) #['merge_sort'])

    @cherrypy.expose
    def get_implementations(self, algorithm, order, size, custom_algorithms):
        l= range(1, int(size)+1)
        if order == 'asc':
            pass
        elif order == 'desc':
            l.sort(reverse=True)
        elif order == 'random':
            random.shuffle(l)
        elif order == 'almost-sorted':
            for i in xrange(len(l)):
                if random.random() < 0.2:
                    idx= random.randint(0, len(l)-1)
                    l[i], l[idx]= l[idx], l[i]

        l= [[i] for i in l]
        
        algorithms= find_sorting_algorithms()

        if algorithm == 'custom':
            custom_algorithms= self._parse_custom_algoritms(custom_algorithms)

        groups= []
        for group_name, group_algorithms in sorted(algorithms.iteritems(),key=lambda x:x[0]):
            for alg_name, impl in sorted(group_algorithms, key=lambda x:x[0]):
                if algorithm == 'custom':
                    if alg_name in custom_algorithms[group_name]:
                        groups.append("%s/%s" % (group_name, alg_name))
                elif alg_name == algorithm:
                    groups.append(group_name)

        cherrypy.response.headers['Content-Type']= 'application/json'
        return json.dumps([l, groups])
    
    def _parse_custom_algoritms(self, custom_algorithms):
        res= defaultdict(list)
        custom_algorithms= custom_algorithms.split(',')
        for custom_algorithm in custom_algorithms:
            group, algorithm_name= custom_algorithm.split('/')
            res[group].append(algorithm_name)
        return res            

    @cherrypy.expose
    def start_sorting(self, order, size, algorithm, custom_algorithms=None):
        orig_l= range(1,int(size)+1)
        if order == 'asc':
            pass
        elif order == 'desc':
            orig_l.sort(reverse=True)
        elif order == 'random':
            random.shuffle(orig_l)
        elif order == 'almost-sorted':
            for i in xrange(len(orig_l)):
                if random.random() < 0.2:
                    idx= random.randint(0, len(orig_l)-1)
                    orig_l[i], orig_l[idx]= orig_l[idx], orig_l[i]
        
        algorithms= find_sorting_algorithms()
        
        if algorithm == 'custom':
            custom_algorithms= self._parse_custom_algoritms(custom_algorithms)

        groups= []
        for group_name, group_algorithms in algorithms.iteritems():
            for alg_name, impl in group_algorithms:
                if algorithm == 'custom':
                    if alg_name in custom_algorithms[group_name]:
                        groups.append(("%s/%s" % (group_name, alg_name), impl, List.from_list(orig_l)))
                elif alg_name == algorithm:
                    groups.append((group_name, impl, List.from_list(orig_l)))
        
        for group_name, impl, l in groups:
            try: 
                impl(l)
            except: 
                l.history.append('crash')
                
        
        group_names= []
        group_updates= []
        for group_name, impl, l in groups:
            updates= []
            for h in l.history:
                if isinstance(h, tuple):
                    if h[0] == 'read':
                        color= '#000'
                        value= None
                    else:
                        color= '#F00'
                        value= h[2]
                    updates.append([h[1], color, value])
                else:                    
                    updates.append([h])

            group_updates.append(updates)
            group_names.append(group_name)

        cherrypy.response.headers['Content-Type']= 'application/json'
        return json.dumps([ [[i] for i in orig_l], group_names, group_updates])
                    

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Set up site-wide config first so we get a log if errors occur.
    cherrypy.config.update({'environment': 'production',
                            'log.error_file': 'site.log',
                            'server.socket_port': 8080,
                            'log.screen': True })

    conf_fname= os.path.join(current_dir, 'cherrypy.ini')
    root= Root()
    cherrypy.quickstart(root, '/', config=conf_fname)

if __name__ == '__main__':    
    main()
