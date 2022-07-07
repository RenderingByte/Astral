# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to display the Options Menu.

# Imports
import Globals
import pygame

pygame.init()

def Display(window, clock, font):
    """
        Update the window to display the Options Menu.
        
        :param window: The window object (declared in Astral.py)
        :param clock: The clock object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)

    """
    
    window.fill((0,0,0))
    
    window.blit(Globals.images.optionsmenuimg, (0, 0))