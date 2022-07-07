# im too lazy to document the engine right now lol!! (you can probably see why...)

import Keymap
import pygame
import json
import Globals

def load(map, drawreceptors):
    data = json.load(open(map, encoding="utf8"))
    
    for note in data["hitObjects"]:
        for kp in data["keyPositions"]:
            if note["x"] == kp:
                note["x"] = data["keyPositions"].index(kp)
    
    if drawreceptors:
        for i in range(0, int(data["keyCount"])):
            Globals.receptors.append(Globals.Receptor((i * Globals.options.options["playfield"][data["keyCount"]-1][1] + Globals.options.options["playfield"][data["keyCount"]-1][2]),Globals.options.options["playfield"][data["keyCount"]-1][0],Keymap.GetKey(Globals.options.options["keybinds"][data["keyCount"]-1][i]),i))
    
    return data

LnReleaseQueue = []
JudgementQueue = []

def Draw(window, map, keycount, dt):
    
    # get from globals
    noteimgs = Globals.images.noteimgs
    receptorimgs = Globals.images.receptorimgs
    receptorDimgs = Globals.images.receptorDimgs
    lnheadimgs = Globals.images.lnheadimgs
    lnbodyimgs = Globals.images.lnbodyimgs
    lntailimgs = Globals.images.lntailimgs
    misssound = Globals.sounds.misssound
    hitpos = Globals.options.options["playfield"][keycount-1][0]
    columnwidth = Globals.options.options["playfield"][keycount-1][1]
    scrollspeed = Globals.options.options["scrollspeed"]
    
    # Receptor Highlighting
    for key in Globals.receptors:
        if pygame.key.get_pressed()[key.keybind]:
            window.blit(receptorDimgs[key.track], (key.x, key.y))
            key.held = True            
        else:
            window.blit(receptorimgs[key.track], (key.x, key.y))
            key.held = False
            key.heldafter = False
    
    # Note Rendering
    for note in map:

        if note["time"] <= Globals.mapinfo.currenttime + ((Globals.options.options["screen_height"] + 50) / (scrollspeed/10)) and note["endTime"] > Globals.mapinfo.currenttime - ((Globals.options.options["screen_height"] + 50) / (scrollspeed/10)): # within screen bounds (roughly)
            
            y = (Globals.mapinfo.currenttime - (note["time"] - 1)) / (note["time"] - (note["time"] - 1)) * (scrollspeed/10)
            yLN = (Globals.mapinfo.currenttime - (note["endTime"] - 1)) / (note["time"] - (note["time"] - 1)) * (scrollspeed/10) + ((columnwidth/2) / (scrollspeed/10))
            
            # too far down, past bottom of screen so delete and reset combo since it's a miss
            if yLN >= Globals.options.options["screen_height"]+50:
                JudgementQueue.append([note, "miss", y, yLN, None])
                if note in map: del map[map.index(note)]
            
            if note["type"] == "note": window.blit(noteimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, y))
            
            drewheldln = False
            
            # Input Handling + Drawing LN
            if Globals.receptors[note["x"]].held:
                
                # Inside register area
                if (y <= hitpos+columnwidth) and (y >= hitpos-columnwidth):
                    
                    if note["type"] == "note" and not Globals.receptors[note["x"]].heldafter and not Globals.receptors[note["x"]].holdingln:
                        JudgementQueue.append([note, "hit", y, yLN, None])
                        Globals.receptors[note["x"]].heldafter = True
                        if note in map: del map[map.index(note)]
                    
                    # hold note, and receptor is released
                    elif note["type"] == "hold" and not Globals.receptors[note["x"]].heldafter:
                        # size of ln is pos+
                        if (hitpos - yLN >= 0):
                            
                            # size of ln can be pos+ after dt
                            if (note["time"] + dt <= note["endTime"]):
  
                                note["time"] += dt
                                
                                # first hold check (not already let go and reholding)
                                if note["newCombo"] == False and not Globals.receptors[note["x"]].holdingln:
                                    JudgementQueue.append([note, "hit", y, yLN , True])
                                    LnReleaseQueue.append([note])
                                    note["newCombo"] = True
                                
                                lnobjS = pygame.transform.scale(lnbodyimgs[Globals.receptors[note["x"]].track], ((columnwidth/1.5), (hitpos - yLN))).convert_alpha()
                                window.blit(lnobjS, (Globals.receptors[note["x"]].x + (columnwidth/6), yLN + (columnwidth/2)))
                                window.blit(lntailimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x + (columnwidth/6), yLN))
                                window.blit(lnheadimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, hitpos))
                                
                                Globals.receptors[note["x"]].heldafter = False
                                Globals.receptors[note["x"]].holdingln = True
                                
                                drewheldln = True # do not drawn a regular ln
                            else:
                                Globals.receptors[note["x"]].heldafter = True
                                Globals.receptors[note["x"]].holdingln = False
                        else:
                            Globals.receptors[note["x"]].heldafter = True
                            Globals.receptors[note["x"]].holdingln = False
                            if note in map: del map[map.index(note)] # so it looks better lol

            if note["type"] == "hold" and not drewheldln:
                lnobj = pygame.transform.scale(lnbodyimgs[Globals.receptors[note["x"]].track], ((columnwidth/1.5), (note["endTime"] - note["time"]) * (scrollspeed/10))).convert_alpha()
                window.blit(lnobj, (Globals.receptors[note["x"]].x + (columnwidth/6), yLN))
                window.blit(lntailimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x + (columnwidth/6), yLN))
                window.blit(lnheadimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, y))
                Globals.receptors[note["x"]].holdingln = False
    
    # Release Handling
    for note in LnReleaseQueue:
        if not Globals.receptors[note[0]["x"]].held:
            if note[0]["type"] == "hold" and note[0]["newCombo"]:

                y = (Globals.mapinfo.currenttime - (note[0]["time"] - 1)) / (note[0]["time"] - (note[0]["time"] - 1)) * (scrollspeed/10)
                yLN = (Globals.mapinfo.currenttime - (note[0]["endTime"] - 1)) / (note[0]["time"] - (note[0]["time"] - 1)) * (scrollspeed/10) + ((columnwidth/2) / (scrollspeed/10))
                
                JudgementQueue.append([note[0], "hit", y, yLN, False]) 
                Globals.receptors[note[0]["x"]].holdingln = False
                if note in LnReleaseQueue: del LnReleaseQueue[LnReleaseQueue.index(note)]
                if hitpos - yLN <= columnwidth/2:
                    if note[0] in map: del map[map.index(note[0])]
    
    # Update Judgements
    for note in JudgementQueue:

        if note[1] == "miss":
            Globals.stats.combo = 0
            Globals.stats.miss += 1
            Globals.stats.hp -= 5
            Globals.stats.latestjudge = "MISS"
            pygame.mixer.Channel(1).play(misssound)
            
        elif note[1] == "hit":
            
            judge_y = ""
            
            if note[0]["type"] == "note":
                bad_range = columnwidth/1.013
                good_range = columnwidth/1.15
                great_range = columnwidth/1.36
                perfect_range = columnwidth/2.14
                marvelous_range = columnwidth/4.29
            elif note[0]["type"] == "hold":
                bad_range = columnwidth*2
                good_range = columnwidth*2
                great_range = columnwidth
                perfect_range = columnwidth/1.66
                marvelous_range = columnwidth/3
            
            if note[0]["type"] == "note": judge_y = note[2]
            elif note[0]["type"] == "hold" and note[4]: judge_y = note[2]
            elif note[0]["type"] == "hold" and not note[4]: judge_y = note[3] - (columnwidth/2)
            else: print("judgement fallback!"); judge_y = note[2] # this should like never occur unless a parse bug got by

            if (judge_y <= hitpos+bad_range) and (judge_y >= hitpos-bad_range):
                Globals.stats.combo += 1
                Globals.stats.latestjudge = "BAD"
                Globals.stats.score += 50 # 50
                Globals.stats.bad += 1
                Globals.stats.hp -= 3
                if (judge_y <= hitpos+good_range) and (judge_y >= hitpos-good_range):
                    Globals.stats.latestjudge = "GOOD"
                    Globals.stats.score += 50  # 100
                    Globals.stats.bad -= 1
                    Globals.stats.good += 1
                    Globals.stats.hp += 1
                    if (judge_y <= hitpos+great_range) and (judge_y >= hitpos-great_range):
                        Globals.stats.latestjudge = "GREAT"
                        Globals.stats.score += 100  # 200
                        Globals.stats.good -= 1
                        Globals.stats.great += 1
                        Globals.stats.hp += 1
                        if (judge_y <= hitpos+perfect_range) and (judge_y >= hitpos-perfect_range):
                            Globals.stats.latestjudge = "PERFECT"
                            Globals.stats.score += 100 # 300
                            Globals.stats.great -= 1
                            Globals.stats.perf += 1
                            Globals.stats.hp += 3
                            if (judge_y <= hitpos+marvelous_range) and (judge_y >= hitpos-marvelous_range):
                                Globals.stats.latestjudge = "MARVELOUS"
                                Globals.stats.score += 50 # 350
                                Globals.stats.perf -= 1
                                Globals.stats.marv += 1
                                Globals.stats.hp += 1
                                
            else:
                Globals.stats.latestjudge = "MISS"
                Globals.stats.combo = 0
                Globals.stats.miss += 1
                Globals.stats.hp -= 5
                pygame.mixer.Channel(1).play(misssound)
        
        Globals.stats.acc = 100*(350*(Globals.stats.marv + Globals.stats.perf) + 200*(Globals.stats.great) + 100*(Globals.stats.good) + 50*(Globals.stats.bad)) / (350*(Globals.stats.marv + Globals.stats.perf + Globals.stats.great + Globals.stats.good + Globals.stats.bad + Globals.stats.miss))
        Globals.stats.acc = round(Globals.stats.acc, 2)
        if Globals.stats.acc > 100: Globals.stats.acc = 100
        if Globals.stats.hp > 100: Globals.stats.hp = 100
        if note in JudgementQueue: del JudgementQueue[JudgementQueue.index(note)]
    
    Globals.mapinfo.playingmap = map