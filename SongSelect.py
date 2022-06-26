import Globals
import pygame
import pygame_gui
import os

def Display(window, clock, font):
    
    window.fill((0,0,0))
    
    songselectimg = pygame.image.load("./images/songselect.png").convert_alpha()
    songselectimg = pygame.transform.scale(songselectimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
    window.blit(songselectimg, (0, 0))
    
    if not Globals.loadedmaps.loadedlist and len(Globals.loadedmaps.maparray) == 0:
        
        def LoadMaps(amt):
            
            print("Counting beatmaps...")

            for filename in os.listdir("./maps/"):
                path = os.path.join("./maps/", filename)
                if os.path.isfile(path + "/beatmap.json"):        
                    
                    Globals.loadedmaps.maparray.append(filename)
                    
                    if not amt == None:
                        if len(Globals.loadedmaps.maparray) >= amt: break
            
            print("Counted " + str(len(Globals.loadedmaps.maparray)) + " beatmaps.")
            
        LoadMaps(Globals.options.options["mapstoload"])
        Globals.loadedmaps.loadedlist = True
    
    elif not Globals.loadedmaps.drewlist:
        Globals.loadedmaps.drewlist = True
        Globals.ui.songselectlist = pygame_gui.elements.UISelectionList(pygame.Rect((Globals.options.options["screen_width"] - (Globals.options.options["screen_width"]/6), 0), (Globals.options.options["screen_width"]/6, Globals.options.options["screen_height"])), item_list=Globals.loadedmaps.maparray, manager=Globals.ui.manager)
        Globals.ui.songselectlist.scroll_bar_width = 10
        Globals.ui.songselectlist.list_item_height = 50
        
    dtforui = clock.tick(Globals.options.options["fps"])/1000.0
    Globals.ui.manager.update(dtforui)
    Globals.ui.manager.draw_ui(window)
    pygame.display.update()