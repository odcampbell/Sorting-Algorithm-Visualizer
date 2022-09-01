import pygame
import random 

# This module holds the main classes for drawing and 
# using the screen in pygame

pygame.init()

# This class holds the majority of the data needed for drawing
# and manages those values dynamically throughout the execution
class DrawingInfo: 
    #colors
    BLACK = 0, 0, 0     
    WHITE =  255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY =  128, 128, 128
    PINK = 255,192,203
    OG_LIGHT = 255,195,120
    YELLOW = 252,210,80
    ORANGE = 225,100,0
    BACKGROUND_COLOR = 245,245,220
    SIDE_PAD = 100
    TOP_PAD = 190 
    listCount = 50
                                     
    FONT = pygame.font.SysFont('comicsans', 17) # Font object for writing in pygame given style and size
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    GREY_GRADIENTS = [ #used to diferentiate bars
       (128, 128, 128),
        (160,160,160),
        (192,192,192)
    ]

    OG_GRADIENTS = [
       (147,112,219),
        (255,165,0),
        (225,100,0)#light
    ]
    
    BERRY_GRADIENTS = [
       (0, 0, 220),
        (128, 0, 128),
        (205, 0, 145)
    ]

    def __init__(self, width, height, lst):

        self.window_width = width
        self.window_height = height
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("Sorting Algorithim Visualizer")
        self.set_list(lst)
        self.screen_center = self.window_width / 2  
        self.list_screen_fill = (self.SIDE_PAD // 2, self.TOP_PAD,
                self.window_width - self.SIDE_PAD, self.window_height - self.TOP_PAD) 

# helps configure variables for drawing the list based on the current values
    def set_list(self, lst): 

        self.lst = lst
        self.min_value = min(lst, key=lambda x: x.sort_val).sort_val
        self.max_value = max(lst, key=lambda x: x.sort_val).sort_val
        self.bar_width = int((self.window_width - self.SIDE_PAD) / len(lst))
        self.bar_height = int((self.window_height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.actual_bar_space = self.bar_width * len(lst)
        self.screen = self.window_width - self.SIDE_PAD

        #arranges bars back in center if they didnt evenly divide the screen
        if (self.actual_bar_space) < (self.screen): 
            self.start_x = (self.SIDE_PAD // 2) + ((self.screen - self.actual_bar_space) // 2)
        else:
            self.start_x = self.SIDE_PAD // 2

# Used to make pygame window resize decently as height and width change
    def resize_screen(self, width, height):
        self.window_width = width
        self.window_height = height
        self.window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        self.screen_center = self.window_width / 2  
        self.list_screen_fill = (self.SIDE_PAD // 2, self.TOP_PAD,
                self.window_width - self.SIDE_PAD, self.window_height - self.TOP_PAD)
        self.bar_width = int((self.window_width - self.SIDE_PAD) / len(self.lst))
        self.bar_height = int((self.window_height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.actual_bar_space = self.bar_width * len(self.lst)
        self.screen = self.window_width - self.SIDE_PAD
        if (self.actual_bar_space) < (self.screen): 
            self.start_x = (self.SIDE_PAD // 2) + ((self.screen - self.actual_bar_space) // 2)
        else:
            self.start_x = self.SIDE_PAD // 2        

# This class represents each individual bar and allows us to store
# the x and y values associated with it to calculate outside of the
# draw_list function if needed, and to do less work during the drawing process
class Bars:
    def __init__(self, val):
        self.sort_val = val
        self.x = 0
        self.y = 0

# This clas holds the main drawing functions
class DrawingManager:
    def __init__(self):
        self.lst = []

    '''
    used every time you want a new set of random nums, or when sorting
    list_config = 1 : create list of bar objects assigned random values, 
    list_config = 2 : update visual bar coordinates
    list_config = 3 : assign the previously created bar object a new value
    Always call either 1 or 3 then 2. Anytime we update a bars's sorting value, it's y val
    for drawing must change. Whenever we update a bar's location in the list 
    (via other functions) we must call this function to update it's x value
    May make more sense to place this fucntion inside of draw_info,
    but becasue of the co-dependency between the classes, this function
    might not have an ideal location as it is currently (and was perviously) designed
    '''
    def configure_list(self, listSize, min_val, max_val, list_config, draw_info=None):
        
        #first pass, make bar then set list
        if list_config == 1:
            for i in range(listSize):
                val = random.randint(min_val, max_val)
                bar = Bars(val)
                self.lst.append(bar) #list of bars
        
        #second pass, calc xy
        elif list_config == 2:
            for index, bar in enumerate(self.lst):
                bar.x = draw_info.start_x + index * draw_info.bar_width
                bar.y = draw_info.window_height - (bar.sort_val - draw_info.min_value) * draw_info.bar_height 
        
        #third pass, (3,2) don't need to remake bar obj just change val
        elif list_config == 3:
            for index, bar in enumerate(self.lst):
                bar.sort_val = random.randint(min_val, max_val)

# Called to update bar position and draw list on screen after a swap
    def draw_list(self, draw_info, color_positions = {}, clear_bg = False, merge=False, merge_list = None):
        
        if merge:
            draw_info.lst = merge_list
        # used for clearing smaller portion of screen when sorting 
        if clear_bg:
            pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, draw_info.list_screen_fill)

        # drawing bars (alternate colors)
        for i, bar in enumerate(draw_info.lst):
            color = draw_info.OG_GRADIENTS[i % 3] 
            bar.x = draw_info.start_x + i * draw_info.bar_width 
            #updating x here because sorting moves the bar within the list
            
            if i in color_positions:
                color = color_positions[i] # maps an index to a color 

            # draw individual bars
            pygame.draw.rect(draw_info.window, color, (bar.x, bar.y, draw_info.bar_width, draw_info.window_height))

        if clear_bg: #when parent doesnt update display we must update it
            pygame.display.update()

# takes in drawinfo object, clears screen, then draws the bars 
# for each value in list via draw_list function
    def draw(self, draw_info, algo_name, ascending):
        
        draw_info.window.fill(draw_info.BACKGROUND_COLOR)

        title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1 ,draw_info.ORANGE) #sharpness and color
        draw_info.window.blit(title, (draw_info.screen_center - title.get_width()/2 , 5))

        controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1 ,draw_info.BLACK) #sharpness and color
        draw_info.window.blit(controls, (draw_info.screen_center - controls.get_width()/2 , 45))
        controls1 = draw_info.FONT.render("T - Toggle Speed | N - Normal Speed", 1 ,draw_info.BLACK) #sharpness and color
        draw_info.window.blit(controls1, (draw_info.screen_center - controls1.get_width()/2 , 75))

        sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | H - Heap Sort | M - Merge Sort", 1, draw_info.BLACK)
        draw_info.window.blit(sorting, (draw_info.screen_center - sorting.get_width()/2 , 105))

        self.draw_list(draw_info) #
        pygame.display.update() #anytime you want to apply changes to the screen
    


