import pygame
import random 

# I included this code in the repo as a demonstration of the starting code 
# generated from following the tutorial.

pygame.init()

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE =  255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY =  128, 128, 128
    BACKGROUND_COLOR = WHITE
    SIDE_PAD = 100 #total padding on each side for vizualization
    TOP_PAD = 150 
    # Font object for writing in pygame given style and size
    FONT = pygame.font.SysFont('comicsans',20)
    LARGE_FONT = pygame.font.SysFont('comicsans',30)

    GRADIENTS = [ #used to diferentiate blocks, FIXME add a reverse scale? 
       (128, 128, 128),
        (160,160,160),
        (192,192,192)
    ]

    RED_GRADIENTS = [ #used to diferentiate blocks, FIXME add a reverse scale? 
       (255, 0, 0),
        (205, 0, 0),
        (165, 0, 0)
    ]

    def __init__(self, width, height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithim Visualizer")
        self.set_list(lst)

    def set_list(self, lst): #parameters
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)

        '''
        block width = total drawing space (not including the side padding)
        divided by number of items in the list
        this makes the bars dynamically adjust to the number of elements in lsit
        '''
        self.block_width = int((self.width - self.SIDE_PAD) / len(lst))
        
        '''
        block height = determined by largest and smallest values in the list, creates a relative offset
        to be applied to each bar, e.g. if our max is 1000 and min is 0, the bar for 100 wouldnt be as high as 1000
        takes total vertical area (minus the very top pad) and divides the vertical area by the rang of values 
        '''
        self.block_height = int((self.height - self.TOP_PAD) / (self.max_value - self.min_value))
        self.actual_block_space = self.block_width * len(lst)
        self.screen = self.width - self.SIDE_PAD
        if (self.actual_block_space) < (self.screen):
            self.start_x = (self.SIDE_PAD // 2) + ((self.screen - self.actual_block_space) // 2)
        else:
            self.start_x = self.SIDE_PAD // 2

#takes in class instance, clears screen, then draws the bars for each value in list via draw_list function
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # 1 define font, #2 Render a font surface #3 Display it
    # access your window, blit takes in surface and coordinates x,y
   # title= draw_info.FONT.render("Sorting Algorithim Vizualizer", 1 ,draw_info.GREEN) #sharpness and color
   # draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 10))
    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1 ,draw_info.GREEN) #sharpness and color
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1 ,draw_info.BLACK) #sharpness and color
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

    sorting = draw_info.FONT.render("B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

    draw_list(draw_info) #
    pygame.display.update() #anytime you want to apply changes to the screen

#draws the rectangle for each value in list
def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    # used for clearing smaller portion of screen instead of entire screen 
    # when sorting especially
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD // 2, draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)

        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # drawing blocks or bars
    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_value)*draw_info.block_height 
        #height of screen minus height of rectangle + 
        #startring pos for drawing down
        color = draw_info.GRADIENTS[i % 3] #FIXEME

        #maps an index to a color to help visualize the sort better
        if i in color_positions:
            color = color_positions[i]

        # draw individual blocks or bars
        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.block_width, draw_info.height))

    if clear_bg: #this function's automatic parent updates, so if called manually we must update
        pygame.display.update()

#randomly creates a list with n values in the given range
def configure_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

# essentially grabs the max from the unsorted portion of the list and drags it to the 
# end on each pass, once it gets there, it will never move because we only 
# swap if its smaller, but in that case it wouldn't have been the max at all
def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)- 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending ) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j] #swaps
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True #allows for program to respond to other keys during sorting process
    
    return lst



def main():

    n = 50
    min_val = 0
    max_val = 100
    run = True
    sorting = False
    ascending = True
    speed = 60
    clock = pygame.time.Clock()

    lst = configure_list(n, min_val, max_val) #predetermined aount of random list of vals in range 

    draw_info = DrawInfo(800, 600, lst) #instantiation of our class

    sorting_algorithim = bubble_sort #holds sorting function
    sorting_algo_name = "Bubble Sort"
    sorting_algorithim_generator = None #stores object created by calling sort function

    while run:
        clock.tick(speed)

        if sorting:
            try:
                next(sorting_algorithim_generator)
            except StopIteration:
                sorting = False
                #reset speed here if you want it to auto
        else:
            draw(draw_info, sorting_algo_name, ascending) #draw_info.draw() self

        for event in pygame.event.get(): #essentially hitting the x in the corner 
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN: #next event in forloop if no key presses
                continue

        # handles k presses for r, resets list
        # generates new list and draws it, 
            if event.key == pygame.K_r: 
                lst = configure_list(n, min_val, max_val) #predetermined aount of random list of vals in range 
                draw_info.set_list(lst)
                sorting = False

        # handles space pressesto start sorting, obv only do so if
        # you aren't currntly sorting anything, thus False
            elif event.key == pygame.K_SPACE and sorting == False: 
                sorting = True
                sorting_algorithim_generator = sorting_algorithim(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_s and not sorting:
                speed = 20
            elif event.key == pygame.K_b and not sorting:
                sorting_algo_name = 'Bubble Sort'
                sorting_algorithim = bubble_sort

    pygame.quit()

#makes sure this code is only run when meant to, not just whenever its imported etc
if __name__ == "__main__":
    main()

