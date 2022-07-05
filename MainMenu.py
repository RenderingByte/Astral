# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to display the Main Menu.

# Imports
import Globals
import pygame
import random
import os
from pyfader import IFader

pygame.init()

img = IFader("","./images/icon.png")

def Display(window, clock, font):
    """
        Update the window to display the Main Menu.
        
        :param window: The window object (declared in Astral.py)
        :param clock: The clock object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)

    """
    
    # Just loaded main menu
    if not pygame.mixer.music.get_busy():
        
        # Load the image
        img.fadeIn(1000)
        
        # Play a random song from map directory.
        Globals.mainmenu.songtitle = random.choice(os.listdir("./maps/"))
        Globals.sounds.menumusicsound = pygame.mixer.Sound("./maps/" + Globals.mainmenu.songtitle + "/audio.mp3")
        pygame.mixer.music.load("./maps/" + Globals.mainmenu.songtitle + "/audio.mp3")
        pygame.mixer.music.set_volume(Globals.options.options["musicvolume"])
        pygame.mixer.music.play()
    
    img.fadeOut(5)
    completed_logo_animation = img.draw(window, (Globals.options.options["screen_width"]/2 - 490, Globals.options.options["screen_height"]/2 - 490))
    
    if completed_logo_animation:
        
        # Display background image
        mainmenuimg = pygame.image.load("./images/mainmenu.png").convert_alpha()
        mainmenuimg = pygame.transform.scale(mainmenuimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
        window.blit(mainmenuimg, (0, 0))
    
        # Display the title of the song
        min, sec = divmod(int(Globals.sounds.menumusicsound.get_length()) - int(pygame.mixer.music.get_pos()/1000), 60)
        hour, min = divmod(min, 60)
        hour, min, sec = str(hour), str(min), str(sec)
        timeleft = min.zfill(2)+":"+sec.zfill(2)
        if int(hour) > 0: hour.zfill(2)+":"+min.zfill(2)+":"+sec.zfill(2)
        songtitle = font.render(str(Globals.mainmenu.songtitle.split("-")[0] + " (" + timeleft + ")"), True, pygame.Color("white"))
        window.blit(songtitle, (Globals.options.options["screen_width"]*0.01, Globals.options.options["screen_height"]/1.08))

        # Display song progress background
        pygame.draw.rect(window, pygame.Color("#101010"), (Globals.options.options["songprogresspos"][0], Globals.options.options["songprogresspos"][1], Globals.options.options["screen_width"], Globals.options.options["songprogresssize"][1]))
        
        # Display song progress
        timepercent = 100 * ((pygame.mixer.music.get_pos()/1000) + Globals.options.options["audiooffset"]) / Globals.sounds.menumusicsound.get_length()
        pygame.draw.rect(window, pygame.Color(Globals.options.options["songprogresscolour"]), (Globals.options.options["songprogresspos"][0], Globals.options.options["songprogresspos"][1], timepercent * (Globals.options.options["songprogresssize"][0]/100), Globals.options.options["songprogresssize"][1]))

    pygame.display.update()