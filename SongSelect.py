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
        
        Globals.ui.searchbox = pygame_gui.elements.UITextEntryLine(pygame.Rect((0, Globals.options.options["screen_height"] - (Globals.options.options["fontsize"]*1.5)), (Globals.options.options["screen_width"] - (Globals.options.options["screen_width"]/2.5), Globals.options.options["fontsize"]*1.5)), manager=Globals.ui.manager)
        Globals.ui.searchbox.text = "Search for a map..."
        Globals.ui.searchbox.rebuild()
        
        Globals.ui.songselectlist = pygame_gui.elements.UISelectionList(pygame.Rect((Globals.options.options["screen_width"] - (Globals.options.options["screen_width"]/2.5), 0), (Globals.options.options["screen_width"]/2.5, Globals.options.options["screen_height"])), item_list=Globals.loadedmaps.maparray, manager=Globals.ui.manager)
        
        Globals.loadedmaps.drewlist = True
        
    # Already Rendered
    else:
        # Player Queried something
        if Globals.ui.searchbox.text != "" and Globals.ui.searchbox.text != "Search for a map...":
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
    
    # Draw background image
    songselectimg = pygame.image.load("./images/songselect.png").convert_alpha()
    songselectimg = pygame.transform.scale(songselectimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
    window.blit(songselectimg, (0, 0))
    
    # Draw Info object
    difficulty = font.render(("Difficulty: N/A | Keycount: " + str(Globals.mainmenu.selectedsong["keyCount"]) + " | Total Objects: " + str(int(Globals.mainmenu.selectedsong["nbNotes"]) + int(Globals.mainmenu.selectedsong["nbHolds"]))), True, pygame.Color("white"))
    window.blit(difficulty, (10, 55))
    
    dtforui = clock.tick(Globals.options.options["fps"])/1000.0
    Globals.ui.manager.update(dtforui)
    Globals.ui.manager.draw_ui(window)
    pygame.display.update()