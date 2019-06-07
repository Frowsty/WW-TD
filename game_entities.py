import pygame
import os
import math
from random import choice
from time import sleep

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)

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

# bullet = pygame.transform.scale(pygame.image.load("pictures/bullet.png"), (25, 25))
#shell = pygame.transform.scale(pygame.image.load("pictures/shell.png"), (50, 50))

class Player(pygame.sprite.Sprite):

    def __init__(self, position=[0,0]):
        super().__init__()
        self.cur_pos = position
        self.reload_frame = 0
        self.player_frames = []
        self.frames = self.load_frames()
        self.reverse_frames = False
        self.player_facing = 0
        self.velocity = 20
        self.bullets = []
        self.ammo = 5
        self.fired_tick = pygame.time.get_ticks()
        self.reload_tick = pygame.time.get_ticks()
        self.reloading = False
        self.health = 100
        self.health_color = GREEN
        self.dead = False
        self.should_knockback = False
        self.knockback = 0
        self.damage = 0
        self.mode = ""
        self.max_health = 100

    def load_frames(self):
        self.player_frames.append(get_image("character_frames/character_main.png"))
        self.player_frames.append(get_image("character_frames/character_reload.png"))

    # def cycle_animation(self):

    #     if self.reverse_frames == True:
    #         self.walkcount -= 1
    #     else:
    #         self.walkcount += 1

    #     if self.walkcount == 3:
    #         self.reverse_frames = True
    #     if self.walkcount == 0 and self.reverse_frames == True:
    #         self.reverse_frames = False

    def health_bar(self, screen):

        if self.health > 75:
            self.health_color = GREEN
        elif self.health > 45 and self.health < 75:
            self.health_color = YELLOW
        elif self.health > 25 and self.health < 45:
            self.health_color = ORANGE
        elif self.health > 0 and self.health < 25:
            self.health_color = RED

        pygame.draw.line(screen, self.health_color, (self.cur_pos[0], self.cur_pos[1] - 10), 
                        (self.cur_pos[0] + self.player_frames[0].get_width() * (self.health / 100), self.cur_pos[1] - 10), 5)
        
        # Healthbar outline
        # TOP
        pygame.draw.line(screen, BLACK, (self.cur_pos[0], self.cur_pos[1] - 14), 
                        (self.cur_pos[0] + self.player_frames[0].get_width() + 1, self.cur_pos[1] - 14), 2)
        # BOTTOM
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] - 2, self.cur_pos[1] - 8), 
                        (self.cur_pos[0] + self.player_frames[0].get_width() + 2, self.cur_pos[1] - 8), 2)
        # LEFT
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] - 2, self.cur_pos[1] - 14), 
                        (self.cur_pos[0] - 2, self.cur_pos[1] - 8), 2)
        # RIGHT
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] + self.player_frames[0].get_width() + 1, self.cur_pos[1] - 14), 
                        (self.cur_pos[0] + self.player_frames[0].get_width() + 1, self.cur_pos[1] - 8), 2)

    def clamp_movement(self):
        if self.cur_pos[0] >= 1280 - self.player_frames[0].get_width() - 50:
            self.cur_pos[0] = 1280 - self.player_frames[0].get_width() - 50
        if self.cur_pos[0] <= 50:
            self.cur_pos[0] = 50
        if self.cur_pos[1] >= 960 - self.player_frames[0].get_height() - 50:
            self.cur_pos[1] = 960 - self.player_frames[0].get_height() - 50
        if self.cur_pos[1] <= 50:
            self.cur_pos[1] = 50
    
    def update_settings(self):
        
        if self.mode == "EASY":
            self.damage = 50
            self.health = 100
        if self.mode == "MEDIUM":
            self.damage = 34
            self.health = 75
        if self.mode == "HARD":
            self.damage = 25
            self.health = 50

    def actions(self, auto_reload):

        if pygame.key.get_pressed()[pygame.K_w]:
            self.cur_pos[1] -= self.velocity
            self.player_facing = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.cur_pos[1] += self.velocity
            self.player_facing = 2
        
        if pygame.key.get_pressed()[pygame.K_a]:
            self.cur_pos[0] -= self.velocity
            self.player_facing = 1

        if pygame.key.get_pressed()[pygame.K_d]:
            self.cur_pos[0] += self.velocity
            self.player_facing = 3
        
        #self.cycle_animation()
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

        if pygame.key.get_pressed()[pygame.K_r] or self.reloading == True or (auto_reload == True and len(self.bullets) == self.ammo):
            if len(self.bullets) != 0:   
                self.reloading = True

                if self.bullets[-1].x >= 1280 or self.bullets[-1].x <= 0 or self.bullets[-1].y >= 960 or self.bullets[-1].y <= 0:
                    for bullet in self.bullets:
                        if (pygame.time.get_ticks() - self.reload_tick) >= 350:
                            self.bullets.pop(self.bullets.index(bullet))
                            self.reload_frame = 1
                            self.reload_tick = pygame.time.get_ticks()

                    if len(self.bullets) == 0:
                        self.reloading = False
                        self.reload_frame = 0

        if pygame.key.get_pressed()[pygame.K_SPACE] and (pygame.time.get_ticks() - self.fired_tick) >= 750 and self.reloading == False:
            self.fired_tick = pygame.time.get_ticks()
            if len(self.bullets) < self.ammo:

                if self.player_facing == 0:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.player_frames[0].get_width() / 2), 
                                                   round(self.cur_pos[1] - 10), self.player_facing, self.damage))
                if self.player_facing == 1:
                    self.bullets.append(Projectile(round(self.cur_pos[0] - 10),
                                                   round(self.cur_pos[1] + 8), self.player_facing, self.damage))
                if self.player_facing == 2:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + 8), 
                                                   round(self.cur_pos[1] + self.player_frames[0].get_height() + 11), self.player_facing, self.damage))
                if self.player_facing == 3:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.player_frames[0].get_width()),
                                                   round(self.cur_pos[1] + self.player_frames[0].get_height() / 1.6), self.player_facing, self.damage))
    
    def draw(self, screen, font, show_healthbar):

        if self.mode == "EASY":
            self.max_health = 100
        if self.mode == "MEDIUM":
            self.max_health = 75
        if self.mode == "HARD":
            self.max_health = 50

        if self.health <= 0:
            self.health = 0
        if self.health >= self.max_health:
            self.health = self.max_health
        
        if self.ammo != 10 and len(self.bullets) > 5:
            for i in range(5):
                self.bullets.pop()
        
        if self.health > 0:
            if self.player_facing == 0:
                screen.blit(pygame.transform.rotate(self.player_frames[self.reload_frame], 90), self.cur_pos)
            if self.player_facing == 1:
                screen.blit(pygame.transform.rotate(self.player_frames[self.reload_frame], 180), self.cur_pos)
            if self.player_facing == 2:
                screen.blit(pygame.transform.rotate(self.player_frames[self.reload_frame], -90), self.cur_pos)
            if self.player_facing == 3:
                screen.blit(self.player_frames[self.reload_frame], self.cur_pos)
        else:
            self.dead = True

        if show_healthbar == True:
            self.health_bar(screen)

