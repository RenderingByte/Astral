# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as a way to display the Options Menu.

# Imports
import Globals
import pygame
import pygame_gui
import os

pygame.init()

def Display(window, clock, font):
    """
        Update the window to display the Options Menu.
        
        :param window: The window object (declared in Astral.py)
        :param clock: The clock object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)

    """
    
    window.blit(Globals.images.optionsmenuimg, (0, 0))
    
    # Use a random element to verify if elements have not been created yet
    if Globals.ui.skinselect == None:
        
        Globals.ui.fullscreenselect = pygame_gui.elements.UIButton(pygame.Rect((100, 300), (200, 50)), text="FULLSCREEN: "+("true" if Globals.options.visualoptions["fullscreen"] else "false"), manager=Globals.ui.manager)
        
        Globals.ui.enablerpcselect = pygame_gui.elements.UIButton(pygame.Rect((1600, 300), (200, 50)), text="RPC: "+("true" if Globals.options.visualoptions["enablerpc"] else "false"), manager=Globals.ui.manager)
        
        Globals.ui.fourkeyonlyselect = pygame_gui.elements.UIButton(pygame.Rect((1600, 400), (200, 50)), text="4K ONLY: "+("true" if Globals.options.visualoptions["fourkeyonly"] else "false"), manager=Globals.ui.manager)
        
        skins = []
        current_selected_skin = Globals.options.visualoptions["skin"]
        for filename in os.listdir("./skins/"): skins.append("Skin ("+filename+")")
        Globals.ui.skinselect = pygame_gui.elements.UIDropDownMenu(skins, starting_option="Skin ("+current_selected_skin+")", relative_rect=pygame.Rect((400, 400), (200, 50)), manager=Globals.ui.manager)
        
        Globals.ui.scrollspeedlbl = Globals.ui.scrollspeed = pygame_gui.elements.UILabel(pygame.Rect((400, 250), (200, 50)), text="SCROLLSPEED", manager=Globals.ui.manager)
        Globals.ui.scrollspeedselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((400, 300), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.scrollspeedselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.scrollspeedselect.text = str(int(Globals.options.visualoptions["scrollspeed"]))
        Globals.ui.scrollspeedselect.rebuild()
        
        Globals.ui.screenwidthlbl = pygame_gui.elements.UILabel(pygame.Rect((100, 350), (200, 50)), text="SCREEN WIDTH", manager=Globals.ui.manager)
        Globals.ui.screenwidthselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((100, 400), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.screenwidthselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.screenwidthselect.text = str(Globals.options.visualoptions["screen_width"])
        Globals.ui.screenwidthselect.rebuild()
        
        Globals.ui.screenheightlbl = pygame_gui.elements.UILabel(pygame.Rect((100, 450), (200, 50)), text="SCREEN HEIGHT", manager=Globals.ui.manager)
        Globals.ui.screenheightselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((100, 500), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.screenheightselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.screenheightselect.text = str(Globals.options.visualoptions["screen_height"])
        Globals.ui.screenheightselect.rebuild()
        
        Globals.ui.fpslbl = pygame_gui.elements.UILabel(pygame.Rect((100, 550), (200, 50)), text="FPS", manager=Globals.ui.manager)
        Globals.ui.fpsselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((100, 600), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.fpsselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.fpsselect.text = str(Globals.options.visualoptions["fps"])
        Globals.ui.fpsselect.rebuild()
        
        
        
        Globals.ui.fontnamelbl = pygame_gui.elements.UILabel(pygame.Rect((700, 250), (200, 50)), text="FONT NAME", manager=Globals.ui.manager)
        Globals.ui.fontnameselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((700, 300), (200, 50)), manager=Globals.ui.manager)
        Globals.ui.fontnameselect.text = str(Globals.options.visualoptions["fontname"])
        Globals.ui.fontnameselect.rebuild()
        
        Globals.ui.fontsizelbl = pygame_gui.elements.UILabel(pygame.Rect((700, 350), (200, 50)), text="FONT SIZE", manager=Globals.ui.manager)
        Globals.ui.fontsizeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((700, 400), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.fontsizeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.fontsizeselect.text = str(Globals.options.visualoptions["fontsize"])
        Globals.ui.fontsizeselect.rebuild()
        
        Globals.ui.audiooffsetlbl = pygame_gui.elements.UILabel(pygame.Rect((400, 450), (200, 50)), text="AUDIO OFFSET", manager=Globals.ui.manager)
        Globals.ui.audiooffsetselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((400, 500), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.audiooffsetselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.audiooffsetselect.text = str(int(Globals.options.visualoptions["audiooffset"]))
        Globals.ui.audiooffsetselect.rebuild()
        
        Globals.ui.visualoffsetlbl = pygame_gui.elements.UILabel(pygame.Rect((400, 550), (200, 50)), text="VISUAL OFFSET", manager=Globals.ui.manager) 
        Globals.ui.visualoffsetselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((400, 600), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.visualoffsetselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.visualoffsetselect.text = str(int(Globals.options.visualoptions["visualoffset"]))
        Globals.ui.visualoffsetselect.rebuild()
        
        Globals.ui.musicvolumelbl = pygame_gui.elements.UILabel(pygame.Rect((400, 650), (200, 50)), text="MUSIC VOLUME", manager=Globals.ui.manager)
        Globals.ui.musicvolumeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((400, 700), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.musicvolumeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.musicvolumeselect.text = str(int(Globals.options.visualoptions["musicvolume"]))
        Globals.ui.musicvolumeselect.rebuild()
        
        Globals.ui.soundvolumelbl = pygame_gui.elements.UILabel(pygame.Rect((400, 750), (200, 50)), text="SOUND VOLUME", manager=Globals.ui.manager)
        Globals.ui.soundvolumeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((400, 800), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.soundvolumeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        Globals.ui.soundvolumeselect.text = str(int(Globals.options.visualoptions["soundvolume"]))
        Globals.ui.soundvolumeselect.rebuild()
        
        
        
        Globals.ui.fpsposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 250), (200, 50)), text="FPS OBJECT POS", manager=Globals.ui.manager)
        Globals.ui.fpsposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 300), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.fpsposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.fpsposselect.text = "("+str(int(Globals.options.visualoptions["fpspos"][0]))+", "+str(int(Globals.options.visualoptions["fpspos"][1]))+")"
        Globals.ui.fpsposselect.rebuild()
        
        Globals.ui.objectsposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 350), (200, 50)), text="OBJECTS LEFT POS", manager=Globals.ui.manager)
        Globals.ui.objectsposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 400), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.objectsposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.objectsposselect.text = "("+str(int(Globals.options.visualoptions["objectspos"][0]))+", "+str(int(Globals.options.visualoptions["objectspos"][1]))+")"
        Globals.ui.objectsposselect.rebuild()
        
        Globals.ui.comboposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 450), (200, 50)), text="COMBO POS", manager=Globals.ui.manager)
        Globals.ui.comboposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 500), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.comboposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.comboposselect.text = "("+str(int(Globals.options.visualoptions["combopos"][0]))+", "+str(int(Globals.options.visualoptions["combopos"][1]))+")"
        Globals.ui.comboposselect.rebuild()
        
        Globals.ui.healthbarposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 550), (200, 50)), text="HEALTH BAR POS", manager=Globals.ui.manager)
        Globals.ui.healthbarposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 600), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.healthbarposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.healthbarposselect.text = "("+str(int(Globals.options.visualoptions["healthbarpos"][0]))+", "+str(int(Globals.options.visualoptions["healthbarpos"][1]))+")"
        Globals.ui.healthbarposselect.rebuild()
        
        Globals.ui.songprogressposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 650), (200, 50)), text="PROGRESS BAR POS", manager=Globals.ui.manager)
        Globals.ui.songprogressposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 700), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.songprogressposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.songprogressposselect.text = "("+str(int(Globals.options.visualoptions["songprogresspos"][0]))+", "+str(int(Globals.options.visualoptions["songprogresspos"][1]))+")"
        Globals.ui.songprogressposselect.rebuild()
        
        Globals.ui.judgementposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 750), (200, 50)), text="JUDGEMENT POS", manager=Globals.ui.manager)
        Globals.ui.judgementposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 800), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.judgementposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.judgementposselect.text = "("+str(int(Globals.options.visualoptions["judgementpos"][0]))+", "+str(int(Globals.options.visualoptions["judgementpos"][1]))+")"
        Globals.ui.judgementposselect.rebuild()
        
        Globals.ui.scoreposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 850), (200, 50)), text="SCORE POS", manager=Globals.ui.manager)
        Globals.ui.scoreposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 900), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.scoreposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.scoreposselect.text = "("+str(int(Globals.options.visualoptions["scorepos"][0]))+", "+str(int(Globals.options.visualoptions["scorepos"][1]))+")"
        Globals.ui.scoreposselect.rebuild()
        
        Globals.ui.accposlbl = pygame_gui.elements.UILabel(pygame.Rect((1000, 950), (200, 50)), text="ACCURACY POS", manager=Globals.ui.manager)
        Globals.ui.accposselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1000, 1000), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.accposselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.accposselect.text = "("+str(int(Globals.options.visualoptions["accpos"][0]))+", "+str(int(Globals.options.visualoptions["accpos"][1]))+")"
        Globals.ui.accposselect.rebuild()
        
        
        
        Globals.ui.healthbarsizelbl = pygame_gui.elements.UILabel(pygame.Rect((1300, 250), (200, 50)), text="HEALTH BAR SIZE", manager=Globals.ui.manager)
        Globals.ui.healthbarsizeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1300, 300), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.healthbarsizeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.healthbarsizeselect.text = "("+str(int(Globals.options.visualoptions["healthbarsize"][0]))+", "+str(int(Globals.options.visualoptions["healthbarsize"][1]))+")"
        Globals.ui.healthbarsizeselect.rebuild()
        
        Globals.ui.songprogresssizelbl = pygame_gui.elements.UILabel(pygame.Rect((1300, 350), (200, 50)), text="PROGRESS BAR SIZE", manager=Globals.ui.manager)
        Globals.ui.songprogresssizeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1300, 400), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.songprogresssizeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.songprogresssizeselect.text = "("+str(int(Globals.options.visualoptions["songprogresssize"][0]))+", "+str(int(Globals.options.visualoptions["songprogresssize"][1]))+")"
        Globals.ui.songprogresssizeselect.rebuild()
        
        Globals.ui.judgementsizelbl = pygame_gui.elements.UILabel(pygame.Rect((1300, 450), (200, 50)), text="JUDGEMENT SIZE", manager=Globals.ui.manager)
        Globals.ui.judgementsizeselect = pygame_gui.elements.UITextEntryLine(pygame.Rect((1300, 500), (75, 50)), manager=Globals.ui.manager)
        Globals.ui.judgementsizeselect.allowed_characters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", " ", ","]
        Globals.ui.judgementsizeselect.text = "("+str(int(Globals.options.visualoptions["judgementsize"][0]))+", "+str(int(Globals.options.visualoptions["judgementsize"][1]))+")"
        Globals.ui.judgementsizeselect.rebuild()
    
    dtforui = clock.tick(Globals.options.visualoptions["fps"])/1000.0
    Globals.ui.manager.update(dtforui)
    Globals.ui.manager.draw_ui(window)