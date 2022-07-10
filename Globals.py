# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as storing the global variables for the application.

# Imports
import json
import requests
import sys
import pygame
import pygame_gui

# Initialization
pygame.init()

# Astral Program
class Program():
    def __init__(self, isRunning):
        self.isRunning = isRunning

program = Program(True)

# Astral Client Version (read-only)
clientversion = "0.01"

def CheckForUpdates():
    """
        Checks for updates to the Astral client using the GitHub repo.
        Compares the current version to the latest version.
        Downloads and runs the installer if needed.
        
        A Network Connection is needed to run this function.

    """

    # Get the latest version from GitHub.
    try:
        
        req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/ver.txt")
        
    except:
        
        print("\033[91mNo Network Connection - Cannot check for updates.")
        return
        
    cloudver = float(req.text)
    
    if cloudver > float(clientversion):
        
        print("\033[93mThere is a new version of Astral available!")
        
        # Download the Latest Installer.
        req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/InstallAstral.bat", allow_redirects=True)
        open('InstallAstral.bat', 'wb').write(req.content)
        
        # Run the Installer, Quit the current program.
        sys("start InstallAstral.bat")
        program.isRunning = False
        
    elif cloudver == float(clientversion): print("\033[92mAstral is running the latest version.")
    
    else:
        
        print("\033[91mVersion Error.")
        program.isRunning = False