class Enemy(pygame.sprite.Sprite):

    def __init__(self, position):
        super().__init__()
        self.cur_pos = position
        self.bullets = []
        self.player_frame = get_image("character_frames/enemy_knife.png")
        # self.frames = self.load_frames()
        self.health = 100
        self.speed = 20
        self.damage = 15
        self.accelerate = pygame.math.Vector2(0, 0)
        self.hit_target_tick = pygame.time.get_ticks()
        self.hit_player = False
        self.direction = pygame.math.Vector2(0,0)


    # def load_frames(self):
    #     self.player_frames.append(get_image("character_frames/frame1.png"))
    #     self.player_frames.append(get_image("character_frames/frame2.png"))
    #     self.player_frames.append(get_image("character_frames/frame3.png"))
    #     self.player_frames.append(get_image("character_frames/frame4.png"))
    
    # def actions(self, player_pos):

    def health_bar(self, screen):

        if self.health > 75:
            self.health_color = GREEN
        elif self.health > 45 and self.health < 75:
            self.health_color = YELLOW
        elif self.health > 25 and self.health < 45:
            self.health_color = ORANGE
        elif self.health > 0 and self.health < 25:
            self.health_color = RED

        # The Healthbar
        pygame.draw.line(screen, self.health_color, (self.cur_pos[0], self.cur_pos[1] - 15), 
                        (self.cur_pos[0] + self.player_frame.get_width() * (self.health / 100), self.cur_pos[1] - 15), 5)

        # Healthbar outline
        # TOP
        pygame.draw.line(screen, BLACK, (self.cur_pos[0], self.cur_pos[1] - 18), 
                        (self.cur_pos[0] + self.player_frame.get_width() + 1, self.cur_pos[1] - 18), 2)
        # BOTTOM
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] - 2, self.cur_pos[1] - 12), 
                        (self.cur_pos[0] + self.player_frame.get_width() + 2, self.cur_pos[1] - 12), 2)
        # LEFT
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] - 2, self.cur_pos[1] - 18), 
                        (self.cur_pos[0] - 2, self.cur_pos[1] - 12), 2)
        # RIGHT
        pygame.draw.line(screen, BLACK, (self.cur_pos[0] + self.player_frame.get_width() + 1, self.cur_pos[1] - 18), 
                        (self.cur_pos[0] + self.player_frame.get_width() + 1, self.cur_pos[1] - 12), 2)
        
    def clamp_movement(self):
        if self.cur_pos[0] >= 1280 - self.player_frame.get_width() - 50:
            self.cur_pos[0] = 1280 - self.player_frame.get_width() - 50
        if self.cur_pos[0] <= 50:
            self.cur_pos[0] = 50
        if self.cur_pos[1] >= 960 - self.player_frame.get_height() - 50:
            self.cur_pos[1] = 960 - self.player_frame.get_height() - 50
        if self.cur_pos[1] <= 50:
            self.cur_pos[1] = 50

    def update_settings(self, game_mode):

        if game_mode == "EASY":
            self.damage = 10
        if game_mode == "MEDIUM":
            self.damage = 15
        if game_mode == "HARD":
            self.damage = 25

    def collision_check(self, player_pos, player_frame):
        if self.cur_pos[0] >= player_pos[0] and self.cur_pos[0] <= player_pos[0] + player_frame.get_width():
            if self.cur_pos[1] >= player_pos[1] and self.cur_pos[1] <= player_pos[1] + player_frame.get_height() and (pygame.time.get_ticks() - self.hit_target_tick) >= 500:
                self.hit_target_tick = pygame.time.get_ticks()
                self.hit_player = True

    def draw(self, screen, player_pos, player_frame, fps, is_player_dead, show_healthbar):
        if self.health <= 0:
            self.health = 0

        if self.health > 0:
            self.direction = (pygame.math.Vector2(player_pos) - pygame.math.Vector2(self.cur_pos)).angle_to(pygame.math.Vector2(1, 0))
            screen.blit(pygame.transform.rotate(self.player_frame, self.direction), self.cur_pos)
            self.player_frame.get_rect().center = pygame.math.Vector2(self.cur_pos)
            if is_player_dead == False:
                self.accelerate = pygame.math.Vector2(self.speed , 0).rotate(-self.direction)
            else:
                self.accelerate = pygame.math.Vector2(0, 0)
            self.cur_pos += self.accelerate * fps + (self.speed * 80) * self.accelerate * fps ** 2
            self.player_frame.get_rect().center = pygame.math.Vector2(self.cur_pos)

            self.collision_check(player_pos, player_frame)
            self.clamp_movement()
        
        if show_healthbar == True:
            self.health_bar(screen)

