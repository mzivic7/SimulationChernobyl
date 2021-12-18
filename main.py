import pygame
import numpy as np
import math
import time
import datetime
import webbrowser

# --Todo-- #
##### recorder, show
### simstep = counter_step
### auto scale graph
######### engine
##### G - add more lines to graph
###### save, load, save on quit
######## main interface
##### second graph ?
### icon

# --Input variables-- #
version = "Pre-alpha 0.1.5"
date = "(18.12.2021)"
update = 30   # screen update frequency
simspeed = 1.0   # simulation speed multiplyer

# --Initial variables-- #
windowx, windowy = 1280, 720   # window width, window height 
graphxstart = 0   # where starts graph area on x axis
graphxlength, graphheight = 360, 180   # graph length and height
counter_step = 0.1   # simulation step size, 0.1 = 1px ###
simstep = 1   # simulation step size ###
sound_volume = 5   # initial sound volume ###
counter = 0   # simulation time
antial = False   # anti aliasing
sound = True   # sound on/off ###
pause = True   # program paused
settings = False   # are settings open
whelp = False   # help window open
whelp_all = False   # full diagram show
wabout = False   # about window open
set_exist = False   # settings file
welcome = False   # print welcome text
textoutcolor = (0,0,0)   # textout color example
textout1, textout2, textout3 = "", "", ""   # text buffer
textoutcolor1, textoutcolor2, textoutcolor3 = (0,0,0), (0,0,0), (0,0,0)   # text color buffer
memtextout = ""   # to store previous text
text_width = 60   # max text width
lang = "eng"   # simulation language
lang_num = 1   # language number in languages file

textout = "Hello!"   # textout example

# --Functions-- #
# mouseover button effect, buttons are numerated by position
def mousover(x,y,color):
    if 177 + x * 31 < mouse[0] < 177 + x * 31 + 30 and 1 + y * 31 < mouse[1] < 1 + y * 31 + 30:   # if mouse is over button:
        pygame.draw.rect(screen, color, (177 + x * 31,1 + y * 31,30,30))  # color it

# mouseover button effect, buttons are defined by coordinates
def mousover_coord(x,y,color):
    if x < mouse[0] < x + 31 and y < mouse[1] < y + 31:   # if mouse is over button:
        pygame.draw.rect(screen, color, (x , y, 30, 30))  # color it

# group of mouseover button effects
def mouseovergroup():
    # button location      main set                  settings set
    mousover(1,0,grey)   # sound switch            # - sound
    mousover(6,0,grey)   # X                       # languages
    mousover(7,0,grey)   # save                    # recording values
    mousover(8,0,grey)   # settings                # config database
    mousover(9,0,lred)   # quit                    # cancle
    mousover(0,1,grey)   # record                  # X
    mousover(1,1,grey)   # show recorded graph     # - simstep
    mousover(5,1,grey)   # simulation speed plus   # X
    mousover(6,1,grey)   # X                       # X
    mousover(7,1,grey)   # load                    # graph values
    mousover(8,1,grey)   # help                    # config encoder

# loads settings from file
def load_settings():
    setfile = open("data/settings.txt")   # open settings file
    setmatrix = setfile.readlines()   # read settings
    setfile.close()   # close file
    setmatrix = setmatrix[0]   # read first line
    setmatrix = setmatrix.split()   # convert string to list
    antial = eval(setmatrix[0])   # set antial
    sound_volume = int(setmatrix[1])   # set sound volume
    simstep = int(setmatrix[2])   # set simstep
    lang = setmatrix[3]   # set simulation language
    return antial, sound_volume, simstep, lang

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
 
# --Logger Setup-- #

# --Load database-- #

# --Load encoder-- #

# --Load settings-- #
try:
    antial, sound_volume, simstep, lang = load_settings()
    set_exist = True
except:
    setfile = open("data/settings.txt","w+")   # create settings file
    setfile.write(str(antial)+' '+str(sound_volume)+' '+str(simstep)+' '+lang+' ')   # write to settings file
    setfile.close()   # close file
    whelp = True   # Show help
    welcome = True   # print welcome text
    
# load matrices containing names, mousover and center coords for help screen
moverbox = np.loadtxt("data/coords.txt", dtype='int', delimiter=',')
rods_moverbox = np.loadtxt("data/rods_coords.txt", dtype='int', delimiter=',')
graph_names_l = np.loadtxt("txt/"+lang+"/graph_coords_l.txt", dtype=object, delimiter=',')
graph_names_r = np.loadtxt("txt/"+lang+"/graph_coords_r.txt", dtype=object, delimiter=',')
graph_names_rods = np.loadtxt("txt/"+lang+"/graph_coords_rods.txt", dtype=object, delimiter=',')
languages = np.loadtxt("txt/languages.txt", dtype='str')   # languages list

