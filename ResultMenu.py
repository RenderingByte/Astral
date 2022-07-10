# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to display the results screen.

# Imports
import Globals
import pygame

pygame.init()

def Display(window, clock, font):
    """
        Update the window to display the Result Menu.
        
        :param window: The window object (declared in Astral.py)
        :param clock: The clock object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)

    """

    if Globals.states.showfailed:
        if not pygame.mixer.Channel(3).get_busy(): pygame.mixer.Channel(3).play(Globals.sounds.failsound)
        window.blit(Globals.images.failimg, (0, 0))
    else:
        if not pygame.mixer.Channel(3).get_busy(): pygame.mixer.Channel(3).play(Globals.sounds.passsound)
        window.blit(Globals.images.passimg, (0, 0))