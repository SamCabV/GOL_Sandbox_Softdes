import requests
import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
import string
import pandas as pd
import matplotlib
import matplotlib.animation as animation
import copy
import pygame
pygame.font.init()
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)

def user_inputs():   
    pygame.init()
    screen = pygame.display.set_mode((640, 480))


    clock = pygame.time.Clock()
    game_mode = 0 # 0 = GOL, 1 = GORB, 2 = Custom
    input_box1 = InputBox(450, 325, 160, 32)
    input_box2 = InputBox(450, 375, 160, 32)
    text_box1 = TextBox(360, 325, 90, 32,"Input α:")
    text_box2 = TextBox(360, 375, 90, 32,"Input δ:")
    gol_switch = button(COLOR_ACTIVE, 50, 225, 150, 50, "Play GOL") 
    gorb_switch = button(COLOR_INACTIVE, 250, 225, 150, 50, "Play GORB") 
    custom_switch = button(COLOR_INACTIVE, 450, 225, 150, 50, "Play Custom")
    finish_switch = button(COLOR_INACTIVE, 50, 325, 300, 80, "Start Game")
    
    input_boxes = [input_box1, input_box2]
    boxes = [input_box1, input_box2, text_box1, text_box2]
    switches = [gol_switch,gorb_switch,custom_switch,finish_switch]
    done = False

    while not done:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gol_switch.isOver(pos):
                    if game_mode == 0:
                        pass
                    else:
                        game_mode = 0
                        gol_switch.color = COLOR_ACTIVE
                        gorb_switch.color = COLOR_INACTIVE
                        custom_switch.color = COLOR_INACTIVE
                        
                if gorb_switch.isOver(pos):
                    if game_mode == 1:
                        pass
                    else:
                        game_mode = 1
                        gol_switch.color = COLOR_INACTIVE
                        gorb_switch.color = COLOR_ACTIVE
                        custom_switch.color = COLOR_INACTIVE
                        
                if custom_switch.isOver(pos):
                    if game_mode == 2:
                        pass
                    else:
                        game_mode = 2
                        gol_switch.color = COLOR_INACTIVE
                        gorb_switch.color = COLOR_INACTIVE
                        custom_switch.color = COLOR_ACTIVE
                
                if finish_switch.isOver(pos):
                    output = [game_mode, input_box1.text, input_box2.text]
                    pygame.quit()
                    return output
                    

                
                    
            if event.type == pygame.MOUSEMOTION:
                if gol_switch.isOver(pos):
                    if game_mode == 0:
                        pass
                    else:
                        gol_switch.color = COLOR_ACTIVE
                        gorb_switch.color = COLOR_INACTIVE
                        custom_switch.color = COLOR_INACTIVE
                        
                if gorb_switch.isOver(pos):
                    if game_mode == 1:
                        pass
                    else:
                        gol_switch.color = COLOR_INACTIVE
                        gorb_switch.color = COLOR_ACTIVE
                        custom_switch.color = COLOR_INACTIVE
                
                if custom_switch.isOver(pos):
                    if game_mode == 2:
                        pass
                    else:
                        gol_switch.color = COLOR_INACTIVE
                        gorb_switch.color = COLOR_INACTIVE
                        custom_switch.color = COLOR_ACTIVE
                
                if finish_switch.isOver(pos):
                        finish_switch.color = COLOR_ACTIVE
                else:
                        finish_switch.color = COLOR_INACTIVE
                
            for box in input_boxes:
                box.handle_event(event)

        screen.fill((30, 30, 30))
        for box in boxes:
            box.draw(screen)
        for switch in switches:
            switch.draw(screen)

        pygame.display.flip()
        clock.tick(30)

class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.Font(None, 32)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
class InputBox:
    #FONT = pygame.font.Font(None, 32)
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
class TextBox:
    #FONT = pygame.font.Font(None, 32)
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