# User Options
class Options():
    def Load(self):
        """
            Load all options from the Options.json file as an array.
            Stores the array in the options.options and options.visualoptions variable.
            
            They both have differences:
            The visualoptions array is the raw data fetched (with tuple format being percentages (0-100).
            Meanwhile, options.options has conversions for the Astral program to use. This should not be accessed by the user.
            
        """
    
        # Load for user to modify (stored as percentages)
        with open("Options.json", "r") as f: self.visualoptions = json.load(f)
        
        # Load for Astral - and nothing else - to use (stored as pixels)
        with open("Options.json", "r") as f:
            self.options = json.load(f)
            
            # y = (x/width|height)*100 -> get percent from pixel
            # y = (x/100)*width|height -> get pixel from percent
            
            # From readability -> Astral
            options.options["scrollspeed"] = options.options["scrollspeed"]/10
            options.options["musicvolume"] = options.options["musicvolume"]/10
            options.options["soundvolume"] = options.options["soundvolume"]/10
            options.options["audiooffset"] = options.options["audiooffset"]/1000
            
            # Percentage to pixel conversion
            for k in range(len(self.options["playfield"])):
                for v in range(len(self.options["playfield"][k])):
                    
                    if v == 0:
                        # hitpos
                        self.options["playfield"][k][v] = (self.options["playfield"][k][v]/100)*options.options["screen_height"]
                    elif v == 1:
                        # columnwidth
                        self.options["playfield"][k][v] = (self.options["playfield"][k][v]/100)*options.options["screen_width"]
                    elif v == 2:
                        # columnoffset
                        self.options["playfield"][k][v] = (self.options["playfield"][k][v]/100)*options.options["screen_width"]
            
            options.options["fpspos"][0] = (options.options["fpspos"][0]/100)*options.options["screen_width"]
            options.options["fpspos"][1] = (options.options["fpspos"][1]/100)*options.options["screen_height"]
            
            options.options["objectspos"][0] = (options.options["objectspos"][0]/100)*options.options["screen_width"]
            options.options["objectspos"][1] = (options.options["objectspos"][1]/100)*options.options["screen_height"]
            
            options.options["combopos"][0] = (options.options["combopos"][0]/100)*options.options["screen_width"]
            options.options["combopos"][1] = (options.options["combopos"][1]/100)*options.options["screen_height"]
            
            options.options["healthbarpos"][0] = (options.options["healthbarpos"][0]/100)*options.options["screen_width"]
            options.options["healthbarpos"][1] = (options.options["healthbarpos"][1]/100)*options.options["screen_height"]
    
            options.options["songprogresspos"][0] = (options.options["songprogresspos"][0]/100)*options.options["screen_width"]
            options.options["songprogresspos"][1] = (options.options["songprogresspos"][1]/100)*options.options["screen_height"]
            
            options.options["judgementpos"][0] = (options.options["judgementpos"][0]/100)*options.options["screen_width"]
            options.options["judgementpos"][1] = (options.options["judgementpos"][1]/100)*options.options["screen_height"]
            
            options.options["scorepos"][0] = (options.options["scorepos"][0]/100)*options.options["screen_width"]
            options.options["scorepos"][1] = (options.options["scorepos"][1]/100)*options.options["screen_height"]
            
            options.options["accpos"][0] = (options.options["accpos"][0]/100)*options.options["screen_width"]
            options.options["accpos"][1] = (options.options["accpos"][1]/100)*options.options["screen_height"]
            
            options.options["healthbarsize"][0] = (options.options["healthbarsize"][0]/100)*options.options["screen_width"]
            options.options["healthbarsize"][1] = (options.options["healthbarsize"][1]/100)*options.options["screen_height"]
            
            options.options["songprogresssize"][0] = (options.options["songprogresssize"][0]/100)*options.options["screen_width"]
            options.options["songprogresssize"][1] = (options.options["songprogresssize"][1]/100)*options.options["screen_height"]
            
            options.options["judgementsize"][0] = (options.options["judgementsize"][0]/100)*options.options["screen_width"]
            options.options["judgementsize"][1] = (options.options["judgementsize"][1]/100)*options.options["screen_height"]
    
    def Save(self):
        """
            Save all the data in options.visualoptions to the Options.json file.
            This same data is then loaded on startup by options.Load().
            
        """
        
        # Do not allow the user to have a scrollspeed below 10 (causes bugs).
        if int(ui.scrollspeedselect.text) < 10: ui.scrollspeedselect.text = "10"
        ui.scrollspeedselect.rebuild()
        
        options.visualoptions["enablerpc"] = options.options["enablerpc"]
        options.visualoptions["fullscreen"] = options.options["fullscreen"]
        options.visualoptions["screen_width"] = int(ui.screenwidthselect.text)
        options.visualoptions["screen_height"] = int(ui.screenheightselect.text)
        options.visualoptions["fps"] = int(ui.fpsselect.text)
        options.visualoptions["fontname"] = ui.fontnameselect.text
        options.visualoptions["fontsize"] = int(ui.fontsizeselect.text)
        options.visualoptions["skin"] = ui.skinselect.selected_option[6:-1]
        options.visualoptions["fourkeyonly"] = options.options["fourkeyonly"]
        options.visualoptions["scrollspeed"] = int(ui.scrollspeedselect.text)
        options.visualoptions["audiooffset"] = int(ui.audiooffsetselect.text)
        options.visualoptions["visualoffset"] = int(ui.visualoffsetselect.text)
        options.visualoptions["musicvolume"] = int(ui.musicvolumeselect.text)
        options.visualoptions["soundvolume"] = int(ui.soundvolumeselect.text)
        
        options.visualoptions["fpspos"] = list(eval(ui.fpsposselect.text))
        options.visualoptions["objectspos"] = list(eval(ui.objectsposselect.text))
        options.visualoptions["combopos"] = list(eval(ui.comboposselect.text))
        options.visualoptions["healthbarpos"] = list(eval(ui.healthbarposselect.text))
        options.visualoptions["songprogresspos"] = list(eval(ui.songprogressposselect.text))
        options.visualoptions["judgementpos"] = list(eval(ui.judgementposselect.text))
        options.visualoptions["scorepos"] = list(eval(ui.scoreposselect.text))
        options.visualoptions["accpos"] = list(eval(ui.accposselect.text))
        options.visualoptions["healthbarsize"] =  list(eval(ui.healthbarsizeselect.text))
        options.visualoptions["songprogresssize"] = list(eval(ui.songprogresssizeselect.text))
        options.visualoptions["judgementsize"] = list(eval(ui.judgementsizeselect.text))
        
        with open("Options.json", "w") as f: json.dump(options.visualoptions, f)
        print("\033[92mOptions Saved!")
        
options = Options()
options.Load()

# UI Items
class UI():
    def __init__(self):
        self.manager = pygame_gui.UIManager((options.options["screen_width"], options.options["screen_height"]), "./skins/" + options.options["skin"] + "/ui_theme.json")
        self.songselectlist = None
        self.searchbox = None
        self.skinselect = None
        self.scrollspeedselect = None
        self.fullscreenselect = None
        self.enablerpcselect = None
        self.fourkeyonlyselect = None
        self.screenwidthselect = None
        self.screenheightselect = None
        self.fpsselect = None
        self.fontnameselect = None
        self.fontsizeselect = None
        self.audiooffsetselect = None
        self.visualoffsetselect = None
        self.musicvolumeselect = None
        self.soundvolumeselect = None
        self.fpsposselect = None
        self.objectsposselect = None
        self.comboposselect = None
        self.healthbarposselect = None
        self.songprogressposselect = None
        self.judgementposselect = None
        self.scoreposselect = None
        self.accposselect = None
        self.healthbarsizeselect = None
        self.songprogresssizeselect = None
        self.judgementsizeselect = None
        
        self.scrollspeedlbl = None
        self.screenwidthlbl = None
        self.screenheightlbl = None
        self.fpslbl = None
        self.fontnamelbl = None
        self.fontsizelbl = None
        self.audiooffsetlbl = None
        self.visualoffsetlbl = None
        self.musicvolumelbl = None
        self.soundvolumelbl = None
        self.fpsposlbl = None
        self.objectsposlbl = None
        self.comboposlbl = None
        self.healthbarposlbl = None
        self.songprogressposlbl = None
        self.judgementposlbl = None
        self.scoreposlbl = None
        self.accposlbl = None
        self.healthbarsizelbl = None
        self.songprogresssizelbl = None
        self.judgementsizelbl = None

