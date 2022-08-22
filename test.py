
def heapify( lst, list_size, index,):
    #dm = manager
    #lst 
    left = 2*index+1
    right = 2*index+2
    max = index
    #if left chld is in scope and greater than parent
    if left < list_size and  lst[left] <lst[max]:
        max = left

    #if right chld is in scope and greater than parent
    if right < list_size and  lst[right]< lst[max]:
        max = right
    
    if(max!=index):
        lst[(index)], lst[(max)] = lst[(max)], lst[(index)] #defined in algorithm!!
       # lst[(index)].x = draw_info.start_x + index * draw_info.bar_width 
       # lst[(max)].x = draw_info.start_x + max * draw_info.bar_width  
        #dm.draw_list(draw_info, {index : draw_info.GREEN, max: draw_info.RED}, True)
        heapify(lst, list_size,max)

    #return lst #necessarry?

def build_max_heap(lst, list_size):
    for i in range(list_size//2-1, -1, -1): #FIXME how to count down in python, whiel?
        heapify(lst,list_size, i)
        #yield True

def heap_sort(lst):
    size = len(lst)

    for i in range(size//2 - 1, -1, -1): #FIXME how to count down in python, whiel?
        heapify(lst,size, i)

    for i in range(size-1,0,-1):
        lst[i],  lst[0] =  lst[0],  lst[i]
        #dm.draw_list(draw_info, {i : draw_info.GREEN, 0: draw_info.RED}, True)
        heapify(lst,i, 0 )
    

if __name__ == "__main__" :
    arr = [12, 11, 13, 5, 6, 7, ]
    heap_sort(arr)
    n = len(arr)
    print('Sorted array is')
    for i in range(n):
        print(arr[i])
