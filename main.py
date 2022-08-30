import pygame
import sorting_algorithms
from classes import DrawingInfo, DrawingManager

# This module holds the main function and is used to run the demonstration
# It is this configuration purely for convenience.

pygame.init()

def main():

# variables

    screen_width = 800
    screen_height = 600

    num_vals = 70 
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
    
    dm.configure_list(num_vals, min_val, max_val, list_config) #get list with vals only
    draw_info = DrawingInfo(screen_width, screen_height, dm.lst) #instantiation of our class and useful vars based on list
    
    list_config = 2 # add x,y, coordinates
    dm.configure_list(num_vals, min_val, max_val, list_config, draw_info ) 
    
    sorting_algorithim = sorting_algorithms.bubble_sort #holds sorting function
    sorting_algo_name = "Bubble Sort"
    sorting_algorithim_generator = None #stores object created by calling sort function

    while run:
        clock.tick(speed)

        if sorting:
            try:
                next(sorting_algorithim_generator)
            except StopIteration:
                sorting = False
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
                dm.configure_list(num_vals, min_val, max_val, list_config, draw_info) #set new sort_values 
                draw_info.set_list(dm.lst) #set new list parameters like min, max,

                list_config = 2 #set new x and y values
                dm.configure_list(num_vals, min_val, max_val, list_config, draw_info) #predetermined aount of random list of vals in range 
                draw_info.lst = dm.lst #update and now use this list
                sorting = False
    
            elif event.key == pygame.K_SPACE and sorting == False: 
                sorting = True
                sorting_algorithim_generator = sorting_algorithim(draw_info, dm, ascending)
                

            elif event.key == pygame.K_a and not sorting: #ascending
                ascending = True

            elif event.key == pygame.K_d and not sorting: # descending
                ascending = False

            elif event.key == pygame.K_n and not sorting: # normal speed
                speed = 60

            elif event.key == pygame.K_t and not sorting: # toggle speed
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
            elif event.key == pygame.K_m and not sorting:
                sorting_algo_name = 'Merge Sort'
                sorting_algorithim = sorting_algorithms.merge_sort

    pygame.quit()


if __name__ == "__main__":
    main()