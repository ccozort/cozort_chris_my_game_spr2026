from ctypes import Array

import pygame as pg
from pygame.sprite import Sprite
from player_states import *
from settings import *
from utils import *
from  os import path
from state_machine import *
from random import randint
from random import choice
from math import floor

vec = pg.math.Vector2


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

# this function checks for x and y collision in sequence and sets the position based on collision direction
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print("collided with wall from x dir")
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            # print("collided with wall from y dir")
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_stuff(sprite, group, name, kill):
        hits = pg.sprite.spritecollide(sprite, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == name:
                return True

class Player(Sprite):
    def __init__(self, game, x, y):
        self._layer = 10  # Set layer before adding to groups
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, "sprite_sheet.png"))
        self.load_images()
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.spritesheet.get_image(0,0,TILESIZE,TILESIZE)
        self.image.set_colorkey(BLACK)
        # self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.hit_rect = PLAYER_HIT_RECT
        self.jumping = False
        self.moving = False
        self.last_update = 0
        self.current_frame = 0
        self.state_machine = StateMachine()
        self.states: Array[State] = [PlayerIdleState(self), PlayerMoveState(self), PlayerDashState(self)]
        self.state_machine.start_machine(self.states)
        self.effect_cd = Cooldown(2000)
        self.health = 100
        self.keys_enabled = True
        self.speed = PLAYER_SPEED
    def get_keys(self):
        self.vel = vec(0,0)
        if self.keys_enabled:
            keys = pg.key.get_pressed()
            if keys[pg.K_f]:
                print(' fired a projectile')
                p = Projectile(self.game, self.pos.x, self.pos.y, vec(1,1))
                p = Projectile(self.game, self.pos.x, self.pos.y, vec(0,-1))
                p = Projectile(self.game, self.pos.x, self.pos.y, vec(-1,1))
            if keys[pg.K_LSHIFT]:
                self.speed = PLAYER_DASH_SPEED
                # self.state_machine.transition("dash")
                # print(self.state_machine.current_state.get_state_name())

            if keys[pg.K_a]:
                self.vel.x = -self.speed
            if keys[pg.K_d]:
                self.vel.x = self.speed
            if keys[pg.K_w]:
                self.vel.y = -self.speed
            if keys[pg.K_s]:
                self.vel.y = self.speed
            if self.vel.x != 0 and self.vel.y != 0:
                self.vel *= 0.7071
            # else:
            #     # self.state_machine.transition("idle")
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE,0,TILESIZE, TILESIZE)]
        self.moving_frames = [self.spritesheet.get_image(TILESIZE*2,0,TILESIZE, TILESIZE), 
                                self.spritesheet.get_image(TILESIZE*3,0,TILESIZE, TILESIZE)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        for frame in self.moving_frames:
            frame.set_colorkey(BLACK)
    def effects_trail(self):
        if self.effect_cd.ready():
            EffectTrail(self.game, self.rect.x, self.rect.y)
    def animate(self):
        now = pg.time.get_ticks()
        if not self.jumping and not self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        elif self.moving:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.moving_frames)
                bottom = self.rect.bottom
                self.image = self.moving_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


    
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("i collided with a mob")
            if str(hits[0].__class__.__name__) == "Coin":
                print("i collided with a coin")
                self.game.pickup_snd.play()
            if str(hits[0].__class__.__name__) == "PowerUp":
                print("i collided with a Power Up")
            if str(hits[0].__class__.__name__) == "Wall":
                print("i collided with a Wall")
                
                self.game.crunch_snd.play()
    
    def state_check(self):
        if self.vel == vec(0,0) and self.state_machine.current_state != "dash":
            self.state_machine.transition("idle")
        pass

    def update(self):
        # print("player updating")
        # self.effects_trail()
        self.state_machine.update()
        self.get_keys()
        self.state_check()
        self.animate()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_coins, True)
        self.collide_with_stuff(self.game.all_powerups, True)
        if collide_with_stuff(self, self.game.all_walls, "Wall", True):
            # print("collided with wall")
            for p in range(100):
                particle = Particle(self.game, self.rect.x, self.rect.y, randint(5,10), randint(5,12))
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.speed = .01
    def update(self):
        # hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        # if hits:
        #     self.speed -=1
        #     # self.new_rect = pg.Rect(self.pos.x, self.pos.y, 100, 100) 
        #     # self.rect = self.new_rect
        #     # self.image.fill(RED)
        # if self.rect.x > WIDTH or self.rect.x < 0:
        #     self.speed *= -1
        #     self.pos.y += TILESIZE
        self.pos += self.vel + self.game.player.pos * self.game.dt
        self.rect.center = self.pos


class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0) 
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass



class Projectile(Sprite):
    def __init__(self, game, x, y, vel):
        self.groups = game.all_sprites, game.all_projectiles
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/2, TILESIZE/2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.vel = vel 
        self.pos = vec(x,y)
        self.speed = 500
        self.rect.center = self.pos
        print("im a real projectile...")
    def update(self):
        if collide_with_stuff(self, self.game.all_walls, "Wall", True):
            print("collided with wall")
            for p in range(100):
                particle = Particle(self.game, self.rect.x, self.rect.y, randint(5,10), randint(5,12))
        self.pos += self.vel * self.speed * self.game.dt
        self.rect.center = self.pos
       


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(0,0)
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
    def update(self):
        pass

class PowerUp(Sprite):
    def __init__(self, game, x, y, effect):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y) * TILESIZE
        self.rect.center = self.pos
        self.effect = effect
    def update(self):
        pass

# look into pooling for particles and projectiles to optimize performance instead of killing and creating new ones
class Particle(Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = randint(2,20)*choice([-1,1])
        self.speedy = randint(2,20)*choice([-1,1])
        self.countdown = Cooldown(5000)
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        self.active = True

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.active = True
    def deactivate(self):
        self.active = False
    def return_to_pool(self):
        self.deactivate()
        # add to pool logic here
    def update(self):
        self.countdown.ticking()
        self.rect.x += self.speedx
        self.rect.y += self.speedy+PLAYER_GRAV
        if collide_with_stuff(self, self.game.all_walls, "Wall", True):
            # print("collided with wall")
            for p in range(35):
                particle = Particle(self.game, self.rect.x, self.rect.y, randint(5,10), randint(5,12))
        if self.countdown.delta > 3:
            # print('time to die...')
            self.deactivate()
            self.kill()

class EffectTrail(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE,TILESIZE), pg.SRCALPHA)
        self.alpha = 255
        self.image.fill((255,255,255,255))
        self.rect = self.image.get_rect()
        self.cd = Cooldown(10)
        self.rect.x = x
        self.rect.y = y
        # coin behavior
        self.scale_x = 32
        self.scale_y = 32
    def update(self):
        if self.alpha <= 100:
            self.kill()
        try:
            self.image.set_alpha(self.alpha)
        except Exception as e:
            print(f"alpha is out of range: {e} with value {self.alpha}")
        self.image.fill((255,255,255,self.alpha))
        
        if self.cd.ready():
            self.scale_x -=1
            self.scale_y -=1
            self.alpha -= 5
            new_image = pg.transform.scale(self.image, (self.scale_x, self.scale_y))
            self.image = new_image