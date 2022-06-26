import Globals
import pygame
import pygame_gui

def Display(window, font):
    
    window.fill((0,0,0))
    
    optionsimg = pygame.image.load("./images/optionsmenu.png").convert_alpha()
    optionsimg = pygame.transform.scale(optionsimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
    window.blit(optionsimg, (0, 0))
    
    
    
    pygame.display.update()