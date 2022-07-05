# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to display the Song Select Menu.

# Imports
import Globals
import pygame
import pygame_gui
import os

def LoadMaps(amt):
    """
        Load maps into the Globals.loadedmaps.maparray array.
        Used for Song Select List.
        
        :param amt: The amount of maps to load. (None = All)

    """
    
    print("Counting beatmaps...")

    for filename in os.listdir("./maps/"):
        
        path = os.path.join("./maps/", filename)
        
        if os.path.isfile(path + "/beatmap.json"):        
            
            Globals.loadedmaps.maparray.append(filename)
            
            if not amt == None:
                if len(Globals.loadedmaps.maparray) >= amt: break
    
    print("Counted " + str(len(Globals.loadedmaps.maparray)) + " beatmaps.")

def Display(window, clock, font):
    """
        Update the window to display the Song Select Menu.
        
        :param window: The window object (declared in Astral.py)
        :param clock: The clock object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)

    """
    
    
    # First Load
    if not Globals.loadedmaps.loadedlist and len(Globals.loadedmaps.maparray) == 0:
 
        LoadMaps(Globals.options.options["mapstoload"])
        Globals.loadedmaps.loadedlist = True
    
    # Maps loaded, but not rendered.
    elif not Globals.loadedmaps.drewlist:
        
        Globals.ui.searchbox = pygame_gui.elements.UITextEntryLine(pygame.Rect((0, 0), (Globals.options.options["screen_width"], Globals.options.options["fontsize"])), manager=Globals.ui.manager)
        Globals.ui.searchbox.rebuild()
        
        Globals.ui.songselectlist = pygame_gui.elements.UISelectionList(pygame.Rect((Globals.options.options["screen_width"] - (Globals.options.options["screen_width"]/5), Globals.options.options["fontsize"]), (Globals.options.options["screen_width"]/5, Globals.options.options["screen_height"] - Globals.options.options["fontsize"])), item_list=Globals.loadedmaps.maparray, manager=Globals.ui.manager)
        Globals.ui.songselectlist.background_colour = pygame.Color(40,10,25)
        Globals.ui.songselectlist.border_colour = pygame.Color(255,255,255)
        Globals.ui.songselectlist.list_item_height = 75
        Globals.ui.songselectlist.rebuild()
        
        Globals.loadedmaps.drewlist = True
        
    # Already Rendered
    else:
        # Player Queried something
        if Globals.ui.searchbox.text != "":
            if Globals.loadedmaps.searchquery != Globals.ui.searchbox.text:
                
                search_array = []
                
                for item in Globals.loadedmaps.maparray:
                    if Globals.ui.searchbox.text.lower() in item.lower():
                        
                        search_array.append(item)
                        
                        # performance
                        if len(search_array) >= 1000: break
                        
                Globals.ui.songselectlist.set_item_list(search_array)
                Globals.loadedmaps.searchquery = Globals.ui.searchbox.text
        
        # Seachbox is empty, reset list.
        else:
            if Globals.loadedmaps.searchquery != "":
                
                Globals.ui.songselectlist.set_item_list(Globals.loadedmaps.maparray)
                Globals.loadedmaps.searchquery = ""
        
    dtforui = clock.tick(Globals.options.options["fps"])/1000.0
    Globals.ui.manager.update(dtforui)
    Globals.ui.manager.draw_ui(window)
    pygame.display.update()