# game engine using template from Chris Bradfield's "Making Games with Python & Pygame"
# I can push from vs code...
# I can push more code from vs code to github
'''
Main file responsible for game loop including input, update, and draw methods.

Tools for game development.

# creating pixel art:
https://www.piskelapp.com/

# free game assets:
https://opengameart.org/

# free sprite sheets:
https://www.kenney.nl/assets

# sound effects:
https://www.bfxr.net/
# music:
https://incompetech.com/music/royalty-free/


'''

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from utils import *
vec = pg.math.Vector2

# import settings


# the game class that will be instantiated in order to run the game...
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        # setting up pygame screen using tuple value for width height
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()
        self.running = True
        self.playing = True
        self.game_cooldown = Cooldown(5000)
        self.levels = ['level1.txt', 'level2.txt', 'level3.txt']
        self.current_level = 0
        self.paused = False
        print('game instantiated...')
        
    
    # a method is a function tied to a Class
 
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'sounds')
        self.wall_img = pg.image.load(path.join(self.img_dir, 'wall_art.png')).convert_alpha()
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, "pickup.wav"))
        self.crunch_snd = pg.mixer.Sound(path.join(self.snd_dir, "crunch.wav"))
        self.map = Map(path.join(self.game_dir, map))
        print('data is loaded')

    def next_level(self, map):
        for w in self.all_walls:
            w.kill()
        for m in self.all_mobs: 
            m.kill()
        for c in self.all_coins:
            c.kill()
        for u in self.all_powerups:
            u.kill()
        # self.player.kill()
        self.load_data(map)
        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 4, 4) 
        # self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning variable...when
                    Wall(self, col, row)
                if tile == 'Pd':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row, "speed")
        # self.run()


    def new(self):
        self.load_data(self.levels[0])
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_projectiles = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        self.all_particles = pg.sprite.Group()
        # self.player = Player(self, 15, 15)
        # self.mob = Mob(self, 4, 4) 
        # self.wall = Wall(self, WIDTH/2/TILESIZE, HEIGHT/2/TILESIZE)
        for row, tiles in enumerate(self.map.data):
            for col, tile, in enumerate(tiles):
                if tile == '1':
                    # call class constructor without assigning variable...when
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row, "speed")
        # pg.mixer.music.load(path.join(self.snd_dir, "Juhani Junkala_Stage 1.ogg"))
        # pg.mixer.music.play(loops=-1)
        self.run()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.MOUSEBUTTONUP:
                print("i can get mouse input")
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_k:
                    print("i can determine when keys are pressed")

            if event.type == pg.KEYUP:
                if event.key == pg.K_k:
                    print("i can determine when keys are released")
                if event.key == pg.K_LSHIFT:
                    self.player.speed = PLAYER_SPEED
                if event.key == pg.K_p:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True

    


    def quit(self):
        pass

    def update(self):
        self.all_sprites.update()
        
        if len(self.all_powerups) < 1:
            if self.current_level >= len(self.levels)-1:
                self.current_level = 0
            else:
                self.current_level += 1
            self.next_level(self.levels[self.current_level])


    
    def draw(self):
        self.screen.fill(BLUE)
        self.draw_text("Hello World", 24, WHITE, WIDTH/2, TILESIZE)
        # self.draw_text(str(self.dt), 24, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Frames per second: " + str(floor(1/self.dt) ), 24, WHITE, WIDTH/2, HEIGHT/4)
        # self.draw_text(str(self.game_cooldown.time), 24, WHITE, WIDTH/2, HEIGHT/.5)
        self.draw_text(str(self.game_cooldown.ready()), 24, WHITE, WIDTH/2, HEIGHT/3)
        self.draw_text(str(self.player.pos), 24, WHITE, WIDTH/2, HEIGHT-TILESIZE*3)
        self.all_sprites.draw(self.screen)
        draw_health_bar(self.screen, 10, 10, self.player.health)
        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # add music for start screen here...
        self.screen.fill(BLACK)
        self.draw_text("THE BEST GAME EVAH!", 48, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def show_pause_screen(self):
        pass
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                    


if __name__ == "__main__":
    g = Game()

g.show_start_screen()

while g.running:
    g.new()


pg.quit()


    

    
