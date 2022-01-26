import pygame
import numpy as np
import math
import time
import datetime
import webbrowser

from simulation_chernobyl.util import fileops
from simulation_chernobyl.graphics import graphics
from simulation_chernobyl.graphics import logger
from simulation_chernobyl.graphics import screens
from simulation_chernobyl.graphics import rgb

logger = logger.Logger()
grapher = graphics.Grapher()
screens = screens.Screens()



# --Todo-- #
###### recorder, show
##### zoom graph
### auto scale graph

######### engine
######## main interface
##### save, load, save on quit
### logging
## second graph ???
## icon

version = "Pre-alpha 0.2.0"
date = "(26.1.2022)" 



###### --Initial variables-- ######
update = 30   # screen update frequency
windowx, windowy = 1280, 720   # window width, window height

simspeed = 1.0   # simulation speed multiplyer
sound_volume = 5   # initial sound volume
zoom = 1   # graph zoom
counter_step = 0.1   # simulation step size
counter = 0   # simulation time

antial = False   # anti aliasing
sound = True   # sound on/off
pause = True   # program paused
settings = False   # settings open
graph_picker = False   # graph picker open
whelp = False   # help window open
whelp_all = False   # full diagram show
wabout = False   # about window open
welcome = False   # print welcome text

lang = "eng"   # simulation language
lang_num = 1   # index of language in use

textout_color = rgb.black   # initial text color
grapher.graph_dim(1, 538, 361, 718, counter_step)   # grapher dimensions



###### --Load database-- ######

###### --Load encoder-- ######

###### --Initial values for grapher-- ######
vals = np.zeros(6)   # empty array to store all values
val_names = ["val1", "val2", "val3", "val4", "val5", "val6"]   # names of these values
val_colors = np.array([rgb.red, rgb.lime, rgb.blue, rgb.black, rgb.purple, rgb.cyan])   # initial line colors
will_rec = np.array([False, True, False, True, False, False])   # will these values be recorded?
will_graph = np.array([True, True, True, False, False, False])   # will these values be graphed?

graph_line_num = 4   # initial number of lines on graph
grapher.set_line_color(graph_line_num, val_colors)   # set initial line colors
vals_graph = np.zeros(graph_line_num)   # empty array to store values that are graphed
colors_graph = np.zeros(graph_line_num, dtype=object)   # empty array to store value colors that are graphed



###### --Load settings-- ######
try:
    antial, sound_volume, zoom, lang = fileops.load_settings()   # try to load settings from file
except:
    setfile = open("data/settings.txt","w+")   # create settings file
    setfile.write(str(antial)+' '+str(sound_volume)+' '+str(zoom)+' '+lang+' ')   # write to settings file
    setfile.close()   # close file
    whelp = True   # Show help
    welcome = True   # print welcome text



###### --Load texts-- ######
languages = np.loadtxt("txt/languages.txt", dtype='str')   # languages list
with open("txt/"+lang+"/texts.txt") as texts: texts_arr = texts.readlines()   # texts
with  open("txt/"+lang+"/about.txt") as fabout_txt: about_txt = fabout_txt.readlines()   # about text
about_txt[0] = about_txt[0].rstrip() + " " + version
about_txt[1] = date



###### --initialize GUI-- ######
pygame.init()   # initialize pygame
pygame.display.set_icon(pygame.image.load('img/icon.png'))   # set game icon
screen = pygame.display.set_mode((windowx, windowy))   # set window size
gui = pygame.image.load("img/gui.png")
menu = pygame.image.load("img/menu.png")
fontlg = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 18)   # large text font
fontmd = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 16)   # medium text font
fontsm = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 15)   # small text font
fontxl = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 20)   # extra large text font
fontsb = pygame.font.Font("txt/fonts/LiberationSans-Bold.ttf", 14)   # small bold text font
clock = pygame.time.Clock()   # start clock
# how many times calculations event is repeated in one iterration of main loop
pygame.time.set_timer(pygame.USEREVENT, int(100/simspeed))



###### --Classes settings-- ######
screens.config(screen, windowx, windowy, lang)
logger.gui_max_width(60)   # max text width



