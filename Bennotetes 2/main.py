
from typing import Set
import pygame
from pygame import mouse
from pygame.mixer import pause
from pygame.rect import Rect
from pygame.version import PygameVersion
import os
import random
from pygame import mixer_music
pygame.font.init()
import time
class Settings:
    (window_width, window_height) = (1000, 720)
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image = os.path.join(path_file, "Images")
    fps = 60
    caption = "Imposter Simulator" 
    max_nof_SuSs = 15 # mindest anzahl von gegnern
    timer_spawn = 0 # timer für den spawn
    timer_resize = 0 # timer fürs resizing 
    game_points = 0 # The Point counter
    SuS_size_speed = 2 #start geschwindigkeit
    normal_SuS_size_speed = 2 
    player_speed = 5 # spieler geschwindigkeit
    
    spawn_verzögerung = 0.9 # delay der gegner spawns
    max_size = 200
    delay_spawn = 1
    delay_resize = 2
    SuS_size = 5
    max_resize = 25
    mouse_siseH = 100
    mouse_siseV = 200
    test1 =  0
    test2 = 1
    
    #Colors
    color_white = (255,255,255)
    color_black = (255,0,0)
    #Fonts
    font = pygame.font.SysFont('', 30)
    game_font = pygame.font.SysFont('', 90)

class Background(object): # Background
    def __init__(self, filename="vent.jpg"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.path_image, filename)).convert()
        self.image = pygame.transform.scale(self.image, (Settings.window_width, Settings.window_height))

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

  

