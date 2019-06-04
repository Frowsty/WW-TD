import pygame
import os
from time import sleep

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

YELLOW = (255, 255, 0)
DK_GREEN = (51, 102, 0)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)

#ASH - image function, loads image into an array and if it has already been loaded, it loads the previous loaded image
#instead of wasting memory on a new image. if it hasn't been it loads it.
_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
    return image

# player_frames = [pygame.transform.scale(pygame.image.load("character_frames/frame_1.png"), (200, 200)),
#                  pygame.transform.scale(pygame.image.load("character_frames/frame_2.png"), (200, 200)),
#                  pygame.transform.scale(pygame.image.load("character_frames/frame_3.png"), (200, 200)),
#                  pygame.transform.scale(pygame.image.load("character_frames/frame_4.png"), (200, 200))]

bullet = pygame.transform.scale(pygame.image.load("pictures/bullet.png"), (15, 15))
#shell = pygame.transform.scale(pygame.image.load("pictures/shell.png"), (50, 50))

class Player(pygame.sprite.Sprite):

    def __init__(self, position=[0,0]):
        super().__init__()
        self.cur_pos = position
        self.walkcount = 0
        self.player_frames = []
        self.frames = self.load_frames()
        self.rect = self.player_frames[0]
        self.reverse_frames = False
        self.player_facing = 0
        self.velocity = 20
        self.bullets = []
        self.ammo = 5
        self.fired_tick = pygame.time.get_ticks()
        self.reloading = False
        self.health = 100

    def load_frames(self):
        self.player_frames.append(get_image("character_frames/frame1.png"))
        self.player_frames.append(get_image("character_frames/frame2.png"))
        self.player_frames.append(get_image("character_frames/frame3.png"))
        self.player_frames.append(get_image("character_frames/frame4.png"))

    def cycle_animation(self):

        if self.reverse_frames == True:
            self.walkcount -= 1
        else:
            self.walkcount += 1

        if self.walkcount == 3:
            self.reverse_frames = True
        if self.walkcount == 0 and self.reverse_frames == True:
            self.reverse_frames = False

    def clamp_movement(self):
        if self.cur_pos[0] >= 1280 - self.rect.get_width():
            self.cur_pos[0] = 1280 - self.rect.get_width()
        if self.cur_pos[0] <= 0:
            self.cur_pos[0] = 0
        if self.cur_pos[1] >= 960 - self.rect.get_height():
            self.cur_pos[1] = 960 - self.rect.get_height()
        if self.cur_pos[1] <= 0:
            self.cur_pos[1] = 0

    def actions(self, auto_reload):

        if pygame.key.get_pressed()[pygame.K_w]:
            self.cur_pos[1] -= self.velocity
            self.cycle_animation()
            self.player_facing = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.cur_pos[1] += self.velocity
            self.cycle_animation()
            self.player_facing = 2
        
        if pygame.key.get_pressed()[pygame.K_a]:
            self.cur_pos[0] -= self.velocity
            self.cycle_animation()
            self.player_facing = 1

        if pygame.key.get_pressed()[pygame.K_d]:
            self.cur_pos[0] += self.velocity
            self.cycle_animation()
            self.player_facing = 3
        
        self.clamp_movement()

        for bullet in self.bullets:
            if bullet.direction == 1 or bullet.direction == 3:
                if bullet.x < 1280 and bullet.x > 0:
                    if bullet.y < 960 and bullet.y > 0:
                        bullet.x += bullet.velocity
            elif bullet.direction == 0 or bullet.direction == 2:
                if bullet.y < 960 and bullet.y > 0:
                    if bullet.x < 1280 and bullet.x > 0:
                        bullet.y += bullet.velocity

        if pygame.key.get_pressed()[pygame.K_r] or self.reloading == True or (auto_reload == True and len(self.bullets) == 5):
            self.reloading = True

            if self.bullets[-1].x >= 1280 or self.bullets[-1].x <= 0 or self.bullets[-1].y >= 960 or self.bullets[-1].y <= 0:
                for bullet in self.bullets:
                    self.bullets.pop(self.bullets.index(bullet))

                if len(self.bullets) == 0:
                    self.reloading = False

        if pygame.key.get_pressed()[pygame.K_SPACE] and (pygame.time.get_ticks() - self.fired_tick) >= 500:
            self.fired_tick = pygame.time.get_ticks()
            if len(self.bullets) < self.ammo:

                if self.player_facing == 0:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.6), round(self.cur_pos[1] + self.rect.get_height() / 8), self.player_facing))
                if self.player_facing == 1:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 8), round(self.cur_pos[1] + self.rect.get_height() / 3.2), self.player_facing))
                if self.player_facing == 2:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 3.3), round(self.cur_pos[1] + self.rect.get_height() / 1.22), self.player_facing))
                if self.player_facing == 3:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.22), round(self.cur_pos[1] + self.rect.get_height() / 1.6), self.player_facing))
    
    def draw(self, screen, font):

        if self.player_facing == 0:
            screen.blit(self.player_frames[self.walkcount], self.cur_pos)
        if self.player_facing == 1:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], 90), self.cur_pos)
        if self.player_facing == 2:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], 180), self.cur_pos)
        if self.player_facing == 3:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], -90), self.cur_pos)

        health_text = font.render(f"HEALTH: {self.health}", True, GREEN)
        screen.blit(health_text, (round((1280 / 2) - (health_text.get_width() / 2)), 5))

