import pygame
import Engine
import Globals

def LoadMap(path):
    data = Engine.load("./maps/" + path + "/beatmap.json", True)
    map = data["hitObjects"]
    keycount = data["keyCount"]
    f = True
    
    if map == None or (Globals.options.options["fourkeyonly"] and not keycount == 4): f = False 
    
    if f:
        Globals.sounds.musicsound = pygame.mixer.Sound("./maps/" + path + "/audio.mp3")
        pygame.mixer.music.load("./maps/" + path + "/audio.mp3")
        pygame.mixer.music.set_volume(Globals.options.options["musicvolume"])
        
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
    
        print("Map loaded: " + path)
        
        return map, keycount
    else: print("map failed to load!"); return None, 0

def Play(window, currenttime, map, keycount, font, clock):

    dt = clock.tick(Globals.options.options["fps"])
    currenttime += dt
    
    if Globals.stats.hp <= 0:
        Globals.Reset(window, map)
        return None, 0
        
    elif len(map) == 0: window.blit(font.render("MAP COMPLETED", True, pygame.Color('green')), (Globals.options.options["screen_width"]/2, Globals.options.options["screen_height"]/5))
    
    map = Engine.draw(window, map, keycount, currenttime, dt)
    
    fps = font.render("FPS: " + str(int(clock.get_fps())), True, pygame.Color(Globals.options.options["fpscolour"]))
    fpsrect = fps.get_rect(center=(Globals.options.options["fpspos"][0], Globals.options.options["fpspos"][1]))
    window.blit(fps, fpsrect)
    
    objects = font.render("OBJECTS: " + str(len(map)), True, pygame.Color(Globals.options.options["objectscolour"]))
    objectsrect = objects.get_rect(center=(Globals.options.options["objectspos"][0], Globals.options.options["objectspos"][1]))
    window.blit(objects, objectsrect)
    
    score = font.render(str(Globals.stats.score), True, pygame.Color(Globals.options.options["scorecolour"]))
    scorerect = score.get_rect(center=(Globals.options.options["scorepos"][0], Globals.options.options["scorepos"][1]))
    window.blit(score, scorerect)
    
    acc = font.render(str(Globals.stats.acc) + "%", True, pygame.Color(Globals.options.options["acccolour"]))
    accrect = acc.get_rect(center=(Globals.options.options["accpos"][0], Globals.options.options["accpos"][1]))
    window.blit(acc, accrect)
    
    combo = font.render(str(Globals.stats.combo), True, pygame.Color(Globals.options.options["combocolour"]))
    comborect = combo.get_rect(center=(Globals.options.options["combopos"][0], Globals.options.options["combopos"][1]))
    window.blit(combo, comborect)
    
    judgement = font.render(str(Globals.stats.latestjudge), True, pygame.Color(Globals.options.options["judgementcolour"]))
    judgementrect = judgement.get_rect(center=(Globals.options.options["judgementpos"][0], Globals.options.options["judgementpos"][1]))
    window.blit(judgement, judgementrect)
    
    timepercent = 100 * ((pygame.mixer.music.get_pos()/1000) + Globals.options.options["audiooffset"]) / Globals.sounds.musicsound.get_length()
    pygame.draw.rect(window, pygame.Color(Globals.options.options["songprogresscolour"]), (Globals.options.options["songprogresspos"][0], Globals.options.options["songprogresspos"][1], timepercent * (Globals.options.options["songprogresssize"][0]/100), Globals.options.options["songprogresssize"][1]))
    
    if Globals.stats.hp >= 75: hpcolour = Globals.options.options["healthbarnormalcolour"]
    elif Globals.stats.hp >= 25: hpcolour = Globals.options.options["healthbarmediumcolour"]
    elif Globals.stats.hp < 25: hpcolour = Globals.options.options["healthbarlowcolour"]
    pygame.draw.rect(window, pygame.Color(hpcolour), (Globals.options.options["healthbarpos"][0], Globals.options.options["healthbarpos"][1], Globals.stats.hp * Globals.options.options["healthbarsize"][0], Globals.options.options["healthbarsize"][1]))
    
    pygame.display.update()
    
    return map, currenttime