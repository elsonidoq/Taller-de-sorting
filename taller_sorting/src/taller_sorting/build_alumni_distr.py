import os
from itertools import chain
import sys
import shutil

algs1= dict(selection_sort=0, 
            insertion_sort=0)
algs2= dict(heapsort=0,
            mergesort=0,
            quicksort=0)

here= os.path.dirname(os.path.abspath(__file__))

def main():
    n= int(sys.argv[1])

    dir= 'alumni_distrs'
    if os.path.exists(dir): shutil.rmtree(dir)
    for i in xrange(1, n+1):
        make_one_copy(dir, 'grupo_%s' % i)
    
    for k, v in chain(algs1.items(), algs2.items()):
        print k, v
    

def make_one_copy(dir, group_name):
    dst= os.path.join(dir, group_name)
    os.makedirs(dst)
    fnames= 'list.py list_algorithms.py test.py'.split()
    
    for fname in fnames:
        shutil.copy(os.path.join(here,fname), dst)

    global algs1, algs2
    alg1= sorted(algs1.items(), key=lambda x:x[1])[0][0]
    algs1[alg1]+=1

    alg2= sorted(algs2.items(), key=lambda x:x[1])[0][0]
    algs2[alg2]+=1

    with open(os.path.join(dst, 'algorithms.py'), 'w') as f:
        f.write(algorithms_template % locals())

algorithms_template= """from list_algorithms import presentar
import random
grupo= '%(group_name)s'

@presentar
def %(alg1)s(a):
    return a

@presentar
def %(alg2)s(a):
    return a
"""
if __name__ == '__main__':
    main()
