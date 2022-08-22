# Credits: tech with tim
# Main Additions:
# Selection Sort and Heap Sort Algorithms
# Revamped Class Structure - instead of one long file
# Other Modifications: 
# Additional Calculations for bar placement
# Aesthetic Makeover - added more colors and gradients

import pygame
import sorting_algorithms
from classes import DrawingInfo, DrawingManager

pygame.init()


def main():

# variables

    screen_width = 800
    screen_height = 600

    num_vals = 50 
    min_val = 5 #list bounds
    max_val = 100

    run = True #controls
    sorting = False
    ascending = True

    list_config = 1 #controls mode of updating list
    speed = 60 #used for clock which can do at least 600
    speedUp = True #used to toggle
    clock = pygame.time.Clock() 

# Setting up List and Parameters
    dm = DrawingManager()
    #get list with vals only
    dm.configure_list(num_vals, min_val, max_val,list_config)
    draw_info = DrawingInfo(screen_width, screen_height, dm.lst) #instantiation of our class and useful vars based on list
    
    list_config = 2 # add x,y, coordinates
    dm.configure_list(num_vals, min_val, max_val, list_config, draw_info ) 
    #dm.setVals(draw_info) # set last values
    
    sorting_algorithim = sorting_algorithms.bubble_sort #holds sorting function
    sorting_algo_name = "Bubble Sort"
    sorting_algorithim_generator = None #stores object created by calling sort function

    while run:
        clock.tick(speed)
        #speed = 60 #used for clock which can do at least 600

        if sorting:
            try:
                next(sorting_algorithim_generator)
            except StopIteration:
                sorting = False
                #reset speed here if you want it to auto
        else:
            dm.draw(draw_info, sorting_algo_name, ascending) 


        for event in pygame.event.get(): #essentially hitting the x in the corner 
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN: #next event in forloop if no key presses
                continue

        # handles k presses for r, resets list
        # generates new list and draws it, 
            if event.key == pygame.K_r: 
                list_config = 3
                dm.configure_list(num_vals, min_val, max_val,list_config,draw_info) #set new sort_values 
                draw_info.set_list(dm.lst) #set new list parameters

                list_config = 2 #set new x and y values
                dm.configure_list(num_vals, min_val, max_val,list_config,draw_info) #predetermined aount of random list of vals in range 
                draw_info.lst = dm.lst #update and now use this list
                sorting = False
        # handles space presses to start sorting, obv only do so if
        # you aren't currntly sorting anything, thus False
            elif event.key == pygame.K_SPACE and sorting == False: 
                sorting = True
                sorting_algorithim_generator = sorting_algorithim(draw_info, dm, ascending)
                

            elif event.key == pygame.K_a and not sorting: #ascending
                ascending = True
            elif event.key == pygame.K_d and not sorting: # descending
                ascending = False
            elif event.key == pygame.K_n and not sorting: # descending
                speed = 60
            elif event.key == pygame.K_t and not sorting: # descending
                if speedUp:
                    speed = 20
                    speedUp = False
                else:
                    speed = 200
                    speedUp = True
            elif event.key == pygame.K_i and not sorting:
                sorting_algo_name = 'InsertionSort'
                sorting_algorithim = sorting_algorithms.insertion_sort
            elif event.key == pygame.K_b and not sorting:
                sorting_algo_name = 'Bubble Sort'
                sorting_algorithim = sorting_algorithms.bubble_sort
            elif event.key == pygame.K_s and not sorting:
                sorting_algo_name = 'Selection Sort'
                sorting_algorithim = sorting_algorithms.selection_sort
            elif event.key == pygame.K_h and not sorting:
                sorting_algo_name = 'Heap Sort'
                sorting_algorithim = sorting_algorithms.heap_sort
                ''' 
                heap sort will appear to run again on space press because
                it builds a max heap each time before it starts sorting,
                and since the heapify function updates the x value of of
                each bar during that process, 
                when heap sort starts sorting and thus drawing, it does so from the new positions
                of the max heap, and not the prior sorted array
                In fact, all the other sorting functions run again, but since they only
                alter the list when its unsorted, nothing is changed on the screen
                '''
    pygame.quit()


#makes sure this code is only run when meant to, not just whenever its imported etc
if __name__ == "__main__":
    main()