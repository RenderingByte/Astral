import json
import pygame
import pygame_gui

pygame.init()

clientversion = "0.00"

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

class UI():
    def __init__(self):
        self.manager = pygame_gui.UIManager((options.options["screen_width"], options.options["screen_height"]))
        # item_list=['Item 1','Item 2','Item 20']
        self.songselectlist = None

ui = UI()

class Images():
    def __init__(self, noteimgs, lnheadimgs, lnbodyimgs, lntailimgs, receptorimgs, receptorDimgs):
        self.noteimgs = noteimgs
        self.lnheadimgs = lnheadimgs
        self.lnbodyimgs = lnbodyimgs
        self.lntailimgs = lntailimgs
        self.receptorimgs = receptorimgs
        self.receptorDimgs = receptorDimgs

images = Images([], [], [], [], [], [])

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

class Sounds():
    def __init__(self, musicsound, hitsound, misssound):
        self.musicsound = musicsound
        self.hitsound = hitsound
        self.misssound = misssound

sounds = Sounds(None, None, None)

class States():
    def __init__(self, inmenu, isselecting, inoptions, isplaying, inmap, failed):
        self.inmenu = inmenu
        self.isselecting = isselecting
        self.inoptions = inoptions
        self.isplaying = isplaying
        self.inmap = inmap
        self.failed = failed

states = States(True, False, False, False, False, False)

class LoadedMaps():
    def __init__(self, maparray, loadedlist, drewlist):
        self.maparray = maparray
        self.loadedlist = loadedlist
        self.drewlist = drewlist

loadedmaps = LoadedMaps([], False, False)

# To load, not really a global (used by song select and Astral)
class MapInfo():
    def __init__(self, map, currenttime, keycount):
        self.map = map
        self.currenttime = currenttime
        self.keycount = keycount

mapinfo = MapInfo(None, 0, 0)

def Reset(window, map):
    global states, mapinfo, stats
    pygame.mixer.music.stop()
    
    if not map == None:
        map.clear()
        failimg = pygame.image.load("./images/fail.png").convert_alpha()
        failimg = pygame.transform.scale(failimg, (options.options["screen_width"], options.options["screen_height"]))
        window.blit(failimg, (0, 0))
        
    states = States(False, (True if map == None else False), False, False, False, (False if map == None else True))
    
    mapinfo = MapInfo(None, 0, 0)
    stats = Stats(0,0,100,0,0,0,0,0,0,100)
    receptors.clear()
    pygame.display.update()