###### --Main loop-- ######
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:   # if any key is pressed:
            # --Key setup-- #
            if e.key == pygame.K_ESCAPE: run = False  # if "escape" key is pressed, close program
            if e.key == pygame.K_p:   # if "P" key is pressed:
                if pause is False: pause = True   # if it is not paused, pause it 
                else: pause = False  # if it is paused, unpause it
        
        
        
        ###### -- Button engine-- ######
        mouse = pygame.mouse.get_pos()   # get mouse position
        if e.type == pygame.MOUSEBUTTONDOWN:   # if mouse clicked:
            
            # main menu
            if settings is False and whelp is False and wabout is False and graph_picker is False:
                if 177 < mouse[0] < 207 and 1 < mouse[1] < 31:   # start /stop
                    if pause is False: pause = True    # pause
                    else: pause = False   # unpause
                if 208 < mouse[0] < 238 and 1 < mouse[1] < 31:   # sound
                    if sound is False: sound = True    # unmute
                    else: sound = False   # mute
                if 239 < mouse[0] < 269 and 32 < mouse[1] < 62:   # simulation speed minus
                    if simspeed >= 0.15:   # if simulation speed is over minimal:
                        if simspeed <= 1.2: simspeed -= 0.1   # if simspeed is bellow 1.2 decrease by 0.1
                        if simspeed > 1.2: simspeed -= 0.2   #if simspeed is above 1.2 decrease by 0.2
                        pygame.time.set_timer(pygame.USEREVENT, int(100/simspeed))   # update simspeed
                if 332 < mouse[0] < 362 and 32 < mouse[1] < 62:   # simulation speed plus
                    if simspeed <= 9.9:
                        if simspeed < 1.2: simspeed += 0.1
                        if simspeed >= 1.2: simspeed += 0.2
                        pygame.time.set_timer(pygame.USEREVENT, int(100/simspeed))
                if 425 < mouse[0] < 455 and 1 < mouse[1] < 31: settings, pause = True, True   # switch to settings
                if 363 < mouse[0] < 393 and 1 < mouse[1] < 31: graph_picker, pause = True, True   # switch to graph picker
                if 425 < mouse[0] < 455 and 32 < mouse[1] < 62: whelp, pause = True, True   # switch to help
                if 456 < mouse[0] < 486 and 32 < mouse[1] < 62: wabout, pause = True, True   # switch to about
                if 456 < mouse[0] < 486 and 1 < mouse[1] < 31: run = False   # quit
            
            # graph picker
            if graph_picker is True:
                for num, val_name in enumerate(val_names):   # for every value:
                    if 1 < mouse[0] < 40 and 62 + num * 30 < mouse[1] < 62 + num * 30 + 29:   # recorder
                        will_rec[num] = not will_rec[num]   # invert: False <-> True
                    if 41 < mouse[0] < 80 and 62 + num * 30 < mouse[1] < 62 + num * 30 + 29:   # grapher
                        will_graph[num] = not will_graph[num]   # invert: False <-> True
                    if 81 < mouse[0] < 130 and 62 + num * 30 < mouse[1] < 62 + num * 30 + 29:   # colors
                        cur_color = 0   # current color
                        for row_num, row in enumerate(rgb.all_main):   # for all colors in array:
                            if np.array_equal(val_colors[num], row):   # if current color is same as color in array
                                cur_color = row_num   # output index of it
                                break   # break loop
                        if cur_color == len(rgb.all_main) - 1:   # if this is last color in list:
                            cur_color = -1   # rotate to start (-1 becouse later it will be returned to 0)
                        val_colors[num] = rgb.all_main[cur_color + 1]   # move to next color in array
                graph_line_num = len(np.delete(will_graph, np.where(will_graph == False)))   # new number of graph lines
                vals_graph = np.zeros(graph_line_num)   # list of vals to be on graph
                colors_graph = np.zeros(graph_line_num, dtype=object)   # output color list
                if 0 < mouse[0] < 31 and 1 < mouse[1] < 31:   # back
                    graph_picker = False
                    num_out = 0   # iterable value for output list
                    for num, check in enumerate(will_graph):   # iterate over all variables
                        if check == True:   # if this value is marked to be plotted:
                            colors_graph[num_out] = val_colors[num]   # add its color to output list
                            num_out += 1   # iterate output list
                    grapher.set_line_color(graph_line_num, colors_graph)   # update grapher colors
                    
            # settings
            if settings is True:
                if 456 < mouse[0] < 486 and 1 < mouse[1] < 31:   # cancle settings changes:
                    settings = False   # exit settings
                    antial, sound_volume, zoom, lang = fileops.load_settings()   # reload settings from file
                if 456 < mouse[0] < 486 and 32 < mouse[1] < 62:   # save settings
                    settings = False   # exit settings
                    setfile = open("data/settings.txt","w+")   # open settings file
                    setfile.write(str(antial)+' '+str(sound_volume)+' '+str(zoom)+' '+lang+' ')   # write to settings file
                    setfile.close()   # close file
                if 177 < mouse[0] < 207 and 1 < mouse[1] < 31:    # turn on antialias
                    if antial is False: antial = True
                    else: antial = False   # turn off antial
                if 208 < mouse[0] < 238 and 1 < mouse[1] < 31 and sound_volume > 1: sound_volume -= 1  # sound volume minus
                if 301 < mouse[0] < 331 and 1 < mouse[1] < 31 and sound_volume < 10: sound_volume += 1  # sound volume plus
                if 208 < mouse[0] < 238 and 32 < mouse[1] < 62 and zoom > 1: zoom -= 1   # zoom minus
                if 301 < mouse[0] < 331 and 32 < mouse[1] < 62 and zoom < 5: zoom += 1   # zoom plus
                if 177 < mouse[0] < 207 and 32 < mouse[1] < 62:    # change language
                    lang = languages[lang_num]   # load language
                    lang_num +=1   # iterate over languages
                    if lang_num >= len(languages): lang_num = 0   # rotate lang num
                    logger.log_add(str((texts_arr[5]).rstrip()), rgb.black)   # print that simulation must restart
                    
            # help window
            if whelp is True:
                if whelp_all is False:   # if help all is closed:
                    if 177 < mouse[0] < 207 and 1 < mouse[1] < 31: whelp = False   # back
                    if 208 < mouse[0] < 238 and 1 < mouse[1] < 31: whelp_all = True  # help all
                if whelp_all is True: # if help all is open:
                    if 177 < mouse[0] < 207 and 1 < mouse[1] < 31: whelp_all = False   # back
                    
            # about window
            if wabout is True:
                if 625 < mouse[0] < 656 and 16 < mouse[1] < 47: wabout = False   # back
                if 680 < mouse[0] < 711 and 222 < mouse[1] < 253:   # open github link
                    webbrowser.open(r"https://github.com/mzivic7/Simulation-Chernobyl")
                # if 680 < mouse[0] < 711 and 255 < mouse[1] < 286:   # open wiki link
                    # webbrowser.open(r"")   # ###
                if 680 < mouse[0] < 711 and 289 < mouse[1] < 320:   # open report bug link
                    webbrowser.open(r"https://github.com/mzivic7/Simulation-Chernobyl/issues")
        
        
        
        ###### --Calculations-- ######
        if e.type == pygame.USEREVENT:   # event for calculations
            if pause is False:   # if it is not paused:
                
                ###### --Engine-- ######
                
                vals[0] = 88 + (math.sin(counter/2))*50   # test values
                vals[1] = 88 + (math.sin((counter/2)+(2*math.pi/3)))*50
                vals[2] = 88 + (math.sin((counter/2)+(4*math.pi/3)))*50
                vals[3] = 88
                vals[4] = 44
                vals[5] = 132
                
                num_out = 0   # iterable value for output list
                for num, check in enumerate(will_graph):
                    if check == True:   # if this value is marked to be plotted:
                        vals_graph[num_out] = vals[num]   # add it to output list
                        num_out += 1   # iterate output list
                grapher.add_val(counter, vals_graph)   # add values to graph
                counter += counter_step   # iterate counter
                counter = round(counter, 2)   # round counter to one decimal
        
        if e.type == pygame.QUIT: run = False   # if exited, break loop
    
    if pause is True: logger.log_add("Paused", rgb.red)   # GUI logger example
    if pause is False: logger.log_add("Unpaused", rgb.lime)   # GUI logger example
    
    
    ###### --Graphics-- ######
    screen.fill((255, 255, 255))   # color screen white
    screen.blit(gui, (0, 0))   # show gui image
    screen.blit(menu, (176, 0))   # show main menu image
    grapher.draw_graph(screen, antial)   # draw graph
    
    # main screen texts
    screen.blit(fontlg.render(str(datetime.timedelta(seconds=round(counter))), True, rgb.black), (270, 5))   # counter time
    screen.blit(fontlg.render(str(round(simspeed, 2)), True, rgb.black), (288, 36))   # simulation speed
    logger.gui_logger(screen, fontsm)   # gui logger
    if welcome is True:   # if this is first time running: print welcome text in logger
        logger.log_add(str((texts_arr[0]).rstrip()), textout_color)
        logger.log_add(str((texts_arr[1]).rstrip()), textout_color)
        logger.log_add(str((texts_arr[2]).rstrip()), textout_color)
        welcome = False

    if settings is False and whelp is False and wabout is False and graph_picker is False:
        screens.main(mouse, pause, sound)   # main menu
    if settings is True:
        screens.settings(mouse, antial, sound_volume, zoom, lang)   # settings
    if graph_picker is True:
        screens.picker(mouse, texts_arr, vals, val_names, val_colors, will_rec, will_graph)   # graph value picker
    if whelp is True:
        screens.help(mouse, whelp_all, lang, texts_arr)   # help
    if wabout is True:
        screens.about(mouse, about_txt)   # about
    
    screen.blit(fontlg.render(str(mouse), True, rgb.black), (5, 695))   # show mouse coordinates
    
    pygame.display.flip()   # update screen
    clock.tick(update)   # screen update frequency
