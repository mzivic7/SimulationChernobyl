import pygame
import numpy as np
import math
import time
import datetime
import webbrowser

from simulation_chernobyl import graphics
from simulation_chernobyl import fileops

logger = graphics.Logger()
grapher = graphics.Grapher()



# --Todo-- #
####### graph support n lines
##### pick lines to be added to graph
##### second graph
##### recorder, show
### auto scale graph
### zoom graph

######### engine
######## main interface
###### save, load, save on quit
### icon



###### --Input variables-- ######
version = "Pre-alpha 0.1.6"
date = "(20.1.2022)"

update = 30   # screen update frequency
windowx, windowy = 1280, 720   # window width, window height 



###### --Initial variables-- ######
simspeed = 1.0   # simulation speed multiplyer
sound_volume = 5   # initial sound volume
zoom = 1   # graph zoom
counter_step = 0.1   # simulation step size
counter = 0   # simulation time

antial = False   # anti aliasing
sound = True   # sound on/off ###
pause = True   # program paused
settings = False   # are settings open
whelp = False   # help window open
whelp_all = False   # full diagram show
wabout = False   # about window open
welcome = False   # print welcome text

textout_color = (0,0,0)   # initial text color
logger.gui_max_width(60)   # max text width

lang = "eng"   # simulation language
lang_num = 1   # index of language in use

grapher.graph_dim(0, 538, 360, 718, counter_step)   # grapher dimensions



###### --Logger Setup-- ######

###### --Load database-- ######

###### --Load encoder-- ######

###### --Load settings-- ######
try:
    antial, sound_volume, zoom, lang = fileops.load_settings()   # try to load settings from file
except:
    setfile = open("data/settings.txt","w+")   # create settings file
    setfile.write(str(antial)+' '+str(sound_volume)+' '+str(zoom)+' '+lang+' ')   # write to settings file
    setfile.close()   # close file
    whelp = True   # Show help
    welcome = True   # print welcome text

# load matrices containing names, mouseover and center coords for help screen
moverbox = np.loadtxt("data/coords.txt", dtype='int', delimiter=',')
rods_moverbox = np.loadtxt("data/rods_coords.txt", dtype='int', delimiter=',')
graph_names_l = np.loadtxt("txt/"+lang+"/graph_coords_l.txt", dtype=object, delimiter=',')
graph_names_r = np.loadtxt("txt/"+lang+"/graph_coords_r.txt", dtype=object, delimiter=',')
graph_names_rods = np.loadtxt("txt/"+lang+"/graph_coords_rods.txt", dtype=object, delimiter=',')
languages = np.loadtxt("txt/languages.txt", dtype='str')   # languages list

# load texts:
texts = open("txt/"+lang+"/texts.txt")   # open file containing texts
texts_arr = texts.readlines()   # store them in matrix
texts.close()   # close file
expl = open("txt/"+lang+"/expl.txt")   # open file containing explanations
explarr = expl.readlines()   # store them in matrix
expl.close()   # close file
gui_expl = open("txt/"+lang+"/gui_expl.txt")   # open file containing gui explanations
gui_explarr = gui_expl.readlines()   # store them in matrix
gui_expl.close()   # close file
rods_expl = open("txt/"+lang+"/rods_expl.txt")   # open file containing rods explanations
rods_explarr = rods_expl.readlines()   # store them in matrix
rods_expl.close()   # close file
fabout_txt= open("txt/"+lang+"/about.txt")   # open file containing about text
about_txt = fabout_txt.readlines()   # store it in matrix
fabout_txt.close()   # close file
about_txt[0] = about_txt[0].rstrip() + " " + version
about_txt[1] = date



###### --initialize GUI-- ######
pygame.init()   # initialize pygame
pygame.display.set_icon(pygame.image.load('img/icon.png'))   # set game icon
screen = pygame.display.set_mode((windowx, windowy))   # set window size
gui = pygame.image.load("img/gui.png")   # load images
menu = pygame.image.load("img/menu.png")
setmenu = pygame.image.load("img/settings.png")
runbt = pygame.image.load("img/run.png")
stopbt = pygame.image.load("img/stop.png")
soundon = pygame.image.load("img/sound.png")
soundoff = pygame.image.load("img/mute.png")
help_gui = pygame.image.load("img/help_gui.png")
back = pygame.image.load("img/back.png")
help_graph_all = pygame.image.load("img/help_all.png")
rods_help = pygame.image.load("img/rods.png")
link = pygame.image.load("img/link.png")
fontlg = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 18)   # large text font
fontsm = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 15)   # small text font
fontxl = pygame.font.Font("txt/fonts/LiberationSans-Regular.ttf", 20)   # extra large text font
fontsb = pygame.font.Font("txt/fonts/LiberationSans-Bold.ttf", 14)   # small bold text font
clock = pygame.time.Clock()   # start clock
# how many times calculations event is repeated in one iterration of main loop
pygame.time.set_timer(pygame.USEREVENT, int(100/simspeed))

