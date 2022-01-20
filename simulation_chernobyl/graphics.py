import pygame
import numpy as np

# colors
black = (0,0,0)
grey  = (210,210,210)
llime = (140,255,140)
lred  = (255,140,140)
red   = (255,0,0)
lime  = (0,255,0)

# mouseover button effect, buttons are numerated by position
def mouseover(surface, x, y, color, mouse):
    if 177 + x * 31 < mouse[0] < 177 + x * 31 + 30 and 1 + y * 31 < mouse[1] < 1 + y * 31 + 30:   # if mouse is over button:
        pygame.draw.rect(surface, color, (177 + x * 31,1 + y * 31,30,30))  # color it

# mouseover button effect, buttons are defined by coordinates
def mouseover_coord(surface, x, y, color, mouse):
    if x < mouse[0] < x + 31 and y < mouse[1] < y + 31:   # if mouse is over button:
        pygame.draw.rect(surface, color, (x , y, 30, 30))  # color it

# group of mouseover button effects
def mouseover_group(surface, mouse):
    # button location      main set                  settings set
    mouseover(surface, 1, 0, grey, mouse)   # sound switch            # - sound
    mouseover(surface, 6, 0, grey, mouse)   # X                       # languages
    mouseover(surface, 7, 0, grey, mouse)   # save                    # recording values
    mouseover(surface, 8, 0, grey, mouse)   # settings                # config database
    mouseover(surface, 9, 0, lred, mouse)   # quit                    # cancle
    mouseover(surface, 0, 1, grey, mouse)   # record                  # X
    mouseover(surface, 1, 1, grey, mouse)   # show recorded graph     # - simstep
    mouseover(surface, 5, 1, grey, mouse)   # simulation speed plus   # X
    mouseover(surface, 6, 1, grey, mouse)   # X                       # X
    mouseover(surface, 7, 1, grey, mouse)   # load                    # graph values
    mouseover(surface, 8, 1, grey, mouse)   # help                    # config encoder

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



class Logger():
    def __init__(self):
        self.mem_text = ""   # to store previous text
        self.text1, self.text2, self.text3 = "", "", ""   # text buffer
        self.text_color1, self.text_color2, self.text_color3 = (0,0,0), (0,0,0), (0,0,0)   # text color buffer
        self.max_width = 100
        
    # log displayed on surface during simulation
    def gui_logger(self, surface, font):
        surface.blit(font.render(str(self.text1), True, self.text_color1), (363, 669))   # text output line 1
        surface.blit(font.render(str(self.text2), True, self.text_color2), (363, 684))   # text output line 2
        surface.blit(font.render(str(self.text3), True, self.text_color3), (363, 699))   # text output line 3
        
    # add new text to log
    def log_add(self, text, text_color=black):
        if text != self.mem_text:   # if new text is sent:
            self.text3, self.text2, self.text1 = self.text2, self.text1, text   # add it to begenning, and shift others
            self.text_color3, self.text_color2, self.text_color1 = self.text_color2, self.text_color1, text_color   # same for colors
            if len(text) > self.max_width:   # if text is larger than window: split it and shift again
                self.text3, self.text2, self.text1 = self.text2, text[self.max_width : len(text)], text[0 : self.max_width]
                self.text_color3, self.text_color2, self.text_color1 = self.text_color2, text_color, text_color   # same for colors
        self.mem_text = text   # update mem
    
    # load max text width
    def gui_max_width(self, max_width):
        self.max_width = max_width


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
        self.val = np.zeros([int(self.length/(counter_step*10)),4])   # graph buffer matrix ###
        self.val0 = np.zeros([int(self.length/(counter_step*10)),2])   # graph empty matrix ###
        
    # add values to graph
    def add_val(self, counter, in1, in2, in3):
        self.val = np.roll(self.val, 1, axis=0)   # move all values in buffer
        self.val[:1] = np.zeros((self.val[:1].shape))   # one place down
        self.val[0,1] = in1   # add new in1 + graph y2, to buffer val1 ###
        self.val[0,2] = in2   # add new in2 + graph y2, to buffer val2 ###
        self.val[0,3] = in3   # add new in3 + graph y2, to buffer val3 ###
        self.val[0,0] = counter * 10   # add new x to buffer
        if counter >= ((self.length/2)/5):   # if buffer overflows:
            self.val[:,0] -= self.counter_step * 10   # substract 1 step from x coords
            if counter > ((self.length/2)/5): # in all next iterrations:
                self.val[0,0] -= (counter * 10 - (self.length/2)*2)   # make first x constant
                
    # draw graph
    def draw_graph(self, surface, antial=False):
        self.val0[:,0] = self.val[:,0] + self.x1   # add x values to seed from buffer
        val1 = self.val0   # set specific line matrix ### G
        val1[:,1] = self.height - self.val[:,1] + self.y1   # ad y to that specific line matrix from buffer ###
        if antial is True: pygame.draw.aalines(surface, (255,0,0), False, val1, 2)   # draw graphed lines ###
        else: pygame.draw.lines(surface, (255,0,0), False, val1, 2)   # draw graphed lines ###
        val2 = self.val0   # ### G
        val2[:,1] = self.height - self.val[:,2] + self.y1    # ### G
        if antial is True: pygame.draw.aalines(surface, (0,255,0), False, val2, 2)   # ###
        else: pygame.draw.lines(surface, (0,255,0), False, val1, 2)   # ### G
        val3 = self.val0   # ### G
        val3[:,1] = self.height - self.val[:,3] + self.y1    # ### G
        if antial is True: pygame.draw.aalines(surface, (0,0,255), False, val3, 2)   # ###
        else: pygame.draw.lines(surface, (0,0,255), False, val1, 2)   # ### G
