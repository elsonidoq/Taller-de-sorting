from list_algorithms import presentar
import random
grupo= 'grupo_Y'

@presentar
def insertion_sort(a):
    swap_test = False
    for i in range ( 0, len ( a ) - 1 ):
        for j in range ( 0, len ( a ) - i - 1 ):
            if a[j] > a[j + 1] :
                a[j], a[j + 1] = a[j + 1], a[j] #elegentan way of swap
                swap_test = True
            if swap_test == False:
                break
    return a

@presentar
def mergesort(a):
    return a

