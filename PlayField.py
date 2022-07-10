# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as handling anything related to the PlayField.

# Imports
import Globals
import Engine
import pygame

def LoadMap(path):
    """
        Loads a given map file by name and returns the map offsets.
        This will also load applicable params of Globals.mapinfo.
        
        :param path: The filename of the map to load (e.g. "MyBeatmap - MyDiff")

    """
    
    data = Engine.load("./maps/" + path + "/beatmap.json", True)
    map = data["hitObjects"]
    timingpoints = data["timingPoints"]
    keycount = data["keyCount"]
    
    # Will be true if the map is valid based on user options and is not corrupted.
    isMapValid = True
    
    if map == None or (Globals.options.options["fourkeyonly"] and not keycount == 4): isMapValid = False 
    
    if isMapValid:
        
        Globals.sounds.musicsound = pygame.mixer.Sound("./maps/" + path + "/audio.mp3")
        pygame.mixer.music.load("./maps/" + path + "/audio.mp3")
        pygame.mixer.music.set_volume(Globals.options.options["musicvolume"])
        
        Globals.images.noteimgs.clear()
        Globals.images.lnheadimgs.clear()
        Globals.images.lnbodyimgs.clear()
        Globals.images.lntailimgs.clear()
        Globals.images.receptorimgs.clear()
        Globals.images.receptorDimgs.clear()
        
        for i in range(0, keycount):
            noteimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/note" + str((i+1)) + ".png").convert_alpha()
            noteimg = pygame.transform.scale(noteimg, (Globals.options.options["playfield"][keycount-1][1], Globals.options.options["playfield"][keycount-1][1]))

            lnheadimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/lnhead" + str((i+1)) + ".png").convert_alpha()
            lnheadimg = pygame.transform.scale(lnheadimg, (Globals.options.options["playfield"][keycount-1][1], Globals.options.options["playfield"][keycount-1][1]))
            
            lnbodyimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/lnbody" + str((i+1)) + ".png").convert_alpha()
            
            lntailimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/lntail" + str((i+1)) + ".png").convert_alpha()
            lntailimg = pygame.transform.scale(lntailimg, (Globals.options.options["playfield"][keycount-1][1] / 1.5, Globals.options.options["playfield"][keycount-1][1] / 2))
            
            receptorimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/receptor" + str((i+1)) + ".png").convert_alpha()
            receptorimg = pygame.transform.scale(receptorimg, (Globals.options.options["playfield"][keycount-1][1], Globals.options.options["playfield"][keycount-1][1]))
            
            receptorDimg = pygame.image.load("./skins/" + Globals.options.options["skin"] + "/receptorD" + str((i+1)) + ".png").convert_alpha()
            receptorDimg = pygame.transform.scale(receptorDimg, (Globals.options.options["playfield"][keycount-1][1], Globals.options.options["playfield"][keycount-1][1]))
            
            Globals.images.noteimgs.append(noteimg)
            Globals.images.lnheadimgs.append(lnheadimg)
            Globals.images.lnbodyimgs.append(lnbodyimg)
            Globals.images.lntailimgs.append(lntailimg)
            Globals.images.receptorimgs.append(receptorimg)
            Globals.images.receptorDimgs.append(receptorDimg)

        # Update globally for every other script
        Globals.mapinfo.playingmap = map
        Globals.mapinfo.playingtps = timingpoints
        Globals.mapinfo.keycount = keycount
        
        print("\033[92mMap loaded: " + path)
        
        # Calculate the offset of the map.
        audio = 0
        visual = 0

        return audio, visual
    
    else:
        
        print("\033[91mmap failed to load!")
        return None, None

