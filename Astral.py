# Environment
from os import environ, system
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Imports
import pygame
import pygame_gui
import requests
import MainMenu
import OptionsMenu
import SongSelect
import Engine
import PlayField
import Globals
from pygame.locals import *

# Initialization
pygame.init()
pygame.mixer.init()
pygame.key.set_repeat()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# Window
window = pygame.display.set_mode((Globals.options.options["screen_width"], Globals.options.options["screen_height"]), (FULLSCREEN | DOUBLEBUF if Globals.options.options["fullscreen"] else DOUBLEBUF), 24)
pygame.display.set_caption("Astral")
pygame.display.set_icon(pygame.image.load('./images/icon.png'))
clock = pygame.time.Clock()
font = pygame.font.Font("./fonts/" + Globals.options.options["fontname"], Globals.options.options["fontsize"])

# Sounds
Globals.sounds.hitsound = pygame.mixer.Sound("./skins/" + Globals.options.options["skin"] + "/sounds/hitsound.mp3")
Globals.sounds.misssound = pygame.mixer.Sound("./skins/" + Globals.options.options["skin"] + "/sounds/misssound.mp3")
pygame.mixer.Sound.set_volume(Globals.sounds.hitsound, Globals.options.options["soundvolume"])
pygame.mixer.Sound.set_volume(Globals.sounds.misssound, Globals.options.options["soundvolume"])

if __name__ == "__main__":
    
    
    # Check for updates
    # https://raw.githubusercontent.com/RenderingByte/Astral/installer/ver.txt

    req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/ver.txt")
    cloudver = float(req.text)
    
    if cloudver > float(Globals.clientversion):
        
        print("There is a new version of Astral available!")
        
        req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/InstallAstral.bat", allow_redirects=True)
        open('InstallAstral.bat', 'wb').write(req.content)
        
        system("start InstallAstral.bat")
        exit()
        
    elif cloudver == float(Globals.clientversion):
        print("Astral is running the latest version.")
    else:
        print("version comp error")
        exit()
    
    
    map = None
    currenttime = 0
    keycount = None

    while 1:
        
        window.fill((0,0,0))
        for event in pygame.event.get():
            
            Globals.ui.manager.process_events(event)
            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == Globals.ui.songselectlist:
                    
                    data = Engine.load("./maps/" + Globals.ui.songselectlist.get_single_selection() + "/beatmap.json", False)
                    pygame.mixer.music.load("./maps/" + Globals.ui.songselectlist.get_single_selection() + "/audio.mp3")
                    pygame.mixer.music.play(start=(data["previewTime"]/1000))
                    
            if event.type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
              if event.ui_element == Globals.ui.songselectlist:
                if Globals.mapinfo.map == None:
                    pygame.mixer.music.stop()
                    Globals.mapinfo.map = Globals.ui.songselectlist.get_single_selection()
                    Globals.states.isselecting = False
                    Globals.states.isplaying = True
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if Globals.states.inmenu:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_RETURN:
                        Globals.states.inmenu = False
                        Globals.states.isselecting = True
                    elif event.key == pygame.K_RSHIFT:
                        Globals.states.inmenu = False
                        Globals.states.inoptions = True
                elif Globals.states.inoptions:
                    if event.key == pygame.K_ESCAPE:
                        Globals.states.inmenu = True
                        Globals.states.inoptions = False
                elif Globals.states.isselecting:
                    if event.key == pygame.K_ESCAPE:
                        Globals.states.inmenu = True
                        Globals.states.isselecting = False
                elif Globals.states.failed:
                    if event.key == pygame.K_RETURN:
                        Globals.states.isselecting = True
                        Globals.states.failed = False
                elif Globals.states.isplaying:
                    if event.key == pygame.K_ESCAPE:
                        Globals.stats.hp = 0
                    else:
                        for key in Globals.receptors:
                            if event.key == key.keybind:
                                pygame.mixer.Channel(0).play(Globals.sounds.hitsound)
        
        ''' DEBUG FOR SPECIFIC SONGS
        if not Globals.states.inmap:
            map, keycount = PlayField.LoadMap("Sugar Loli - x1.2")
            pygame.mixer.music.play(start=((map[0]["time"]/1000) + Globals.options.options["audiooffset"]))
            currenttime = map[0]["time"] + Globals.options.options["visualoffset"]
            Globals.states.inmap = True
            Globals.mapinfo.map = map
        map, currenttime = PlayField.Play(window, currenttime, map, keycount, font, clock)
        '''
        
        if Globals.states.inmenu:
            MainMenu.Display(window, font)
        elif Globals.states.inoptions:
            OptionsMenu.Display(window, font)
        elif Globals.states.isselecting:
            SongSelect.Display(window, clock, font)
        elif Globals.states.isplaying:
            if not Globals.mapinfo.map == None:
                if not Globals.states.inmap:
                    map, keycount = PlayField.LoadMap(Globals.mapinfo.map)
                    if not map == None:
                        pygame.mixer.music.play(start=((map[0]["time"]/1000) + Globals.options.options["audiooffset"]))
                        currenttime = map[0]["time"] + Globals.options.options["visualoffset"]
                        Globals.states.inmap = True
                    else:
                        Globals.mapinfo.map = None
                        Globals.states.isplaying = False
                        Globals.states.isselecting = True
                        Globals.Reset(window, None)
                if not map == None: map, currenttime = PlayField.Play(window, currenttime, map, keycount, font, clock)
            else:
                print("map selection error")
                exit()