# load texts:
texts = open("txt/"+lang+"/texts.txt")   # open file containing texts
textsarr = texts.readlines()   # store them in matrix
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

# --initialize GUI-- #
pygame.init()   # initialize pygame
pygame.display.set_icon(pygame.image.load('img/icon.png'))   # set game icon
screen = pygame.display.set_mode((windowx, windowy))   # set window size
gui = pygame.image.load("img/gui.png")   # load images
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
pygame.time.set_timer(pygame.USEREVENT, int(100/simspeed))   # simulation speed

# --Colors-- #
black = (0,0,0)
grey  = (210,210,210)
llime = (140,255,140)
lred  = (255,140,140)
red   = (255,0,0)
lime  = (0,255,0)

# --Initial matrix-- #
val = np.zeros([int((graphxlength)/(counter_step*10)),4])   # graph buffer matrix ### G
val0 = np.zeros([int((graphxlength)/(counter_step*10)),2])   # graph empty matrix

# --Main loop-- #
run = True
while run:
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:   # if any key is pressed:
            # --Key setup-- #
            if e.key == pygame.K_ESCAPE: run = False  # if "escape" key is pressed, close program
            if e.key == pygame.K_p:   # if "P" key is pressed:
                if pause is False: pause = True   # if it is not paused, pause it 
                else: pause = False  # if it is paused, unpause it
                
        # -- Button engine-- #
        mouse = pygame.mouse.get_pos()   # get mouse position
        if e.type == pygame.MOUSEBUTTONDOWN:   # if mouse clicked:
            # main menu
            if settings is False and whelp is False and wabout is False:
                if 177 < mouse[0] < 207 and 1 < mouse[1] < 31:   # start /stop
                    if pause is False: pause = True    # pause
                    else: pause = False   # unpause
                    if pause is True: textout, textoutcolor = "Paused", red   # just example ###
                    if pause is False: textout, textoutcolor = "Unpaused", lime   # just example ###
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
            if settings is True  and whelp is False and wabout is False:   
                if 456 < mouse[0] < 486 and 1 < mouse[1] < 31:   # cancle settings
                    settings = False
                    antial, sound_volume, simstep, lang = load_settings()
                if 456 < mouse[0] < 486 and 32 < mouse[1] < 62:   # save settings
                    settings = False
                    setfile = open("data/settings.txt","w+")   # open settings file
                    setfile.write(str(antial)+' '+str(sound_volume)+' '+str(simstep)+' '+lang+' ')   # write to settings file
                    setfile.close()   # close file
                if 177 < mouse[0] < 207 and 1 < mouse[1] < 31:    # turn on antialias
                    if antial is False: antial = True
                    else: antial = False   # turn off antial
                if 208 < mouse[0] < 238 and 1 < mouse[1] < 31 and sound_volume > 1: sound_volume -= 1  # sound volume minus
                if 301 < mouse[0] < 331 and 1 < mouse[1] < 31 and sound_volume < 10: sound_volume += 1  # sound volume plus
                if 208 < mouse[0] < 238 and 32 < mouse[1] < 62 and simstep > 1: simstep -= 1   # simstep minus
                if 301 < mouse[0] < 331 and 32 < mouse[1] < 62 and simstep < 5: simstep += 1   # simstep plus
                if 177 < mouse[0] < 207 and 32 < mouse[1] < 62:    # languages
                    lang = languages[lang_num]
                    lang_num +=1
                    if lang_num >= len(languages): lang_num = 0
                    textout = str((textsarr[5]).rstrip())
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
                if 680 < mouse[0] < 711 and 289 < mouse[1] < 320:   # open report link
                    webbrowser.open(r"https://github.com/mzivic7/Simulation-Chernobyl/issues")
        
        # --Calculations-- #
        if e.type == pygame.USEREVENT:
            if pause is False:   # if it is not paused:
                # --Engine-- #
                
                # --Graphs-- #
                val1in = 88 + (math.sin(counter/2))*50   # set y value for val1 ### G
                val2in = 88 + (math.sin((counter/2)+(2*math.pi/3)))*50   # set y value for val2 ### G
                val3in = 88 + (math.sin((counter/2)+(4*math.pi/3)))*50   # set y value for val2 ### G
                val = np.roll(val, 1, axis=0)   # move all values in buffer
                val[:1] = np.zeros((val[:1].shape))   # one place down
                val[0,1] = windowy - val1in   # add new y to buffer val1 ### G
                val[0,2] = windowy - val2in   # add new y to buffer val2 ### G
                val[0,3] = windowy - val3in   # add new y to buffer val3 ### G
                val[0,0] = graphxstart + counter * 10   # add new x to buffer
                if counter >= (((graphxlength)/2)/5):   # if buffer overflows:
                    val[:,0] -= counter_step*10   # substract 2 from x coords
                    if counter > (((graphxlength)/2)/5): # in all next iterrations:
                        val[0,0] -= (counter * 10 - ((graphxlength)/2)*2)   # make first x constant
                counter += counter_step   # iterate counter
                counter = round(counter, 2)   # round counter to one decimal
        
        if e.type == pygame.QUIT: run = False   # if exited, break loop
    
    # --Draw lines-- #
    screen.fill((255, 255, 255))   # color screen white
    val0[:,0] = val[:,0]   # add x values to seed from buffer
    val1 = val0   # set specific line matrix ### G
    val1[:,1] = val[:,1]   # ad y to that specific line matrix from buffer ### G
    if antial is True: pygame.draw.aalines(screen, (255,0,0), False, val1, 2)   # draw graphed lines ### G
    else: pygame.draw.lines(screen, (255,0,0), False, val1, 2)   # draw graphed lines ### G
    val2 = val0   # ### G
    val2[:,1] = val[:,2]   # ### G
    if antial is True: pygame.draw.aalines(screen, (0,255,0), False, val2, 2)   # ### G
    else: pygame.draw.lines(screen, (0,255,0), False, val1, 2)   # ### G
    val3 = val0   # ### G
    val3[:,1] = val[:,3]   # ### G
    if antial is True: pygame.draw.aalines(screen, (0,0,255), False, val3, 2)   # ### G
    else: pygame.draw.lines(screen, (0,0,255), False, val1, 2)   # ### G
    
    # --Menu button style-- #
    if whelp is False and wabout is False: mouseovergroup()   # draw rectangles if mouse is over button
    if settings is False and whelp is False and wabout is False:   ## main menu ##
        mousover(2,1,grey)   # simulation speed minus
        mousover(9,1,grey)   # about
        # start/stop
        if pause is True: pygame.draw.rect(screen, llime, (177,1,30,30)) # if simulation is paused: color it
        mousover(0,0,grey) # start / stop
        if pause is True: screen.blit(runbt, (177, 1))   # if simulation is paused: show image
        else: screen.blit(stopbt, (177, 1))
        if sound is True: screen.blit(soundon, (208, 1))   #if sound is on
        else: screen.blit(soundoff, (208, 1))
    
    screen.blit(gui, (0, 0))   ## show gui image ##
    
    # --Main screen texts-- #
    screen.blit(fontlg.render(str(datetime.timedelta(seconds=round(counter))), True, black), (270, 5))   # counter text
    screen.blit(fontlg.render(str(round(simspeed, 2)), True, black), (288, 36))   # simulation speed text
    if textout != memtextout:   # if new text is sent:
        textout3, textout2, textout1 = textout2, textout1, textout   # add it to begenning, and shift others
        textoutcolor3, textoutcolor2, textoutcolor1 = textoutcolor2, textoutcolor1, textoutcolor   # same for colors
        if len(textout) > text_width:   # if text is larger than window: split it and shift again
            textout3, textout2, textout1 = textout2, textout[text_width : len(textout)], textout[0 : text_width]
            textoutcolor3, textoutcolor2, textoutcolor1 = textoutcolor2, textoutcolor, textoutcolor   # same for colors
    memtextout = textout   # update mem
    if welcome is True:
        textout1, textout2, textout3 = str((textsarr[0]).rstrip()), str((textsarr[1]).rstrip()), str((textsarr[2]).rstrip())
    screen.blit(fontsm.render(str(textout1), True, textoutcolor1), (363, 669))   # text output line 1
    screen.blit(fontsm.render(str(textout2), True, textoutcolor2), (363, 684))   # text output line 2
    screen.blit(fontsm.render(str(textout3), True, textoutcolor3), (363, 699))   # text output line 3
    
    # --Settings-- #
    if settings is True  and whelp is False and wabout is False:   ## settings ##
        pygame.draw.rect(screen, (255,255,255), (177,1,309,61))   # settings overlay
        mouseovergroup()
        if antial is True: pygame.draw.rect(screen, llime, (177,1,30,30))
        mousover(1,0,grey)   # - sound
        mousover(0,0,grey)   # anti aliasing
        mousover(4,0,grey)   # + sound
        mousover(5,0,grey)   # X
        mousover(4,1,grey)   # + simstep
        mousover(9,1,llime)   # save
        screen.blit(setmenu, (177, 1))   # show settings
        screen.blit(fontlg.render("V:" + str(sound_volume), True, black), (248, 6))   # simulation speed text
        screen.blit(fontlg.render("S:" + str(simstep), True, black), (248, 37))   # simulation step text
        screen.blit(fontsm.render(lang, True, black), (180, 37))   # languages
        
    # --Help-- #
    if whelp is True:
        mousover(0,0,grey)   # back button
        screen.blit(back, (176, 0))   # back button
        screen.blit(help_graph_all, (208, 1))   # help diagram button
        pygame.draw.rect(screen, (255,255,255), (177,271,109,267))   # hide part of left imputs
        pygame.draw.rect(screen, (255,255,255), (1,539,360,180))   # hide graph
        pygame.draw.line(screen, black, (176, 271), (176, 537))   # draw border over that hidden part
        screen.blit(rods_help, (294, 549))   # rods help picture
        screen.blit(fontlg.render(str((textsarr[4]).rstrip()), True, black), (5,543))   # inside core text
        if whelp_all is False:
            mousover(1,0,grey)   # help diagram button
            screen.blit(help_graph_all, (208, 1))   # help diagram button
            pygame.draw.rect(screen, (255,255,255), (1104,1,175,718))   # hide inputs
            screen.blit(help_gui, (1107,4))   # show gui help 
            screen.blit(fontsm.render(lang, True, black), (1111, 599))   # add language name to gui help
            for line_num, lines in enumerate(gui_explarr):   # for each line in gui explanations:
                # print that line in new row
                screen.blit(fontsm.render(str((gui_explarr[line_num]).rstrip()), True, black), (1145, int(4+(line_num*15.5))))
            text_wrap(screen, str((textsarr[3]).rstrip()), (5 ,5, 177, 530), fontsm, fontsm, black)   # explanation text
            for line_num, lines in enumerate(moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    pygame.draw.line(screen, black, (165, 75), (190, 75))   # draw straight line
                    pygame.draw.line(screen, black, (190, 75), (lines[4], lines[5]))   # draw line conecting box
                    pygame.draw.rect(screen, black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)  # draw outline
                    text_wrap(screen, str((explarr[line_num]).rstrip()), (5 ,67, 172, 530),fontsm, fontsb, black)   # print text
            for line_num, lines in enumerate(rods_moverbox):   # for every line in file: (line contains coords of box)
                if lines[0] < mouse[0] < lines[2] + 1 and lines[1] < mouse[1] < lines[3] + 1:   # if mouse is over it
                    pygame.draw.rect(screen, black, (lines[0],lines[1],lines[2]-lines[0]+1,lines[3]-lines[1]+1), 1)  # draw outline
                    text_wrap(screen, str((rods_explarr[line_num]).rstrip()), (5 ,565, 285, 720),fontsm, fontsb, black)  # print txt
                        
        if whelp_all is True:   # if all help is true:
            text_lines(screen, graph_names_l[:,6], (5,5,172,520), fontsb, 6)   # left all help
            connect_lines(screen, graph_names_l, (177, 2, 22))   # draw lines connecting left text to elements
            text_lines(screen, graph_names_r[:,6], (1110,5,1280,520), fontsb, 6)   # right all help
            connect_lines(screen, graph_names_r, (1103, 2, 22))   # draw lines connecting right text to elements
            text_lines(screen, graph_names_rods[:,6], (5,565,172,520), fontsb, 6)   # rods all help
            connect_lines(screen, graph_names_rods, (177, 562, 22))   # draw lines connecting right text to elements
            pygame.draw.line(screen, black, (176, 538), (176, 719))   # names border extended line

    # --About-- #
    if wabout is True:
        pygame.draw.rect(screen, (255,255,255), (1,1,windowx-2,windowy-2))   # blank screen
        mousover_coord(625, 16, grey)
        screen.blit(back, (624, 15))   # back button
        text_lines(screen, about_txt, (529,60,800,500), fontxl, 10)   # show about text
        mousover_coord(680, 222, grey)
        mousover_coord(680, 256, grey)
        mousover_coord(680, 290, grey)
        screen.blit(link, (679, 221))   # github button
        screen.blit(link, (679, 255))   # wiki button
        screen.blit(link, (679, 289))   # report bug button
    
    
    screen.blit(fontlg.render(str(mouse), True, black), (5, 695))   # show mouse coordinates
    pygame.display.flip()   # update screen
    clock.tick(update)   # screen update frequency
