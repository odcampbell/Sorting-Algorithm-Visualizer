import pygame

# This module holds the sorting algorthms implemented

pygame.init()

#take in a DrawingInfo object, a draw_manager object, and boolean
def bubble_sort(draw_info, manager, ascending = True):
    lst = draw_info.lst #updated list
    dm = manager #functions

    for i in range(len(lst)- 1):
        for j in range(len(lst) - 1 - i):
            bar1 = lst[j] #bars
            bar2 = lst[j + 1]

            if (bar1.sort_val > bar2.sort_val and ascending ) or (bar1.sort_val < bar2.sort_val and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j] #swaps
                dm.draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True #allows for program to respond to other keys during sorting process
    
    return lst

def insertion_sort(draw_info, manager, ascending=True):
    lst = draw_info.lst #updated list
    dm = manager #functions

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1].sort_val > current.sort_val and ascending
            descending_sort = i > 0 and lst[i - 1].sort_val < current.sort_val and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            dm.draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def selection_sort(draw_info, manager, ascending=True):
    lst = draw_info.lst
    dm = manager

    num_vals = range(0, len(lst)-1)

    for i in num_vals:
        best_value = i
        for j in range(i+1, len(lst)):
            ascending_sort = lst[j].sort_val < lst[best_value].sort_val and ascending
            descending_sort = lst[j].sort_val > lst[best_value].sort_val and not ascending

            if ascending_sort: #"angled brackets not allowed in youtube description"
                best_value = j
            elif descending_sort:
                best_value = j

        if best_value != i:
            lst[best_value], lst[i] = lst[i], lst[best_value]
            dm.draw_list(draw_info, {best_value: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

# makes a max or min heap out of given index
# takes in draw_info isntead of a list because of
# the need for information from the class
def heapify(draw_info, list_size, index, manager, ascending):
    dm = manager
    lst = draw_info.lst
    left = 2*index+1
    right = 2*index+2
    max = index
    #if left chld is in scope and greater than parent
    if left < list_size and  lst[left].sort_val > lst[max].sort_val and ascending:
        max = left
    elif left < list_size and  lst[left].sort_val < lst[max].sort_val and not ascending:
        max = left

    #if right chld is in scope and greater than parent
    if right < list_size and  lst[right].sort_val > lst[max].sort_val and ascending:
        max = right
    elif right < list_size and  lst[right].sort_val < lst[max].sort_val and not ascending:
        max = right

    if(max!=index):
        lst[(index)], lst[(max)] = lst[(max)], lst[(index)] #defined in algorithm!!
        lst[(index)].x = draw_info.start_x + index * draw_info.bar_width 
        lst[(max)].x = draw_info.start_x + max * draw_info.bar_width  
        #dm.draw_list(draw_info, {index : draw_info.GREEN, max: draw_info.RED}, True)
        heapify(draw_info, list_size,max,dm,ascending)

    #return lst #necessarry?


def heap_sort(draw_info, manager, ascending=True):
    dm = manager
    list_size = len(draw_info.lst)

    for i in range(list_size//2-1, -1, -1): #FIXME how to count down in python, whiel?
        heapify(draw_info,list_size, i, dm, ascending)

    for i in range(list_size-1,0,-1):
        draw_info.lst[i],  draw_info.lst[0] =  draw_info.lst[0],  draw_info.lst[i]
        dm.draw_list(draw_info, {i : draw_info.GREEN, 0: draw_info.RED}, True)
        heapify(draw_info,i, 0,dm, ascending)
        yield True
    
    return draw_info.lst

# made so I didnt have to type draw_info.lst[] every time
# actually performs the sort
#implementation adapted from: https://stackoverflow.com/questions/62993954/how-do-i-make-this-merge-sort-function-a-generator-python

 #def merge_sort(draw_info, manager, ascending=True, sort_list = None):
def merge_sort(draw_info, manager, ascending=True):
    # arr is a unique list that all levels in the recursion tree can access:
    arr = draw_info.lst
    def mergeSortRec(start, end):  # separate function that can take start/end indices
        if end - start > 1:
            middle = (start + end) // 2

            yield from mergeSortRec(start, middle)  # don't provide slice, but index range
            manager.draw_list(draw_info, {start : draw_info.GREEN, end: draw_info.RED}, True)  
            yield from mergeSortRec(middle, end)
            manager.draw_list(draw_info, {start : draw_info.GREEN, end: draw_info.RED}, True) 

            left = arr[start:middle]
            right  = arr[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a].sort_val < right[b].sort_val:
                    arr[c] = left[a]
                    a += 1
                else:
                    arr[c] = right[b]
                    b += 1
                c += 1

            while a < len(left):
                arr[c] = left[a]
                a += 1
                c += 1

            while b < len(right):
                arr[c] = right[b]
                b += 1
                c += 1
            
            yield arr
    yield from mergeSortRec(0, len(arr))  # call inner function with start/end arguments
    #manager.draw_list(draw_info, {3 : draw_info.GREEN, 4: draw_info.RED}, True) 
    
    yield