def Play(window, font, clock):
    """
        Updates the PlayField. This should be ran once every map.
        
        :param window: The window object (declared in Astral.py)
        :param font: The font object (declared in Astral.py)
        :param window: The clock object (declared in Astral.py)
        
    """
    
    # Draw the playfield image
    window.blit(Globals.images.playfieldimg, (0, 0))
    
    # Update the current time with any new TimingPoints.
    tp_to_apply = {}
    current_tp = {}
    first_tp = False
    
    for i in range(0, len(Globals.mapinfo.playingtps)):
        if Globals.mapinfo.currenttime >= Globals.mapinfo.playingtps[i]["time"]:
                
            tp_to_apply = Globals.mapinfo.playingtps[i]
            current_tp = Globals.mapinfo.playingtps[i-1]
            if i == 0: first_tp = True
                
    if not first_tp and (tp_to_apply != {} and current_tp != {}): Globals.mapinfo.currenttime = Globals.mapinfo.currenttime - (60/current_tp["bpm"]/current_tp["timingSignature"]) + (60/tp_to_apply["bpm"]/tp_to_apply["timingSignature"])
    if first_tp and Globals.mapinfo.currenttime == 0: Globals.mapinfo.currenttime = Globals.mapinfo.currenttime + (60/tp_to_apply["bpm"]/tp_to_apply["timingSignature"])
    
    # Update the current time with delta.
    # This also adds frame indepedency.
    dt = clock.tick(Globals.options.options["fps"])
    Globals.mapinfo.currenttime += dt
    
    # Player has died.
    if Globals.stats.hp <= 0:

        Globals.Reset(window, Globals.mapinfo.playingmap, False)
        return
    
    # Map has been completed.
    elif len(Globals.mapinfo.playingmap) == 0: Globals.Reset(window, Globals.mapinfo.playingmap, True); return
    
    # Update Engine
    Engine.Draw(window, Globals.mapinfo.playingmap, Globals.mapinfo.keycount, dt)
    
    # Draw FPS Object
    fps = font.render("FPS: " + str(int(clock.get_fps())), True, pygame.Color(Globals.options.options["fpscolour"]))
    fpsrect = fps.get_rect(center=(Globals.options.options["fpspos"][0], Globals.options.options["fpspos"][1]))
    window.blit(fps, fpsrect)
    
    # Draw Remaining Objects Object
    objects = font.render("OBJECTS: " + str(len(Globals.mapinfo.playingmap)), True, pygame.Color(Globals.options.options["objectscolour"]))
    objectsrect = objects.get_rect(center=(Globals.options.options["objectspos"][0], Globals.options.options["objectspos"][1]))
    window.blit(objects, objectsrect)
    
    # Draw Score Object
    score = font.render(str(Globals.stats.score), True, pygame.Color(Globals.options.options["scorecolour"]))
    scorerect = score.get_rect(center=(Globals.options.options["scorepos"][0], Globals.options.options["scorepos"][1]))
    window.blit(score, scorerect)
    
    # Draw Accuracy Object
    acc = font.render(str(Globals.stats.acc) + "%", True, pygame.Color(Globals.options.options["acccolour"]))
    accrect = acc.get_rect(center=(Globals.options.options["accpos"][0], Globals.options.options["accpos"][1]))
    window.blit(acc, accrect)
    
    # Draw Combo Object
    combo = font.render(str(Globals.stats.combo), True, pygame.Color(Globals.options.options["combocolour"]))
    comborect = combo.get_rect(center=(Globals.options.options["combopos"][0], Globals.options.options["combopos"][1]))
    window.blit(combo, comborect)
    
    # Draw Judgement Object
    judgeimg = Globals.images.marvimg
    if Globals.stats.latestjudge == "MARVELOUS": judgeimg = Globals.images.marvimg
    elif Globals.stats.latestjudge == "PERFECT": judgeimg = Globals.images.perfimg
    elif Globals.stats.latestjudge == "GREAT": judgeimg = Globals.images.greatimg
    elif Globals.stats.latestjudge == "GOOD": judgeimg = Globals.images.goodimg
    elif Globals.stats.latestjudge == "BAD": judgeimg = Globals.images.badimg
    elif Globals.stats.latestjudge == "MISS": judgeimg = Globals.images.missimg

    judgementrect = judgeimg.get_rect(center=(Globals.options.options["judgementpos"][0], Globals.options.options["judgementpos"][1]))
    window.blit(judgeimg, judgementrect)
    
    # Draw Song Progress Bar Object
    timepercent = 100 * ((pygame.mixer.music.get_pos()/1000) + Globals.options.options["audiooffset"]) / Globals.sounds.musicsound.get_length()
    pygame.draw.rect(window, pygame.Color(Globals.options.options["songprogresscolour"]), (Globals.options.options["songprogresspos"][0], Globals.options.options["songprogresspos"][1], timepercent * (Globals.options.options["songprogresssize"][0]/100), Globals.options.options["songprogresssize"][1]))
    
    # Draw HP Bar Object
    if Globals.stats.hp >= 75: hpcolour = Globals.options.options["healthbarnormalcolour"]
    elif Globals.stats.hp >= 25: hpcolour = Globals.options.options["healthbarmediumcolour"]
    elif Globals.stats.hp < 25: hpcolour = Globals.options.options["healthbarlowcolour"]
    pygame.draw.rect(window, pygame.Color(hpcolour), (Globals.options.options["healthbarpos"][0], Globals.options.options["healthbarpos"][1], (Globals.stats.hp/100) * (Globals.options.options["healthbarsize"][0]), Globals.options.options["healthbarsize"][1]))