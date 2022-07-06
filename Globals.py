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
    req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/ver.txt")
    cloudver = float(req.text)
    
    if cloudver > float(clientversion):
        
        print("There is a new version of Astral available!")
        
        # Download the Latest Installer.
        req = requests.get("https://raw.githubusercontent.com/RenderingByte/Astral/installer/InstallAstral.bat", allow_redirects=True)
        open('InstallAstral.bat', 'wb').write(req.content)
        
        # Run the Installer, Quit the current program.
        sys("start InstallAstral.bat")
        pygame.quit(); exit()
        
    elif cloudver == float(clientversion): print("Astral is running the latest version.")
    
    else:
        
        print("Version Error.")
        pygame.quit(); exit()

# User Options
class Options():
    def Load(self):
        with open("options.json", "r") as f:
            self.options = json.load(f)
    
    def Save(self):
        with open("options.json", "w") as f:
            json.dump(self.options, f)
        print("Options Saved!")
        
options = Options()
options.Load()

# UI Items
class UI():
    def __init__(self):
        self.manager = pygame_gui.UIManager((options.options["screen_width"], options.options["screen_height"]))
        self.songselectlist = None
        self.searchbox = None

ui = UI()

# Engine/PlayField Images
class Images():
    def __init__(self, noteimgs, lnheadimgs, lnbodyimgs, lntailimgs, receptorimgs, receptorDimgs):
        self.noteimgs = noteimgs
        self.lnheadimgs = lnheadimgs
        self.lnbodyimgs = lnbodyimgs
        self.lntailimgs = lntailimgs
        self.receptorimgs = receptorimgs
        self.receptorDimgs = receptorDimgs

images = Images([], [], [], [], [], [])

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
    def __init__(self, menumusicsound, musicsound, hitsound, misssound):
        self.menumusicsound = menumusicsound
        self.musicsound = musicsound
        self.hitsound = hitsound
        self.misssound = misssound

sounds = Sounds(None, None, None, None)

# Global States
class States():
    def __init__(self, inmenu, isselecting, inoptions, isplaying, inmap, failed):
        self.inmenu = inmenu
        self.isselecting = isselecting
        self.inoptions = inoptions
        self.isplaying = isplaying
        self.inmap = inmap
        self.failed = failed

states = States(True, False, False, False, False, False)

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

def Reset(window, map):
    global states, mapinfo, stats
    """
        Reset the Engine and Various Globals.
        
        :param window: The window object (declared in Astral.py)
        :param map: A map object (None is acceptable)

    """
    
    # Stop the song.
    pygame.mixer.music.stop()
    
    # If a map object has been passed, fail the player.
    if not map == None:
        map.clear()
        failimg = pygame.image.load("./images/fail.png").convert_alpha()
        failimg = pygame.transform.scale(failimg, (options.options["screen_width"], options.options["screen_height"]))
        window.blit(failimg, (0, 0))
    
    receptors.clear()
    
    images.noteimgs.clear()
    images.receptorimgs.clear()
    images.receptorDimgs.clear()
    images.lnheadimgs.clear()
    images.lnbodyimgs.clear()
    images.lntailimgs.clear()
    
    states = States(False, (True if map == None else False), False, False, False, (False if map == None else True))
    mapinfo = MapInfo(None, None, {}, 0, 0)
    stats = Stats(0,0,100,0,0,0,0,0,0,100)
   
    pygame.display.update()