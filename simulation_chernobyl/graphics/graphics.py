import pygame
import numpy as np
from ..graphics import rgb

# mouseover button effect, buttons are numerated by position
def mouseover(surface, x, y, color, mouse):
    if 177 + x * 31 < mouse[0] < 177 + x * 31 + 30 and 1 + y * 31 < mouse[1] < 1 + y * 31 + 30:   # if mouse is over button:
        pygame.draw.rect(surface, color, (177 + x * 31,1 + y * 31,30,30))  # color it

# mouseover button effect, buttons are defined by coordinates
def mouseover_coord(surface, x, y, color, mouse):
    if x < mouse[0] < x + 31 and y < mouse[1] < y + 31:   # if mouse is over button:
        pygame.draw.rect(surface, color, (x, y, 30, 30))  # color it

# group of mouseover button effects
def mouseover_group(surface, mouse):
    # button location      main set                  settings set
    mouseover(surface, 1, 0, rgb.gray1, mouse)   # sound switch            # - sound
    mouseover(surface, 6, 0, rgb.gray1, mouse)   # X                       # languages
    mouseover(surface, 7, 0, rgb.gray1, mouse)   # save                    # recording values
    mouseover(surface, 8, 0, rgb.gray1, mouse)   # settings                # config database
    mouseover(surface, 9, 0, rgb.red1, mouse)   # quit                    # cancle
    mouseover(surface, 0, 1, rgb.gray1, mouse)   # record                  # X
    mouseover(surface, 1, 1, rgb.gray1, mouse)   # show recorded graph     # - simstep
    mouseover(surface, 5, 1, rgb.gray1, mouse)   # simulation speed plus   # X
    mouseover(surface, 6, 1, rgb.gray1, mouse)   # X                       # X
    mouseover(surface, 7, 1, rgb.gray1, mouse)   # load                    # graph values
    mouseover(surface, 8, 1, rgb.gray1, mouse)   # help                    # config encoder

# prints text in box with word wrapping, with separator for bold tittle
def text_wrap(surface, text, pos, font, tittle_font, color=(0,0,0)):
    words = text.split(' ')   # convert string to list of words
    space = font.size(' ')[0]   # the width of a space
    x, y, maxw, maxh = pos   # get dimensions
    outfont = tittle_font   # set font to tittle font
    for word in words:   # for each word in list:
        word_surf = outfont.render(word, True, color)   # create word surface
        wordw, wordh = word_surf.get_size()   # get word size
        if x + wordw >= maxw or word == "///":   # if word goes over max or word is separator mark
            x = pos[0]   # reset x
            y += wordh   # start on new row
            if word == "///": outfont = font   # if word is separator mark change font to normal
        if word != "///":   # if word is not separator mark:
            surface.blit(word_surf, (x, y))   # show word
            x += wordw + space   # go to next word position

# prints text in box with word wrapping by readding line by line
def text_lines(surface, text_list, pos, font, line_space=0, color=(0,0,0)):
    x, y, maxw, maxh = pos   # get dimensions
    space = font.size(' ')[0]   # the width of a space
    for line_num, line in enumerate(text_list):   # for each row
        words = str((text_list[line_num]).rstrip()).split(' ')   # convert string to list of words
        x = pos[0]   # x dimension
        for word in words:   # for each word in list:
            word_surf = font.render(word, True, color)   # create word surface
            wordw, wordh = word_surf.get_size()   # get word size
            if x + wordw >= maxw:   # if word goes over max
                x = pos[0] + space   # reset x
                y += wordh   # start on new row
            surface.blit(word_surf, (x, y))   # show word
            x += wordw + space   # go to next word position
        y += wordh + line_space   # new row

# connect lines from element on graph to its corespondong name and draw outine box
def connect_lines(surface, coords_graph, coords_text, color=(0,0,0)):
    x_text, y_text, y_step_text = coords_text   # get text coordinates and step size
    for row_num, row in enumerate(coords_graph):   # for each row in graph coords matrix
        x1_scr, y1_scr, x2_scr, y2_scr, xc_scr, yc_scr = row[:6].astype(int)   # get graph coordinates
        # draw line
        pygame.draw.line(surface, color, (x_text, y_text + y_step_text/2 + row_num * y_step_text), (xc_scr, yc_scr))
        pygame.draw.rect(surface, color, (x1_scr, y1_scr, x2_scr - x1_scr +1, y2_scr - y1_scr + 1), 1)  # draw outline



class Grapher():
    def __init__(self):
        self.mem = 1
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 300, 150
        self.length = self.x2 - self.x1
        self.height = self.y1 - self.y2
        self.val = np.zeros([int(self.length),4])
        self.val0 = np.zeros([int((self.length)),2])
        self.counter_step = 1
        
    # graph dimensions
    def graph_dim(self, x1, y1, x2, y2, counter_step):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2   # absolute graph dimensions
        self.length = x2 - x1   # graph length
        self.height = y2 - y1   # graph height
        self.counter_step = counter_step   # counter step
        self.vals_num = 3   # number of values to be graphed
        vals = np.zeros(self.vals_num, dtype=object)
        self.val0 = np.zeros([int(self.length/(self.counter_step*10)),2])   # graph empty matrix
        
    # set line colors and number of values that will be imported
    def set_line_color(self, vals_num, line_colors):
        self.line_colors = line_colors   # line colors
        self.vals_num = vals_num   # line number
        self.val = np.zeros([int(self.length/(self.counter_step*10)),vals_num + 1])   # graph buffer matrix
    
    
    # add values to graph
    def add_val(self, counter, in_arr):
        self.val = np.roll(self.val, 1, axis=0)   # move all values in buffer
        self.val[:1] = np.zeros((self.val[:1].shape))   # one place down
        self.val[0,1:] = in_arr   # add new imputs
        self.val[0,0] = counter * 10   # add new x to buffer
        if counter >= ((self.length/2)/5):   # if buffer overflows:
            self.val[:,0] -= self.counter_step * 10   # substract 1 step from x coords
            if counter > ((self.length/2)/5): # in all next iterrations:
                self.val[0,0] -= (counter * 10 - (self.length/2)*2)   # make first x constant
                
    # draw graph
    def draw_graph(self, surface, antial=False):
        self.val0[:,0] = self.val[:,0] + self.x1   # add x values to seed from buffer
        for column_num, column in enumerate(self.val.T):   # for every column in val array (transpose, then read rows)
            if column_num != 0:   # skip first column - it is x value
                val_out = self.val0   # load x values in output line array
                val_out[:,1] = self.height - column + self.y1   # from buffer add y, and graph y coordinates
                color = self.line_colors[column_num - 1]   # set line color
                if antial is True: pygame.draw.aalines(surface, color, False, val_out, 2)   # draw graphed lines
                else: pygame.draw.lines(surface, color, False, val_out, 2)   # draw graphed lines
