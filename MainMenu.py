import Globals
import pygame

def Display(window, font):
    window.fill((0,0,0))
    
    mainmenuimg = pygame.image.load("./images/mainmenu.png").convert_alpha()
    mainmenuimg = pygame.transform.scale(mainmenuimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
    window.blit(mainmenuimg, (0, 0))
    
    pygame.display.update()