ui = UI()

# Engine/PlayField Images
class Images():
    def __init__(self, noteimgs, lnheadimgs, lnbodyimgs, lntailimgs, receptorimgs, receptorDimgs, playfieldimg, mainmenuimg, optionsmenuimg, songselectmenuimg, marvimg, perfimg, greatimg, goodimg, badimg, missimg, failimg, passimg, cursorimg, cursorimgrect):
        self.noteimgs = noteimgs
        self.lnheadimgs = lnheadimgs
        self.lnbodyimgs = lnbodyimgs
        self.lntailimgs = lntailimgs
        self.receptorimgs = receptorimgs
        self.receptorDimgs = receptorDimgs
        self.playfieldimg = playfieldimg
        self.mainmenuimg = mainmenuimg
        self.optionsmenuimg = optionsmenuimg
        self.songselectmenuimg = songselectmenuimg
        self.marvimg = marvimg
        self.perfimg = perfimg
        self.greatimg = greatimg
        self.goodimg = goodimg
        self.badimg = badimg
        self.missimg = missimg
        self.failimg = failimg
        self.passimg = passimg
        self.cursorimg = cursorimg
        self.cursorimgrect = cursorimgrect

images = Images([], [], [], [], [], [], None, None, None, None, None, None, None, None, None, None, None, None, None, None)

# Engine Receptors
class Receptor():
    def __init__(self,a,b,c,d):
        self.x = a
        self.y = b
        self.keybind = c
        self.track = d
        self.held = False
        self.heldafter = False
        self.holdingln = False

receptors = []

# Engine Stats
class Stats():
    def __init__(self, combo, score, acc, marv, perf, great, good, bad, miss, hp):
        self.combo = combo
        self.score = score
        self.acc = acc
        self.marv = marv
        self.perf = perf
        self.great = great
        self.good = good
        self.bad = bad
        self.miss = miss
        self.hp = hp
        self.latestjudge = ""

stats = Stats(0,0,100,0,0,0,0,0,0,100)

# Global Sounds
class Sounds():
    def __init__(self, menumusicsound, musicsound, hitsound, misssound, uibutton, failsound, passsound):
        self.menumusicsound = menumusicsound
        self.musicsound = musicsound
        self.hitsound = hitsound
        self.misssound = misssound
        self.uibutton = uibutton
        self.failsound = failsound
        self.passsound = passsound

sounds = Sounds(None, None, None, None, None, None, None)

# Global States
class States():
    def __init__(self, inmenu, isselecting, inoptions, isplaying, inmap, showresults, showfailed):
        self.inmenu = inmenu
        self.isselecting = isselecting
        self.inoptions = inoptions
        self.isplaying = isplaying
        self.inmap = inmap
        self.showresults = showresults
        self.showfailed = showfailed

states = States(True, False, False, False, False, False, False)

# SongSelect Maps
class LoadedMaps():
    def __init__(self, maparray, loadedlist, drewlist):
        self.maparray = maparray
        self.loadedlist = loadedlist
        self.drewlist = drewlist
        self.searchquery = ""

loadedmaps = LoadedMaps([], False, False)

# Current Map + SongSelect
class MapInfo():
    def __init__(self, map, playingmap, playingtps, currenttime, keycount):
        self.map = map
        self.playingmap = playingmap
        self.playingtp = playingtps
        self.currenttime = currenttime
        self.keycount = keycount

mapinfo = MapInfo(None, None, {}, 0, 0)

# Main menu items that cannot be a part of other classes
class MainMenu():
    def __init__(self, selectedsong):
        selectedsong = selectedsong

mainmenu = MainMenu(None)

def Reset(window, map, passed):
    global states, mapinfo, stats
    """
        Reset the Engine and Various 
        
        :param window: The window object (declared in Astral.py)
        :param map: A map object (None is acceptable)

    """
    
    # Stop the song.
    pygame.mixer.music.stop()
    
    # If a map object has been passed
    if not map == None: map.clear()
    
    receptors.clear()
    
    images.noteimgs.clear()
    images.receptorimgs.clear()
    images.receptorDimgs.clear()
    images.lnheadimgs.clear()
    images.lnbodyimgs.clear()
    images.lntailimgs.clear()
    
    states = States(False, (True if map == None else False), False, False, False, (False if map == None else True), (False if passed else True))
    mapinfo = MapInfo(None, None, {}, 0, 0)
    stats = Stats(0,0,100,0,0,0,0,0,0,100)
    
