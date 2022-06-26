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
            Globals.receptors.append(Globals.Receptor((i * Globals.options.options["playfield"][data["keyCount"]-1][1] + Globals.options.options["playfield"][data["keyCount"]-1][2]),Globals.options.options["playfield"][data["keyCount"]-1][0],Keymap.getkey(Globals.options.options["keybinds"][data["keyCount"]-1][i]),i))
    
    return data

LnReleaseQueue = []
JudgementQueue = []

def draw(window, map, keycount, currenttime, dt):
    
    # get from globals
    noteimgs = Globals.images.noteimgs
    receptorimgs = Globals.images.receptorimgs
    receptorDimgs = Globals.images.receptorDimgs
    lnheadimgs = Globals.images.lnheadimgs
    lnbodyimgs = Globals.images.lnbodyimgs
    lntailimgs = Globals.images.lntailimgs
    misssound = Globals.sounds.misssound
    
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

        if note["time"] <= currenttime + ((Globals.options.options["screen_height"] + 50) / (Globals.options.options["scrollspeed"]/10)) and note["endTime"] > currenttime - ((Globals.options.options["screen_height"] + 50) / (Globals.options.options["scrollspeed"]/10)): # within screen bounds (roughly)
            
            y = (currenttime - (note["time"] - 1)) / (note["time"] - (note["time"] - 1)) * (Globals.options.options["scrollspeed"]/10)
            yLN = (currenttime - (note["endTime"] - 1)) / (note["time"] - (note["time"] - 1)) * (Globals.options.options["scrollspeed"]/10) + ((Globals.options.options["playfield"][keycount-1][1]/2) / (Globals.options.options["scrollspeed"]/10))
            lnobj = pygame.transform.scale(lnbodyimgs[Globals.receptors[note["x"]].track], ((Globals.options.options["playfield"][keycount-1][1]/1.5), (note["endTime"] - note["time"]) * (Globals.options.options["scrollspeed"]/10)))
            
            # too far down, past bottom of screen so delete and reset combo since it's a miss
            if yLN >= Globals.options.options["screen_height"]+50:
                JudgementQueue.append([note, "miss", y, yLN, None])
                if note in map: del map[map.index(note)]
            
            if note["type"] == "note": window.blit(noteimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, y))
            
            drewheldln = False
            
            # Input Handling + Drawing LN
            if Globals.receptors[note["x"]].held:
                
                # Inside register area
                if (y <= Globals.options.options["playfield"][keycount-1][0]+Globals.options.options["playfield"][keycount-1][1]) and (y >= Globals.options.options["playfield"][keycount-1][0]-Globals.options.options["playfield"][keycount-1][1]):
                    
                    if note["type"] == "note" and not Globals.receptors[note["x"]].heldafter and not Globals.receptors[note["x"]].holdingln:
                        JudgementQueue.append([note, "hit", y, yLN, None])
                        Globals.receptors[note["x"]].heldafter = True
                        if note in map: del map[map.index(note)]
                    
                    # hold note, and receptor is released
                    elif note["type"] == "hold" and not Globals.receptors[note["x"]].heldafter:
                        # size of ln is pos+
                        if (Globals.options.options["playfield"][keycount-1][0] - yLN >= 0):
                            
                            # size of ln can be pos+ after dt
                            if (note["time"] + dt <= note["endTime"]):
  
                                note["time"] += dt
                                
                                # first hold check (not already let go and reholding)
                                if note["newCombo"] == False and not Globals.receptors[note["x"]].holdingln:
                                    JudgementQueue.append([note, "hit", y, yLN , True])
                                    LnReleaseQueue.append([note])
                                    note["newCombo"] = True
                                
                                lnobjS = pygame.transform.scale(lnbodyimgs[Globals.receptors[note["x"]].track], ((Globals.options.options["playfield"][keycount-1][1]/1.5), (Globals.options.options["playfield"][keycount-1][0] - yLN)))
                                window.blit(lnobjS, (Globals.receptors[note["x"]].x + (Globals.options.options["playfield"][keycount-1][1]/6), yLN + (Globals.options.options["playfield"][keycount-1][1]/2)))
                                window.blit(lntailimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x + (Globals.options.options["playfield"][keycount-1][1]/6), yLN))
                                window.blit(lnheadimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, Globals.options.options["playfield"][keycount-1][0]))
                                
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
                window.blit(lnobj, (Globals.receptors[note["x"]].x + (Globals.options.options["playfield"][keycount-1][1]/6), yLN))
                window.blit(lntailimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x + (Globals.options.options["playfield"][keycount-1][1]/6), yLN))
                window.blit(lnheadimgs[Globals.receptors[note["x"]].track], (Globals.receptors[note["x"]].x, y))
                Globals.receptors[note["x"]].holdingln = False
    
    # Release Handling
    for note in LnReleaseQueue:
        if not Globals.receptors[note[0]["x"]].held:
            if note[0]["type"] == "hold" and note[0]["newCombo"]:

                y = (currenttime - (note[0]["time"] - 1)) / (note[0]["time"] - (note[0]["time"] - 1)) * (Globals.options.options["scrollspeed"]/10)
                yLN = (currenttime - (note[0]["endTime"] - 1)) / (note[0]["time"] - (note[0]["time"] - 1)) * (Globals.options.options["scrollspeed"]/10) + ((Globals.options.options["playfield"][keycount-1][1]/2) / (Globals.options.options["scrollspeed"]/10))
                
                JudgementQueue.append([note[0], "hit", y, yLN, False]) 
                Globals.receptors[note[0]["x"]].holdingln = False
                if note in LnReleaseQueue: del LnReleaseQueue[LnReleaseQueue.index(note)]
                if Globals.options.options["playfield"][keycount-1][0] - yLN <= Globals.options.options["playfield"][keycount-1][1]/2:
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
                bad_range = Globals.options.options["playfield"][keycount-1][1]/1.013
                good_range = Globals.options.options["playfield"][keycount-1][1]/1.15
                great_range = Globals.options.options["playfield"][keycount-1][1]/1.36
                perfect_range = Globals.options.options["playfield"][keycount-1][1]/2.14
                marvelous_range = Globals.options.options["playfield"][keycount-1][1]/4.29
            elif note[0]["type"] == "hold":
                bad_range = Globals.options.options["playfield"][keycount-1][1]*2
                good_range = Globals.options.options["playfield"][keycount-1][1]*2
                great_range = Globals.options.options["playfield"][keycount-1][1]
                perfect_range = Globals.options.options["playfield"][keycount-1][1]/1.66
                marvelous_range = Globals.options.options["playfield"][keycount-1][1]/3
            
            if note[0]["type"] == "note": judge_y = note[2]
            elif note[0]["type"] == "hold" and note[4]: judge_y = note[2]
            elif note[0]["type"] == "hold" and not note[4]: judge_y = note[3] - (Globals.options.options["playfield"][keycount-1][1]/2)
            else: print("judgement fallback!"); judge_y = note[2] # this should like never occur unless a parse bug got by

            if (judge_y <= Globals.options.options["playfield"][keycount-1][0]+bad_range) and (judge_y >= Globals.options.options["playfield"][keycount-1][0]-bad_range):
                Globals.stats.combo += 1
                Globals.stats.latestjudge = "BAD"
                Globals.stats.score += 50 # 50
                Globals.stats.bad += 1
                Globals.stats.hp -= 3
                if (judge_y <= Globals.options.options["playfield"][keycount-1][0]+good_range) and (judge_y >= Globals.options.options["playfield"][keycount-1][0]-good_range):
                    Globals.stats.latestjudge = "GOOD"
                    Globals.stats.score += 50  # 100
                    Globals.stats.bad -= 1
                    Globals.stats.good += 1
                    Globals.stats.hp += 1
                    if (judge_y <= Globals.options.options["playfield"][keycount-1][0]+great_range) and (judge_y >= Globals.options.options["playfield"][keycount-1][0]-great_range):
                        Globals.stats.latestjudge = "GREAT"
                        Globals.stats.score += 100  # 200
                        Globals.stats.good -= 1
                        Globals.stats.great += 1
                        Globals.stats.hp += 1
                        if (judge_y <= Globals.options.options["playfield"][keycount-1][0]+perfect_range) and (judge_y >= Globals.options.options["playfield"][keycount-1][0]-perfect_range):
                            Globals.stats.latestjudge = "PERFECT"
                            Globals.stats.score += 100 # 300
                            Globals.stats.great -= 1
                            Globals.stats.perf += 1
                            Globals.stats.hp += 3
                            if (judge_y <= Globals.options.options["playfield"][keycount-1][0]+marvelous_range) and (judge_y >= Globals.options.options["playfield"][keycount-1][0]-marvelous_range):
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
    
    return map