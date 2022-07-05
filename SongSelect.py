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
    
    # Draw background image
    songselectimg = pygame.image.load("./images/songselect.png").convert_alpha()
    songselectimg = pygame.transform.scale(songselectimg, (Globals.options.options["screen_width"], Globals.options.options["screen_height"]))
    window.blit(songselectimg, (0, 0))
    
    # Draw "Map Details" object
    mapdetails = font.render("Map Details", True, pygame.Color("white"))
    window.blit(mapdetails, (15, 60))
    
    # Draw Map Name object
    mapname = font.render("Name: " + str(Globals.mainmenu.selectedsong["title"]), True, pygame.Color("white"))
    window.blit(mapname, (15, 120))
    
    # Draw Map Difficulty Name object
    diffname = font.render("Difficulty Name: " + str(Globals.mainmenu.selectedsong["diffname"]), True, pygame.Color("white"))
    window.blit(diffname, (15, 150))
    
    # Draw Artist Name object
    artistname = font.render("Artist: " + str(Globals.mainmenu.selectedsong["artist"]), True, pygame.Color("white"))
    window.blit(artistname, (15, 180))
    
    # Draw Difficulty object
    difficulty = font.render(("Difficulty: N/A"), True, pygame.Color("white"))
    window.blit(difficulty, (15, 210))
    
    # Draw Creator object
    creator = font.render(("Creator: " + Globals.mainmenu.selectedsong["creator"]), True, pygame.Color("white"))
    window.blit(creator, (15, 240))
    
    # Draw Keycount object
    keycount = font.render(("Keycount: " + str(Globals.mainmenu.selectedsong["keyCount"])), True, pygame.Color("white"))
    window.blit(keycount, (15, 270))
    
    # Total Objects object
    totalobjects = font.render(("Total Objects: " + str(int(Globals.mainmenu.selectedsong["nbNotes"]) + int(Globals.mainmenu.selectedsong["nbHolds"]))), True, pygame.Color("white"))
    window.blit(totalobjects, (15, 300))
    
    dtforui = clock.tick(Globals.options.options["fps"])/1000.0
    Globals.ui.manager.update(dtforui)
    Globals.ui.manager.draw_ui(window)
    pygame.display.update()