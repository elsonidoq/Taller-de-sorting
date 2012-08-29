import os
def main():

    here= os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, 'cherrypy_template.ini')) as f:
        content= f.read()

    with open(os.path.join(here, 'cherrypy.ini'), 'w') as f:
        f.write(content % locals())


