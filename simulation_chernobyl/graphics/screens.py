import pygame
import numpy as np
from ..graphics import graphics as gr
from ..graphics import rgb

class Screens():
    def __init__(self):
        self.windowx, self.windowy = 1280, 720
        self.surface = pygame.display.set_mode((self.windowx, self.windowy))
    
    # load everything needed
    def config(self, surface, windowx, windowy, lang):
        self.surface, self.windowx, self.windowy = surface, windowx, windowy
        self.gui = pygame.image.load("img/gui.png")   # load images
        self.menu = pygame.image.load("img/menu.png")
        self.setmenu = pygame.image.load("img/settings.png")
        self.runbt = pygame.image.load("img/run.png")
        self.stopbt = pygame.image.load("img/stop.png")
        self.soundon = pygame.image.load("img/sound.png")
        self.soundoff = pygame.image.load("img/mute.png")
        self.help_gui = pygame.image.load("img/help_gui.png")
        self.back = pygame.image.load("img/back.png")
        self.help_graph_all = pygame.image.load("img/help_all.png")
        self.rods_help = pygame.image.load("img/rods.png")
        self.link = pygame.image.load("img/link.png")
        self.accept = pygame.image.load("img/accept.png")
        self.cancle = pygame.image.load("img/cancle.png")
        self.fontlg = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 18)   # large text font
        self.fontmd = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 16)   # medium text font
        self.fontsm = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 15)   # small text font
        self.fontxl = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 20)   # extra large text font
        self.fontsb = pygame.font.Font("txt/fonts/LiberationSans-Bold.ttf", 14)   # small bold text font
        # load matrices containing names, mouseover and center coords for help surface
        self.moverbox = np.loadtxt("data/coords.txt", dtype='int', delimiter=',')
        self.rods_moverbox = np.loadtxt("data/rods_coords.txt", dtype='int', delimiter=',')
        self.graph_names_l = np.loadtxt("txt/"+lang+"/graph_coords_l.txt", dtype=object, delimiter=',')
        self.graph_names_r = np.loadtxt("txt/"+lang+"/graph_coords_r.txt", dtype=object, delimiter=',')
        self.graph_names_rods = np.loadtxt("txt/"+lang+"/graph_coords_rods.txt", dtype=object, delimiter=',')
        with open("txt/"+lang+"/expl.txt") as expl: self.explarr = expl.readlines()   # explanations
        with open("txt/"+lang+"/gui_expl.txt") as gui_expl: self.gui_explarr = gui_expl.readlines()   # gui explanations
        with open("txt/"+lang+"/rods_expl.txt") as rods_expl: self.rods_explarr = rods_expl.readlines()   # rods explanations
        
    # main menu, without main screen
    def main(self, mouse, pause, sound):
        gr.mouseover_group(self.surface, mouse)   # draw rectangles if mouse is over button
        gr.mouseover(self.surface, 2, 1, rgb.gray1, mouse)   # simulation speed minus
        gr.mouseover(self.surface, 9, 1, rgb.gray1, mouse)   # about
        # start/stop
        if pause is True: pygame.draw.rect(self.surface, rgb.green1, (177,1,30,30)) # if simulation is paused: color it
        gr.mouseover(self.surface, 0, 0, rgb.gray1, mouse) # start / stop
        if pause is True: self.surface.blit(self.runbt, (177, 1))   # if simulation is paused: show image
        else: self.surface.blit(self.stopbt, (177, 1))
        if sound is True: self.surface.blit(self.soundon, (208, 1))   # if sound is on
        else: self.surface.blit(self.soundoff, (208, 1))
        self.surface.blit(self.menu, (176, 0))      # show main menu image again because of mouseover effects
    
    # settings menu
    def settings(self, mouse, antial, sound_volume, zoom, lang):
        pygame.draw.rect(self.surface, (255,255,255), (177,1,309,61))   # settings overlay
        gr.mouseover_group(self.surface, mouse)   # mouseover effects for main menu
        if antial is True: pygame.draw.rect(self.surface, rgb.green1, (177,1,30,30))
        gr.mouseover(self.surface, 1, 0, rgb.gray1, mouse)   # - sound
        gr.mouseover(self.surface, 0, 0, rgb.gray1, mouse)   # anti aliasing
        gr.mouseover(self.surface, 4, 0, rgb.gray1, mouse)   # + sound
        gr.mouseover(self.surface, 5, 0, rgb.gray1, mouse)   # X
        gr.mouseover(self.surface, 4, 1, rgb.gray1, mouse)   # + zoom
        gr.mouseover(self.surface, 9, 1, rgb.green1, mouse)   # save
        self.surface.blit(self.setmenu, (177, 1))   # show settings
        self.surface.blit(self.fontlg.render("V:" + str(sound_volume), True, rgb.black), (248, 6))   # sound volume text
        self.surface.blit(self.fontlg.render("Z:" + str(zoom), True, rgb.black), (248, 37))   # graph zoom text
        self.surface.blit(self.fontsm.render(lang, True, rgb.black), (180, 37))   # languages
    
    # graph values picker
    def picker(self, mouse, texts_arr, vals, val_names, val_colors, will_rec, will_graph):
        pygame.draw.rect(self.surface, (255,255,255), (1,1,self.windowx-2,self.windowy-2))   # blank screen
        gr.mouseover_coord(self.surface, 1, 1, rgb.gray1, mouse)   # back button mouseover effect
        self.surface.blit(self.back, (0, 0))   # back button
        # lines
        line_pos = 31   # horizontal lines start
        while line_pos < self.windowy - 28:
            pygame.draw.line(self.surface, rgb.black, (0, line_pos), (self.windowx, line_pos))   # draw horizontal lines
            line_pos += 30   # space between 2 lines
        vertical_lines = [0, 40, 80, 130, 490, 638, 680, 720, 770, 1130]   # where will be drawn verticallines
        for vline in vertical_lines:
            pygame.draw.line(self.surface, rgb.black, (vline, 31), (vline, self.windowy))   # draw vertical lines
            if vline == vertical_lines[5]:   # if it is middle line: draw more one line next to it
                pygame.draw.line(self.surface, rgb.black, (vline + 2, 31), (vline + 2, self.windowy))
        # texts
        self.surface.blit(self.fontmd.render(str((texts_arr[6]).rstrip()), True, rgb.black), (40, 7))   # explanation text
        for word_repeat in range(2):   # repeat it twice:
            if word_repeat == 1: vertical_lines = vertical_lines[5:]   # in second iterration move to right side
            for word_num, word in enumerate(texts_arr[7].replace("\n", "").split(" ")):   # for every word
                word_pos = vertical_lines[word_num] + 6   # increase word position by line position
                self.surface.blit(self.fontmd.render(word, True, rgb.black), (word_pos, 38))   # print column names
        for num, val_name in enumerate(val_names):   # for every value:
            column = 0   # on what side should be written, default = left
            if 62 + num * 30 > self.windowy: column = 640   # if ther eis no more space on left: write on right side
            pygame.draw.rect(self.surface, val_colors[num], (81 + column, 62 + num * 30, 49, 29))   # value color
            self.surface.blit(self.fontmd.render(val_name, True, rgb.black), (136 + column, 68 + num * 30))   # value name
            self.surface.blit(self.fontmd.render(str(round(vals[num], 2)), True, rgb.black), (496 + column, 68 + num * 30))   # value
            if will_rec[num] == True:   # if this value will be recorded:
                pygame.draw.rect(self.surface, rgb.green1, (1 + column, 62 + num * 30, 39, 29))   # background color green
                self.surface.blit(self.accept, (5 + column, 62 + num * 30))   # show accept
            else:   # if not:
                pygame.draw.rect(self.surface, rgb.red1, (1 + column, 62 + num * 30, 39, 29))   # background color red
                self.surface.blit(self.cancle, (5 + column, 62 + num * 30))   # show X
            if will_graph[num] == True:   # if this value will be graphed:
                pygame.draw.rect(self.surface, rgb.green1, (41 + column, 62 + num * 30, 39, 29))   # background color green
                self.surface.blit(self.accept, (45 + column, 62 + num * 30))   # show accept
            else:   # if not:
                pygame.draw.rect(self.surface, rgb.red1, (41 + column, 62 + num * 30, 39, 29))   # background color red
                self.surface.blit(self.cancle, (45 + column, 62 + num * 30))   # show X
    
    # help screen
    def help(self, mouse, whelp_all, lang, texts_arr):
        gr.mouseover(self.surface, 0, 0, rgb.gray1, mouse)   # back button mouseover effect
        self.surface.blit(self.back, (176, 0))   # back button
        gr.mouseover(self.surface, 8, 1, rgb.green1, (426, 33))   # make help button lime
        self.surface.blit(self.menu, (176, 0))      # show main menu image again because of mouseover effects
        self.surface.blit(self.help_graph_all, (208, 1))   # all help diagram button
        pygame.draw.rect(self.surface, (255,255,255), (177,271,109,267))   # hide part of left imputs
        pygame.draw.rect(self.surface, (255,255,255), (1,539,360,180))   # hide graph
        pygame.draw.line(self.surface, rgb.black, (176, 271), (176, 537))   # draw border over that hidden part
        pygame.draw.rect(self.surface, (255,255,255), (1104,1,175,718))   # hide right inputs
        self.surface.blit(self.rods_help, (294, 549))   # rods help picture
        self.surface.blit(self.fontlg.render(str((texts_arr[4]).rstrip()), True, rgb.black), (5,543))   # inside core text
        
        # normal help with mouseover
        if whelp_all is False:
            gr.mouseover(self.surface, 1, 0, rgb.gray1, mouse)   # help diagram button
            self.surface.blit(self.help_graph_all, (208, 1))   # help diagram button
            self.surface.blit(self.help_gui, (1107,4))   # show gui help 
            self.surface.blit(self.fontsm.render(lang, True, rgb.black), (1111, 630))   # add language name to gui help
            for line_num, lines in enumerate(self.gui_explarr):   # for each line in gui explanations:
                # print that line in new row
                self.surface.blit(self.fontsm.render(str((self.gui_explarr[line_num]).rstrip()), True, rgb.black), (1145, int(4+(line_num*15.5))))
            # explanation text
            gr.text_wrap(self.surface, str((texts_arr[3]).rstrip()), (5 ,5, 177, 530), self.fontsm, self.fontsm, rgb.black) 
            # main explanations
            for line_num, lines in enumerate(self.moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    pygame.draw.line(self.surface, rgb.black, (165, 75), (190, 75))   # draw straight line
                    pygame.draw.line(self.surface, rgb.black, (190, 75), (lines[4], lines[5]))   # draw line conecting box
                    # draw outline
                    pygame.draw.rect(self.surface, rgb.black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)
                    # print text
                    gr.text_wrap(self.surface, str((self. explarr[line_num]).rstrip()), (5 ,67, 172, 530),self.fontsm, self.fontsb, rgb.black)
            # rods explanations
            for line_num, lines in enumerate(self.rods_moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    # draw outline
                    pygame.draw.rect(self.surface, rgb.black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)
                    # print text
                    gr.text_wrap(self.surface, str((self. rods_explarr[line_num]).rstrip()), (5 ,565, 285, 720),self.fontsm, self.fontsb, rgb.black)
                       
        # all help
        if whelp_all is True:
            gr.mouseover(self.surface, 1, 0, rgb.green1, (209, 2))   # make all_help button lime
            self.surface.blit(self.help_graph_all, (208, 1))   # show all_help buton again
            gr.text_lines(self.surface, self.graph_names_l[:,6], (5,5,172,520), self.fontsb, 6)   # left all help
            gr.connect_lines(self.surface, self.graph_names_l, (177, 2, 22))   # draw lines connecting left text to elements
            gr.text_lines(self.surface, self.graph_names_r[:,6], (1110,5,1280,520), self.fontsb, 6)   # right all help
            gr.connect_lines(self.surface, self.graph_names_r, (1103, 2, 22))   # draw lines connecting right text to elements
            gr.text_lines(self.surface, self.graph_names_rods[:,6], (5,565,172,520), self.fontsb, 6)   # rods all help
            gr.connect_lines(self.surface, self.graph_names_rods, (177, 562, 22))   # draw lines connecting rods text to elements
            pygame.draw.line(self.surface, rgb.black, (176, 538), (176, 719))   # names border extended line
    
    # about screen
    def about(self, mouse, about_txt):
        pygame.draw.rect(self.surface, (255,255,255), (1,1,self.windowx-2,self.windowy-2))   # blank screen
        gr.mouseover_coord(self.surface, 625, 16, rgb.gray1, mouse)   # back button mouseover effect
        self.surface.blit(self.back, (624, 15))   # back button
        gr.text_lines(self.surface, about_txt, (529,60,800,500), self.fontxl, 10)   # show about text
        gr.mouseover_coord(self.surface, 680, 222, rgb.gray1, mouse)
        gr.mouseover_coord(self.surface, 680, 256, rgb.gray1, mouse)
        gr.mouseover_coord(self.surface, 680, 290, rgb.gray1, mouse)
        self.surface.blit(self.link, (679, 221))   # github button
        self.surface.blit(self.link, (679, 255))   # wiki button
        self.surface.blit(self.link, (679, 289))   # report bug button
