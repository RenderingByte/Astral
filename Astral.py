# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as the entry point for the application.

# Environment
from os import environ as env
env['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Imports
import Globals
import MainMenu
import OptionsMenu
import SongSelect
import PlayField
import Engine
import pygame
import pygame_gui
from pygame.locals import *

# Pygame Initialization
pygame.init()
pygame.mixer.init()
pygame.key.set_repeat()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

# Window Setup
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

# Application Entry Point
if __name__ == "__main__":
    
    print("This program is still in development. Please expect and report any bugs to Byte#4174, or on the GitHub page.")
    print("Maps with SV Changes will have incorrect timing. SV's aren't even implemented anyways, so there should be no reason for you to be playing these maps.")
    print("Some regular maps may be out of sync as well, but this should be rare.")
    Globals.CheckForUpdates()

    # Window Loop
    while 1:
        
        window.fill((0,0,0))
        
        # Pygame Events are captured here
        for event in pygame.event.get():
            
            # Exit Event
            if event.type == pygame.QUIT: pygame.quit(); exit()
            
            # Capture UI Events
            Globals.ui.manager.process_events(event)
            
            # -> Selection Lists
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
            
            # Handle Keypresses
            if event.type == pygame.KEYDOWN:
                if Globals.states.inmenu:
                    if event.key == pygame.K_ESCAPE: pygame.quit(); exit()
                        
                    elif event.key == pygame.K_RETURN:
                        
                        pygame.mixer.music.stop()
                        Globals.states.inmenu = False
                        Globals.states.isselecting = True
                        
                    elif event.key == pygame.K_TAB:
                        
                        pygame.mixer.music.stop()
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
                        
                        Globals.Reset(window, None)
                        
                    else:
                        
                        # Play Hitsound
                        for key in Globals.receptors:
                            if event.key == key.keybind: pygame.mixer.Channel(0).play(Globals.sounds.hitsound)
        
        if Globals.states.inmenu:
            
            MainMenu.Display(window, clock, font)
            
        elif Globals.states.inoptions:
            
            OptionsMenu.Display(window, clock, font)
            
        elif Globals.states.isselecting:
            
            SongSelect.Display(window, clock, font)
            
        elif Globals.states.isplaying:
            if not Globals.mapinfo.map == None:
                if not Globals.states.inmap:
                    
                    audio, visual = PlayField.LoadMap(Globals.mapinfo.map)
                    
                    if not Globals.mapinfo.playingmap == None:
                        
                        pygame.mixer.music.play(start=(audio))
                        Globals.mapinfo.currenttime = visual
                        Globals.states.inmap = True
                        
                    else:
                        
                        Globals.mapinfo.map = None
                        Globals.states.isplaying = False
                        Globals.states.isselecting = True
                        Globals.Reset(window, None)
                        
                if not Globals.mapinfo.playingmap == None: PlayField.Play(window, font, clock)
                
            else:
                
                print(Globals.mapinfo.map)
                print("map selection error")
                pygame.quit(); exit()