def VisibleUI(show, pool):
    """
        Change visibility of drawn pygame_gui elements.
        
        :param show: Show or hide elements?
        :param pool: Which set to modify? (ex. options)
    """
    
    if not show:
        if pool == "songselect":
            if not ui.songselectlist == None:
                        
                ui.songselectlist.hide()
                ui.songselectlist.disable()
                ui.searchbox.visible = 0
                ui.searchbox.disable()
                
        elif pool == "options":
            if not ui.skinselect == None:
                
                ui.skinselect.hide()
                ui.scrollspeedselect.hide()
                ui.fullscreenselect.hide()
                ui.enablerpcselect.hide()
                ui.fourkeyonlyselect.hide()
                ui.screenwidthselect.hide()
                ui.screenheightselect.hide()
                ui.fpsselect.hide()
                ui.fontnameselect.hide()
                ui.fontsizeselect.hide()
                ui.audiooffsetselect.hide()
                ui.visualoffsetselect.hide()
                ui.musicvolumeselect.hide()
                ui.soundvolumeselect.hide()
                ui.fpsposselect.hide()
                ui.objectsposselect.hide()
                ui.comboposselect.hide()
                ui.healthbarposselect.hide()
                ui.songprogressposselect.hide()
                ui.judgementposselect.hide()
                ui.scoreposselect.hide()
                ui.accposselect.hide()
                ui.healthbarsizeselect.hide()
                ui.songprogresssizeselect.hide()
                ui.judgementsizeselect.hide()
                
                ui.scrollspeedlbl.hide()
                ui.screenwidthlbl.hide()
                ui.screenheightlbl.hide()
                ui.fpslbl.hide()
                ui.fontnamelbl.hide()
                ui.fontsizelbl.hide()
                ui.audiooffsetlbl.hide()
                ui.visualoffsetlbl.hide()
                ui.musicvolumelbl.hide()
                ui.soundvolumelbl.hide()
                ui.fpsposlbl.hide()
                ui.objectsposlbl.hide()
                ui.comboposlbl.hide()
                ui.healthbarposlbl.hide()
                ui.songprogressposlbl.hide()
                ui.judgementposlbl.hide()
                ui.scoreposlbl.hide()
                ui.accposlbl.hide()
                ui.healthbarsizelbl.hide()
                ui.songprogresssizelbl.hide()
                ui.judgementsizelbl.hide()
                
    else:
        if pool == "songselect":
            if not ui.songselectlist == None:
                        
                ui.songselectlist.show()
                ui.songselectlist.enable()
                ui.searchbox.visible = 1
                ui.searchbox.enable()
                
        elif pool == "options":
            if not ui.skinselect == None:
                
                ui.skinselect.show()
                ui.scrollspeedselect.show()
                ui.fullscreenselect.show()
                ui.enablerpcselect.show()
                ui.fourkeyonlyselect.show()
                ui.screenwidthselect.show()
                ui.screenheightselect.show()
                ui.fpsselect.show()
                ui.fontnameselect.show()
                ui.fontsizeselect.show()
                ui.audiooffsetselect.show()
                ui.visualoffsetselect.show()
                ui.musicvolumeselect.show()
                ui.soundvolumeselect.show()
                ui.fpsposselect.show()
                ui.objectsposselect.show()
                ui.comboposselect.show()
                ui.healthbarposselect.show()
                ui.songprogressposselect.show()
                ui.judgementposselect.show()
                ui.scoreposselect.show()
                ui.accposselect.show()
                ui.healthbarsizeselect.show()
                ui.songprogresssizeselect.show()
                ui.judgementsizeselect.show()
                
                ui.scrollspeedlbl.show()
                ui.screenwidthlbl.show()
                ui.screenheightlbl.show()
                ui.fpslbl.show()
                ui.fontnamelbl.show()
                ui.fontsizelbl.show()
                ui.audiooffsetlbl.show()
                ui.visualoffsetlbl.show()
                ui.musicvolumelbl.show()
                ui.soundvolumelbl.show()
                ui.fpsposlbl.show()
                ui.objectsposlbl.show()
                ui.comboposlbl.show()
                ui.healthbarposlbl.show()
                ui.songprogressposlbl.show()
                ui.judgementposlbl.show()
                ui.scoreposlbl.show()
                ui.accposlbl.show()
                ui.healthbarsizelbl.show()
                ui.songprogresssizelbl.show()
                ui.judgementsizelbl.show()