class Enemy(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.cur_pos = position
        self.bullets = []
        self.walkcount = 0
        self.player_frames = []
        self.frames = self.load_frames()
        self.rect = self.player_frames[0]
        self.health = 100
        self.player_facing = 0


    def load_frames(self):
        self.player_frames.append(get_image("character_frames/frame1.png"))
        self.player_frames.append(get_image("character_frames/frame2.png"))
        self.player_frames.append(get_image("character_frames/frame3.png"))
        self.player_frames.append(get_image("character_frames/frame4.png"))
    
    def actions(self, auto_reload):

        if pygame.key.get_pressed()[pygame.K_SPACE] and (pygame.time.get_ticks() - self.fired_tick) >= 500:
            self.fired_tick = pygame.time.get_ticks()
            if len(self.bullets) < self.ammo:

                if self.player_facing == 0:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.6), round(self.cur_pos[1] + self.rect.get_height() / 8), self.player_facing))
                if self.player_facing == 1:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 8), round(self.cur_pos[1] + self.rect.get_height() / 3.2), self.player_facing))
                if self.player_facing == 2:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 3.3), round(self.cur_pos[1] + self.rect.get_height() / 1.22), self.player_facing))
                if self.player_facing == 3:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.22), round(self.cur_pos[1] + self.rect.get_height() / 1.6), self.player_facing))
    
    def draw(self, screen):

        if self.player_facing == 0:
            screen.blit(self.player_frames[self.walkcount], self.cur_pos)
        if self.player_facing == 1:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], 90), self.cur_pos)
        if self.player_facing == 2:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], 180), self.cur_pos)
        if self.player_facing == 3:
            screen.blit(pygame.transform.rotate(self.player_frames[self.walkcount], -90), self.cur_pos)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.bullet = ""
        self.direction = direction
        self.velocity = 45
        self.hit_target = False

    def draw(self,screen, bullet_img):
        self.bullet = bullet_img

        if self.hit_target == False:
            if self.direction == 0:
                self.velocity = -45
                if self.y < 960 and self.y > 0:
                    screen.blit(pygame.transform.rotate(self.bullet, 0), (self.x, self.y))
            if self.direction == 1:
                self.velocity = -45
                if self.x < 1280 and self.x > 0:
                    screen.blit(pygame.transform.rotate(self.bullet, 90), (self.x, self.y))
            if self.direction == 2:
                self.velocity = 45
                if self.y < 960 and self.y > 0:
                    screen.blit(pygame.transform.rotate(self.bullet, 180), (self.x, self.y))
            if self.direction == 3:
                self.velocity = 45
                if self.x < 1280 and self.x > 0:
                    screen.blit(pygame.transform.rotate(self.bullet, -90), (self.x, self.y))