def draw(dimx, dimy):

    cellsize = 8
    sz = 8
       
    vdimx = dimx-2
    vdimy = dimy -2
    
    grid = make_grid(dimx,dimy) 

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    surface = pygame.display.set_mode((vdimx * cellsize, vdimy * cellsize))
    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (sz)
                row = pos[1] // (sz)
                # Set that location to one
                if grid[row][column] == 0:
                    grid[row][column] = 1
                else:
                    grid[row][column] = 0
                #print("Click ", pos, "Grid coordinates: ", row, column)
        
        # Set the screen background
        surface.fill(col_background)
        
        for j, tile in enumerate(grid):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*sz,j*sz,sz,sz)
                pygame.draw.rect(surface, map_color(tile_contents), myrect)

        

        # Draw the grid
        draw_grid(surface,dimx,dimy)


        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    return grid
def draw_grid(surface, dimy, dimx):
    sz = 8
    for i in range(dimx):
        new_height = round(i*sz)
        new_width = round(i*sz)
        pygame.draw.line(surface, col_alive, (0,new_height), (10000,new_height),1)
        pygame.draw.line(surface, col_alive, (new_width,0), (new_width,10000),1)
def game(dimx, dimy, cellsize,grid,alpha = [2,3], delta = [3],GORB = 0):
    pygame.init()
    vdimx = dimx-2
    vdimy = dimy -2
    surface = pygame.display.set_mode((vdimx * cellsize, vdimy * cellsize))
    pygame.display.set_caption("John Conway's Game of Life")
    
    cells = grid
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        surface.fill(col_grid)
        
        cells = play_round(surface, cells,alpha,delta, GORB)
        clock.tick(60)

        pygame.display.update()

def map_color(cell):

    if cell == 0:
        col = col_background
    if cell == 1:
        col= col_alive
    return col
def play_round(surface, grid, alpha = [2,3],delta = [3], GORB = 0):

    if GORB == 0:
        sz = 8
        #test = copy.deepcopy(grid)
        #test = copy.copy(grid)
        size = grid.shape
        new_grid = make_grid(size[0],size[1])
        for i in range(size[0]-2):
            for j in range(size[1]-2):            
                new_grid[i+1][j+1] = evaluate(i+1,j+1,grid,alpha,delta)
        for j, tile in enumerate(new_grid):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*sz,j*sz,sz,sz)
                pygame.draw.rect(surface, map_color(tile_contents), myrect)
        draw_grid(surface,size[0],size[1])
        return new_grid
    if GORB == 1:
        sz = 8
        #test = copy.deepcopy(grid)
        #test = copy.copy(grid)
        size = grid.shape
        new_grid = make_grid(size[0],size[1])
        for i in range(size[0]-2):
            for j in range(size[1]-2):
                alpha_rand = random.sample(range(0,8),random.randint(0,8))
                delta_rand = random.sample(range(0,8),random.randint(0,8))
                new_grid[i+1][j+1] = evaluate(i+1,j+1,grid,alpha_rand,delta_rand)
        for j, tile in enumerate(new_grid):
            for i, tile_contents in enumerate(tile):
                myrect = pygame.Rect(i*sz,j*sz,sz,sz)
                pygame.draw.rect(surface, map_color(tile_contents), myrect)
        draw_grid(surface,size[0],size[1])
        return new_grid
def evaluate(n,m,grid,alpha,delta):
    an = n
    am = m
    alpha_check = []
    delta_check = []
    new_cell = cell(grid[an][am],grid[an+1][am],grid[an+1][am+1],grid[an][am+1],grid[an-1][am],grid[an][am-1],grid[an-1][am-1],grid[an+1][am-1],grid[an-1][am+1])
    
    if new_cell._state == 0:
        for i in delta:
            delta_check.append(new_cell.check_n(i))
        next_state = any(delta_check)
    if new_cell._state == 1:
        for i in alpha:
            alpha_check.append(new_cell.check_n(i))
        next_state = any(alpha_check)
    return next_state
class cell:
    
    def __init__(self, state, TL, T, TR, L, R, BL, B, BR):
        self._state = state
        self._num_n = TL + T + TR + L + R + BL + B + BR
    
    def check_n(self,n):
        if self._num_n == n:
            return 1
        else:
            return 0
def make_grid(n,m):
    grid = np.zeros((n+2, m+2), dtype=int)
    return grid
def populate_grid(keyn, keym, grid):
    grid[keyn+2, keym+2] = 1
    return grid
    
