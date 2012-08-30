import sys
from math import log
from random import shuffle
from itertools import chain
import optparse

from list_algorithms import find_sorting_algorithms
from list import List

def main():
    parser = optparse.OptionParser("usage: %prog algoritmo [options]")
    parser.prog= __file__

    parser.add_option('-l', '--listita', dest='listita', default=False, action='store_true', help='ejecuta tu algoritmo con una lista chiquita')
    parser.add_option('-L', '--listota', dest='listota', default=False, action='store_true', help='ejecuta tu algoritmo con una lista grandota')
    parser.add_option('-g', '--grupo', dest='group_name', help='En caso de ambiguedad, el nombre del grupo')
    parser.add_option('-e', '--estimar-constantes', default=False, action='store_true', dest='estimate_constants', help='Si tu algoritmo es n*log(n) o n^2, trata de estimar la constante')
    parser.add_option('-t', '--todos', default=False, action='store_true', dest='all', help='Prueba todos los algoritmos')

    available_algorithms= find_sorting_algorithms()

    options, args = parser.parse_args(sys.argv[1:])

    selected_sorting_algorithms= []
    if len(args) > 0: selected_algorithm= args[0]

    for group_name, algorithms in available_algorithms.iteritems():
        if options.group_name is not None and options.group_name != group_name: continue
        for name, sorting_algorithm in algorithms:
            if options.all or name == selected_algorithm:
                selected_sorting_algorithms.append((group_name, name, sorting_algorithm))

    matches= len(selected_sorting_algorithms)
    fail= matches == 0 or (matches > 1 and not options.all)

    if matches == 0:
        print
        print "Falta el nombre del algoritmo (o pifiaste escribiendo)!"
    elif matches > 1 and not options.all:            
        print
        print "Hay muchos grupos con ese algoritmo, usa -g"
        print "Si queres probar todos los algoritmos proba con -a"

    if fail:
        print "Estan definidos estos:\n"
        for group_name, algorithms in available_algorithms.iteritems():
            print "\tGrupo: %s" % group_name
            for name, sorting_algorithm in algorithms:
                print "\t\t%s" % name
        print 
        parser.print_help()
        return

    if not any([options.listita, options.listota, options.estimate_constants]):
        parser.error("te falta elegir la opcion (-l, -L, -e)!")
        parser.print_help()

    print_result= len(selected_sorting_algorithms) == 1
    for group_name, name, selected_sorting_algorithm in selected_sorting_algorithms:

        if options.listita:
            l= range(10); shuffle(l)
            l= List(l)
            succesfull= apply(l, selected_sorting_algorithm, print_result=print_result)
        
        elif options.listota:
            l= range(5000); shuffle(l)
            l= List(l)
            succesfull= apply(l, selected_sorting_algorithm, print_result=print_result)

        elif options.estimate_constants:
            print
            print "Bueno, parece que tu algoritmo es O(%s) con constante %.02f" % estimate_constants(selected_sorting_algorithm)
            print

        if (options.listota or options.listita) and not print_result:
            print group_name, name, succesfull

def apply(l, sorting_algorithm, print_result=True):
    shuffle(l)
    orig_l= l[:]
    solution= sorted(orig_l)
    try:
        l= sorting_algorithm(l)
    except Exception,e:
        if print_result:
            print e
        return False

    if not isinstance(l, List): return False
    if l == solution:
        if print_result: print "Anduvo! =D"
        return True
    elif len(l) < 20:
        if print_result:
            print "nop, algo fallo"
            print "la lista original era: %s" % orig_l
            print "tu algoritmo la dejo asi: %s" % l
        return False
    else:
        if print_result:
            print "no anduvo =("
            print "la lista es muy grande, si queres ver que paso, podes probar con -l"
        return False


def estimate_constants(sorting_algorithm):
    candidates= [('n^2', lambda x:x**2), ('n*log(n)', lambda x:x*log(x,2))]

    dots= generate_dots(sorting_algorithm)
    results= []
    for name, candidate in candidates:
        constants= []
        for x,y in dots:
            c= float(y)/candidate(x)
            constants.append(c)
        avg= sum(constants)/len(constants)

        error= sum(abs(avg*candidate(x)-y) for x,y in dots)
        results.append((name, avg, error))

    best= min(results, key=lambda x:x[2])
    return best[0], best[1]



def generate_dots(sorting_algorithm):
    res= []
    print "Ejecutando el algoritmo..."
    for i in xrange(50, 300, 10):
        l = range(i)
        shuffle(l)
        l= List.from_list(l) 
        sorting_algorithm(l)

        res.append((i, l.counter.cnt))

    return res
        

if __name__ == '__main__':
    main()
