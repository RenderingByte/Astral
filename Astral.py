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
pygame.display.set_icon(pygame.image.load('./images/icon_transparent.png'))
clock = pygame.time.Clock()
font = pygame.font.Font("./fonts/" + Globals.options.options["fontname"], Globals.options.options["fontsize"])

# Sounds
Globals.sounds.hitsound = pygame.mixer.Sound("./skins/" + Globals.options.options["skin"] + "/sounds/hitsound.mp3")
Globals.sounds.misssound = pygame.mixer.Sound("./skins/" + Globals.options.options["skin"] + "/sounds/misssound.mp3")
pygame.mixer.Sound.set_volume(Globals.sounds.hitsound, Globals.options.options["soundvolume"])
pygame.mixer.Sound.set_volume(Globals.sounds.misssound, Globals.options.options["soundvolume"])

# Images
Globals.images.mainmenuimg = pygame.image.load("./images/mainmenu.png").convert_alpha()
Globals.images.mainmenuimg = pygame.transform.scale(Globals.images.mainmenuimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
Globals.images.optionsmenuimg = pygame.image.load("./images/optionsmenu.png").convert_alpha()
Globals.images.optionsmenuimg = pygame.transform.scale(Globals.images.optionsmenuimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
Globals.images.songselectmenuimg = pygame.image.load("./images/songselect.png").convert_alpha()
Globals.images.songselectmenuimg = pygame.transform.scale(Globals.images.songselectmenuimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
Globals.images.playfieldimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/playfield.png").convert_alpha()
Globals.images.playfieldimg = pygame.transform.scale(Globals.images.playfieldimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
Globals.images.marvimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/marvelous.png").convert_alpha()
Globals.images.marvimg = pygame.transform.scale(Globals.images.marvimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.perfimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/perfect.png").convert_alpha()
Globals.images.perfimg = pygame.transform.scale(Globals.images.perfimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.greatimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/great.png").convert_alpha()
Globals.images.greatimg = pygame.transform.scale(Globals.images.greatimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.goodimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/good.png").convert_alpha()
Globals.images.goodimg = pygame.transform.scale(Globals.images.goodimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.badimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/bad.png").convert_alpha()
Globals.images.badimg = pygame.transform.scale(Globals.images.badimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.missimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/miss.png").convert_alpha()
Globals.images.missimg = pygame.transform.scale(Globals.images.missimg, (Globals.options.options["judgementsize"][0], Globals.options.options["judgementsize"][1]))
Globals.images.failimg = pygame.image.load("./images/fail.png").convert_alpha()
Globals.images.failimg = pygame.transform.scale(Globals.images.failimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
Globals.images.passimg = pygame.image.load("./images/pass.png").convert_alpha()
Globals.images.passimg = pygame.transform.scale(Globals.images.passimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))

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
                    
                    try:
                        pygame.mixer.music.load("./maps/" + Globals.ui.songselectlist.get_single_selection() + "/audio.mp3")
                        pygame.mixer.music.play(start=(data["previewTime"]/1000))
                    except:
                        print("Song failed to load due to an error.")
                        break
                    
                    Globals.mainmenu.selectedsong = data    
                            
            if event.type == pygame_gui.UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION:
                if event.ui_element == Globals.ui.songselectlist:
                    if Globals.mapinfo.map == None:
                        
                        pygame.mixer.music.stop()
                        
                        if not Globals.ui.songselectlist.get_single_selection() == None:
                            
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
                        
                elif Globals.states.showresults:
                    if event.key == pygame.K_RETURN:
                        
                        Globals.ui.songselectlist.enable()
                        Globals.states.isselecting = True
                        Globals.states.showresults = False
                        
                elif Globals.states.isplaying:
                    if event.key == pygame.K_ESCAPE:
                        
                        Globals.ui.songselectlist.enable()
                        Globals.Reset(window, None, False)
                        
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
            if not Globals.states.inmap:
                
                audio, visual = PlayField.LoadMap(Globals.mapinfo.map)
                
                if audio == None or visual == None:
                    
                    Globals.Reset(window, None, False)
                    Globals.states.isselecting = True
                    Globals.states.isplaying = False
                    Globals.mapinfo.map = None
                
                else:
                
                    if not Globals.mapinfo.playingmap == None:
                        
                        pygame.mixer.music.play(start=(audio))
                        Globals.mapinfo.currenttime = visual
                        Globals.ui.songselectlist.disable()
                        Globals.states.inmap = True
                        
                    else:
                        
                        Globals.mapinfo.map = None
                        Globals.states.isplaying = False
                        Globals.states.isselecting = True
                        Globals.Reset(window, None, False)
                
            # Remove if, push up one indentation level??
            if not Globals.mapinfo.playingmap == None and not Globals.states.showresults: PlayField.Play(window, font, clock)