class Projectile(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, damage):
        super().__init__()
        self.x = x
        self.y = y
        self.bullet = ""
        self.direction = direction
        self.velocity = 45
        self.hit_target = False
        self.damage = damage

    def collision_check(self, enemy_pos, enemy_frame):
        if self.x >= enemy_pos[0] and self.x <= enemy_pos[0] + enemy_frame.get_width():
            if self.y >= enemy_pos[1] and self.y <= enemy_pos[1] + enemy_frame.get_height():
                self.hit_target = True
                self.x = -50
                self.y = -50

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

class PowerUp(pygame.sprite.Sprite):

    def __init__(self, screen, attribute, pos, called_tick):
        super().__init__()
        self.pos = pos
        self.attribute = attribute
        self.screen = screen
        self.colors = [RED, GREEN, BLUE, PURPLE, ORANGE]
        self.activate = False
        self.activate_attrib = ""
        self.called_tick = called_tick
        self.draw = True
        self.clicked_tick = 0

    def run(self, shell_img):
        if self.draw == True:
            self.pos[1] += 10
            if self.attribute == 1:
                pygame.draw.circle(self.screen, choice(self.colors), (self.pos[0], self.pos[1]), 25)
                self.screen.blit(shell_img, (self.pos[0] - 35, self.pos[1] - 20))
                self.screen.blit(shell_img, (self.pos[0] - 25, self.pos[1] - 20))
                self.screen.blit(shell_img, (self.pos[0] - 15, self.pos[1] - 20))
            
            if self.attribute == 2:
                pygame.draw.circle(self.screen, choice(self.colors), (self.pos[0], self.pos[1]), 25)
                self.screen.blit(pygame.transform.scale(shell_img, (60, 60)), (self.pos[0] - 33, self.pos[1] - 30))
            
            if self.attribute == 3:
                pygame.draw.circle(self.screen, choice(self.colors), (self.pos[0], self.pos[1]), 25)
                pygame.draw.line(self.screen, DARK_RED, (self.pos[0] - 15, self.pos[1]), (self.pos[0] + 15, self.pos[1]), 5)
                pygame.draw.line(self.screen, DARK_RED, (self.pos[0], self.pos[1] - 15), (self.pos[0], self.pos[1] + 15), 5)

    def return_attribute(self, mouse_x, mouse_y):
        if mouse_x < self.pos[0] + 25 and mouse_x > self.pos[0] - 25:
            if mouse_y < self.pos[1] + 25 and mouse_y > self.pos[1] - 25:
                if pygame.mouse.get_pressed()[0] == True:
                    if self.attribute == 1:
                        self.activate_attrib = "increase ammo"
                    elif self.attribute == 2:
                        self.activate_attrib = "increase damage"
                    elif self.attribute == 3:
                        self.activate_attrib = "increase health"
                    self.clicked_tick = pygame.time.get_ticks()