class SuS(pygame.sprite.Sprite): # Die Gegner
    def __init__(self):
        super().__init__()
        self.image_original = pygame.image.load(os.path.join(Settings.path_image, "bluesus.png")).convert_alpha()
        self.scale = Settings.SuS_size
        self.image = pygame.transform.scale(self.image_original, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, Settings.window_width - 25)
        self.rect.top = random.randint(0, Settings.window_height - 25)
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    def update(self):
        old_center = self.rect.center
        self.image = pygame.transform.scale(self.image_original, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        Settings.test1 +=0.15
        if Settings.test1 >= Settings.test2 and self.scale <= Settings.max_size : #das wachsend er gegner
            self.scale += random.randint(1,4)
            Settings.test1 = 0
        if self.rect.bottom > Settings.window_height:    #wenn die seiten berührt werdeb sterben die gegner 
           self.kill()    
        if self.rect.top < 0:
            self.kill()
        if self.rect.right > Settings.window_width:
            self.kill()
        if self.rect.left < 0:
            self.kill()   




class Mouse(pygame.sprite.Sprite):
    def __init__(self, ):
        super().__init__()
        self.image_og = pygame.image.load(os.path.join(Settings.path_image, "hand.png")).convert_alpha() #die maus wird durch die hand im spiel ersetzt
        self.scaleH = Settings.mouse_siseH
        self.scaleV = Settings.mouse_siseV
        self.image = pygame.transform.scale(self.image_og, (self.scaleV, self.scaleH))

        self.rect = pygame.Rect(0, 0, -5, 1) # x, y, width, height


    def draw(self, screen):
        self.screen.blit(self.image, self.rect)


    def update(self):
        self.rect.center = pygame.mouse.get_pos()


    
            



class Game(object):
    def __init__(self):
        super().__init__()


        # PyGame-Setup / Init
        pygame.init()
        pygame.display.set_caption(Settings.caption)
        self.screen = pygame.display.set_mode((Settings.window_width,Settings.window_height))
        self.clock = pygame.time.Clock()
        self.running = False
        self.SuSs = pygame.sprite.Group()
        self.ispaused = False
        self.SuS = SuS()
        self.mous = Mouse()
        self.mouse = pygame.sprite.Group()

    

    def run(self):
        self.start()
        self.gametext = Settings.game_font.render(f'', False, Settings.color_black)
        # Mainloop
        self.running = True
        while self.running:
            self.clock.tick(Settings.fps)
            self.update()
            self.watch_for_events()
            self.draw()
            self.collison()
            
        # Quits the game
        pygame.quit()

    def draw(self):          # Drawin everything on the Screen
        self.background.draw(self.screen)
        self.SuSs.draw(self.screen)
        self.mouse.draw(self.screen)
        
        self.screen.blit(self.pointtext,(0, 0))
        self.screen.blit(self.gametext,( Settings.window_width//2-240 ,Settings.window_height//2))
        pygame.display.flip()

    def update(self):             # alles das pro frame gecheckt wird
        self.SuSs.update()
        self.mouse.update()
        Settings.timer_spawn += 0.0166666666
        if Settings.timer_spawn >= Settings.delay_spawn and len(self.SuSs.sprites()) <= Settings.max_nof_SuSs:
            self.SuSs.add(SuS())
            spawnsound = pygame.mixer.Sound("spawn.mp3")
            
            spawnsound.play()
            
            Settings.timer_spawn = 0
        Settings.timer_resize += 0.0166666666
        if Settings.timer_resize >= Settings.delay_resize and Settings.SuS_size <= Settings.max_resize:
            Settings.SuS_size += 1
            Settings.timer_resize = 0
        
        
        
       # Text
        
        self.pointtext = Settings.font.render(f'Points = {Settings.game_points}', False, Settings.color_black)
        
    def pause(self):              #die pause funktion
        paused = True 
        while paused:
         

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
            
    def collison(self):        #die collision zwischen 2 gegnern
        
        SuSs = self.SuSs.sprites()
        for i,SuS1 in enumerate(SuSs):
            for SuS2 in SuSs[i+1:]:
                if pygame.sprite.collide_rect(SuS1, SuS2):
                    self.gameover()
                
            
           
        


    def destroy(self):   #das zerstören der gegner bringt andere punkte umso größer sie werden
        if pygame.sprite.groupcollide(self.mouse, self.SuSs, False, True):
            match Settings.SuS_size:
                case 5:
                    Settings.game_points += 1
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                     
                case 6: 
                    Settings.game_points += 1
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 7:
                    Settings.game_points += 2
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 8:
                    Settings.game_points += 2
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 9:
                    Settings.game_points += 2
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 10:
                    Settings.game_points += 3
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 11:
                    Settings.game_points += 5
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 12:
                    Settings.game_points += 5
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 13:
                    Settings.game_points += 5
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 14:
                    Settings.game_points += 5
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 15:
                    Settings.game_points += 6
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 16:
                    Settings.game_points += 6
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 17:
                    Settings.game_points += 8
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 18:
                    Settings.game_points += 8
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 19:
                    Settings.game_points += 8
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 20:
                    Settings.game_points += 10
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 21:
                    Settings.game_points += 10
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 22:
                    Settings.game_points += 11
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 23:
                    Settings.game_points += 12     
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()    
                case 24:
                    Settings.game_points += 15
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case 25:
                    Settings.game_points += 15
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                case _: 
                    if Settings.SuS_size > 25: Settings.game_points += 20
                    else: Settings.game_points += 1
                    spawnsound = pygame.mixer.Sound("kill.mp3")
                    spawnsound.play()
                
        
        
    def gameover(self): # Gameover
        self.ispaused = True
        self.gametext = Settings.game_font.render(f'GAME OVER!', False, Settings.color_black)
        print('Game Over!')
        
        time.sleep(4)
        self.running = False
        
    def watch_for_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN: 
                # Buttom press events with Python 3.10 (match cases/switch cases)
                match event.key:
                    case pygame.K_ESCAPE:
                        self.running = False

                    case pygame.K_p:
                        self.pause()
                    case _:
                        print("Keine Bekannte Taste!")
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.destroy()


    def start(self): # wird am start einamal durch genommen 
       
        self.background = Background()
        self.SuSs.add(SuS())
        self.mouse.add(Mouse())
        pygame.mouse.set_visible(False)
        hintergrundmusik = pygame.mixer.Sound("drip.mp3")
        
        hintergrundmusik.play()






if __name__ == "__main__":

    game = Game()
    game.run()