# colors
black = (0,0,0)
grey  = (210,210,210)
llime = (140,255,140)
lred  = (255,140,140)
red   = (255,0,0)
lime  = (0,255,0)

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
            if settings is False and whelp is False and wabout is False:
                if 177 < mouse[0] < 207 and 1 < mouse[1] < 31:   # start /stop
                    if pause is False: pause = True    # pause
                    else: pause = False   # unpause
                    if pause is True: logger.log_add("Paused", red)   # just example ###
                    if pause is False: logger.log_add("Unpaused", lime)   # just example ###
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
                if 425 < mouse[0] < 455 and 32 < mouse[1] < 62: whelp, pause = True, True   # switch to help
                if 456 < mouse[0] < 486 and 32 < mouse[1] < 62: wabout, pause = True, True   # switch to about
                if 456 < mouse[0] < 486 and 1 < mouse[1] < 31: run = False   # quit
                    #### exit ask to save
                    
            # settings
            if settings is True and whelp is False and wabout is False:   
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
                    lang_num +=1   # itterate over languages
                    if lang_num >= len(languages): lang_num = 0   # rotate lang num
                    logger.log_add(str((texts_arr[5]).rstrip()), black)   # print that simulation must restart
                    
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

                in1 = 88 + (math.sin(counter/2))*50
                in2 = 88 + (math.sin((counter/2)+(2*math.pi/3)))*50
                in3 = 88 + (math.sin((counter/2)+(4*math.pi/3)))*50
                
                grapher.add_val(counter, in1, in2, in3)   # add values to graph
                counter += counter_step   # iterate counter
                counter = round(counter, 2)   # round counter to one decimal
        
        if e.type == pygame.QUIT: run = False   # if exited, break loop
    
    
    ###### --Graphics-- ######
    screen.fill((255, 255, 255))   # color screen white
    screen.blit(gui, (0, 0))   # show gui image
    screen.blit(menu, (176, 0))   # show main menu image
    grapher.draw_graph(screen, antial)   # draw graph
    
    # main screen texts
    screen.blit(fontlg.render(str(datetime.timedelta(seconds=round(counter))), True, black), (270, 5))   # counter time
    screen.blit(fontlg.render(str(round(simspeed, 2)), True, black), (288, 36))   # simulation speed
    logger.gui_logger(screen, fontsm)   # gui logger
    if welcome is True:   # if this is first time running: print welcome text in logger
        logger.log_add(str((texts_arr[0]).rstrip()), textout_color)
        logger.log_add(str((texts_arr[1]).rstrip()), textout_color)
        logger.log_add(str((texts_arr[2]).rstrip()), textout_color)
        welcome = False

    # main menu
    if whelp is False and wabout is False: graphics.mouseover_group(screen, mouse)   # draw rectangles if mouse is over button
    if settings is False and whelp is False and wabout is False:   ## main menu ##
        graphics.mouseover(screen, 2, 1, grey, mouse)   # simulation speed minus
        graphics.mouseover(screen, 9, 1, grey, mouse)   # about
        # start/stop
        if pause is True: pygame.draw.rect(screen, llime, (177,1,30,30)) # if simulation is paused: color it
        graphics.mouseover(screen, 0, 0, grey, mouse) # start / stop
        if pause is True: screen.blit(runbt, (177, 1))   # if simulation is paused: show image
        else: screen.blit(stopbt, (177, 1))
        if sound is True: screen.blit(soundon, (208, 1))   # if sound is on
        else: screen.blit(soundoff, (208, 1))
        screen.blit(menu, (176, 0))      # show main menu image again because of mouseover effects
    
    # settings menu
    if settings is True and whelp is False and wabout is False:   ## settings ##
        pygame.draw.rect(screen, (255,255,255), (177,1,309,61))   # settings overlay
        graphics.mouseover_group(screen, mouse)   # mouseover effects for main menu
        if antial is True: pygame.draw.rect(screen, llime, (177,1,30,30))
        graphics.mouseover(screen, 1, 0, grey, mouse)   # - sound
        graphics.mouseover(screen, 0, 0, grey, mouse)   # anti aliasing
        graphics.mouseover(screen, 4, 0, grey, mouse)   # + sound
        graphics.mouseover(screen, 5, 0, grey, mouse)   # X
        graphics.mouseover(screen, 4, 1, grey, mouse)   # + zoom
        graphics.mouseover(screen, 9, 1, llime, mouse)   # save
        screen.blit(setmenu, (177, 1))   # show settings
        screen.blit(fontlg.render("V:" + str(sound_volume), True, black), (248, 6))   # sound volume text
        screen.blit(fontlg.render("Z:" + str(zoom), True, black), (248, 37))   # graph zoom text
        screen.blit(fontsm.render(lang, True, black), (180, 37))   # languages
        
    # help menu
    if whelp is True:
        graphics.mouseover(screen, 0, 0, grey, mouse)   # back button
        screen.blit(back, (176, 0))   # back button
        graphics.mouseover(screen, 8, 1, llime, (426, 33))   # make help button lime
        screen.blit(menu, (176, 0))      # show main menu image again because of mouseover effects
        screen.blit(help_graph_all, (208, 1))   # all help diagram button
        pygame.draw.rect(screen, (255,255,255), (177,271,109,267))   # hide part of left imputs
        pygame.draw.rect(screen, (255,255,255), (1,539,360,180))   # hide graph
        pygame.draw.line(screen, black, (176, 271), (176, 537))   # draw border over that hidden part
        pygame.draw.rect(screen, (255,255,255), (1104,1,175,718))   # hide right inputs
        screen.blit(rods_help, (294, 549))   # rods help picture
        screen.blit(fontlg.render(str((texts_arr[4]).rstrip()), True, black), (5,543))   # inside core text
        if whelp_all is False:
            graphics.mouseover(screen, 1, 0, grey, mouse)   # help diagram button
            screen.blit(help_graph_all, (208, 1))   # help diagram button
            screen.blit(help_gui, (1107,4))   # show gui help 
            screen.blit(fontsm.render(lang, True, black), (1111, 599))   # add language name to gui help
            for line_num, lines in enumerate(gui_explarr):   # for each line in gui explanations:
                # print that line in new row
                screen.blit(fontsm.render(str((gui_explarr[line_num]).rstrip()), True, black), (1145, int(4+(line_num*15.5))))
            graphics.text_wrap(screen, str((texts_arr[3]).rstrip()), (5 ,5, 177, 530), fontsm, fontsm, black)   # explanation text
            for line_num, lines in enumerate(moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    pygame.draw.line(screen, black, (165, 75), (190, 75))   # draw straight line
                    pygame.draw.line(screen, black, (190, 75), (lines[4], lines[5]))   # draw line conecting box
                    pygame.draw.rect(screen, black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)  # draw outline
                    graphics.text_wrap(screen, str((explarr[line_num]).rstrip()), (5 ,67, 172, 530),fontsm, fontsb, black)   # print text
            for line_num, lines in enumerate(rods_moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    pygame.draw.rect(screen, black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)  # draw outline
                    graphics.text_wrap(screen, str((rods_explarr[line_num]).rstrip()), (5 ,565, 285, 720),fontsm, fontsb, black)  # print text
                        
        if whelp_all is True:   # if all help is true:
            graphics.mouseover(screen, 1, 0, llime, (209, 2))   # make all_help button lime
            screen.blit(help_graph_all, (208, 1))   # show all_help buton again
            graphics.text_lines(screen, graph_names_l[:,6], (5,5,172,520), fontsb, 6)   # left all help
            graphics.connect_lines(screen, graph_names_l, (177, 2, 22))   # draw lines connecting left text to elements
            graphics.text_lines(screen, graph_names_r[:,6], (1110,5,1280,520), fontsb, 6)   # right all help
            graphics.connect_lines(screen, graph_names_r, (1103, 2, 22))   # draw lines connecting right text to elements
            graphics.text_lines(screen, graph_names_rods[:,6], (5,565,172,520), fontsb, 6)   # rods all help
            graphics.connect_lines(screen, graph_names_rods, (177, 562, 22))   # draw lines connecting rods text to elements
            pygame.draw.line(screen, black, (176, 538), (176, 719))   # names border extended line
    
    # about menu
    if wabout is True:
        pygame.draw.rect(screen, (255,255,255), (1,1,windowx-2,windowy-2))   # blank screen
        graphics.mouseover_coord(screen, 625, 16, grey, mouse)   # back button mouseover effect
        screen.blit(back, (624, 15))   # back button
        graphics.text_lines(screen, about_txt, (529,60,800,500), fontxl, 10)   # show about text
        graphics.mouseover_coord(screen, 680, 222, grey, mouse)
        graphics.mouseover_coord(screen, 680, 256, grey, mouse)
        graphics.mouseover_coord(screen, 680, 290, grey, mouse)
        screen.blit(link, (679, 221))   # github button
        screen.blit(link, (679, 255))   # wiki button
        screen.blit(link, (679, 289))   # report bug button
    
    screen.blit(fontlg.render(str(mouse), True, black), (5, 695))   # show mouse coordinates ###
    pygame.display.flip()   # update screen
    clock.tick(update)   # screen update frequency
