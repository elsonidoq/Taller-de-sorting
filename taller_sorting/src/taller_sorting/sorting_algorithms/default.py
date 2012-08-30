from taller_sorting.list_algorithms import presentar
from random import randint
grupo= 'grupo_00'

@presentar
def heapsort(lista):
    heapify(lista)
    end= len(lista)-1
    while end > 0:
        lista[end], lista[0]= lista[0], lista[end]
        shiftDown(lista, 0, end-1)
        end-=1
    return lista        

def heapify(lista):
    start= len(lista)/2
    while start>=0:
        shiftDown(lista, start, len(lista)-1)
        start-=1

def shiftDown(lista, start, end):
    root= start
    l_root= lista[root]
    while 2*root <= end:
        child= root*2
        l_child= lista[child]
        if child < end and l_child < lista[child+1]:
            child+=1
            l_child= lista[child]
        if l_root < l_child:
            lista[root], lista[child]= l_child, l_root
            root= child
        else:
            return

def shiftDown_old(lista, start, end):
    root= start
    while 2*root <= end:
        child= root*2
        if child < end and lista[child] < lista[child+1]:
            child+=1
        if lista[root] < lista[child]:
            lista[root], lista[child]= lista[child], lista[root]
            root= child
        else:
            return



@presentar
def quicksort(lista):
    return _quick_sort(lista, 0, len(lista), lambda l, start, end: end-1)


def _quick_sort(lista, start, end, pivot_func):
    if end - start <= 1: return lista
    else:
        pivotIndex= pivot_func(lista, start, end)
        pivot= lista[pivotIndex]
        lista[end-1], lista[pivotIndex]= pivot, lista[end-1]

        storeIndex= start
        for i in xrange(start, end-1):
            if lista[i] <= pivot:
                lista[i], lista[storeIndex]= lista[storeIndex], lista[i]
                storeIndex+=1
        
        lista[storeIndex], lista[end-1]= lista[end-1], lista[storeIndex]
        _quick_sort(lista, start, storeIndex, pivot_func)
        _quick_sort(lista, storeIndex, end, pivot_func)
        return lista
         

@presentar
def insertion_sort(lista):
    for i in xrange(1, len(lista)):
        e= lista[i]
        for j in xrange(i):
            if lista[j] > e:
                for k in xrange(i-1, j-1,-1):
                    lista[k+1]= lista[k]
                lista[j]= e
                e= lista[i]
    return lista        

@presentar
def mergesort(lista):
    _merge_sort_mejor(lista, lista.crear_temporal(), 0, len(lista))
    return lista

def _merge_sort_mejor(lista, tmp, start_index, end_index):
    if end_index - start_index <= 1:
        return 
    else:
        end_m1= start_index + (end_index - start_index)/2
        _merge_sort_mejor(lista, tmp, start_index, end_m1)
        _merge_sort_mejor(lista, tmp, end_m1, end_index)
        #import ipdb;ipdb.set_trace()

        i1= start_index
        i2= end_m1
        i= start_index
        #e1= lista[i1]
        #e2= lista[i2]
        while i1 < end_m1 and i2 < end_index:
            if lista[i1] < lista[i2]:
                tmp[i]= lista[i1]
                i1+=1
                #if i1 < end_m1: e1= lista[i1]
            else:
                tmp[i]= lista[i2]
                i2+=1
                #if i2 < end_index: e2= lista[i2]
            i+=1
        
        index= end_m= None
        if i1 < end_m1:
            index= i1
            end_m= end_m1
        if i2 < end_index:
            index= i2
            end_m= end_index
        
        if index is not None:
            for j in xrange(index, end_m):
                tmp[i]= lista[j]
                i+=1
        
        for i in xrange(start_index, end_index):
            lista[i]= tmp[i]
        return 
           
           

#@presentar
#def mergesort(lista):
#    if len(lista) <= 1:
#        return lista
#    else:
#        m1= mergesort(lista[:len(lista)/2])
#        m2= mergesort(lista[len(lista)/2:])
#
#        i1= i2= 0
#        i= 0
#        while i1 < len(m1) and i2 < len(m2):
#            if m1[i1] < m2[i2]:
#                lista[i]= m1[i1]
#                i1+=1
#            else:
#                lista[i]= m2[i2]
#                i2+=1
#            i+=1
#        
#        
#        index= m= None
#        if i1 < len(m1):
#            index= i1
#            m= m1
#        if i2 < len(m2):
#            index= i2
#            m= m2
#        
#        if index is not None:
#            for j in xrange(index, len(m)):
#                lista[i]= m[j]
#                i+=1
#
#        return lista
