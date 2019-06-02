import pygame
import os

player_frames = [pygame.image.load("character_frames/frame_1.gif"), pygame.image.load("character_frames/frame_2.gif"),
                 pygame.image.load("character_frames/frame_3.gif"), pygame.image.load("character_frames/frame_4.gif")]

bullet = pygame.transform.scale(pygame.image.load("pictures/bullet.png"), (50, 50))

class Player(pygame.sprite.Sprite):

    def __init__(self, start_pos=[0,0]):
        super().__init__()
        self.start_pos = start_pos
        self.cur_pos = start_pos
        self.walkcount = 0
        self.rect = player_frames[self.walkcount]
        self.reverse_frames = False
        self.player_facing = 0
        self.velocity = 20
        self.bullets = []
        self.ammo = 5
        self.fired_tick = pygame.time.get_ticks()
        self.reloading = False

    def cycle_animation(self):

        if self.reverse_frames == True:
            self.walkcount -= 1
        else:
            self.walkcount += 1

        if self.walkcount == 3:
            self.reverse_frames = True
        if self.walkcount == 0 and self.reverse_frames == True:
            self.reverse_frames = False

    def actions(self, screen, get_key, auto_reload):

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
            for bullet in self.bullets:
                self.bullets.pop(self.bullets.index(bullet))

            if len(self.bullets) == 0:
                self.reloading = False

        if pygame.key.get_pressed()[pygame.K_SPACE] and (pygame.time.get_ticks() - self.fired_tick) >= 0:
            self.fired_tick = pygame.time.get_ticks()
            if len(self.bullets) < self.ammo:

                if self.player_facing == 0:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.8), round(self.cur_pos[1]), self.player_facing))
                if self.player_facing == 1:
                    self.bullets.append(Projectile(round(self.cur_pos[0]), round(self.cur_pos[1] + self.rect.get_height() / 4), self.player_facing))
                if self.player_facing == 2:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 4), round(self.cur_pos[1] + self.rect.get_height() / 1.25), self.player_facing))
                if self.player_facing == 3:
                    self.bullets.append(Projectile(round(self.cur_pos[0] + self.rect.get_width() / 1.25), round(self.cur_pos[1] + self.rect.get_height() / 1.8), self.player_facing))
    
    def draw(self, screen):

        if self.player_facing == 0:
            screen.blit(player_frames[self.walkcount], self.cur_pos)
        if self.player_facing == 1:
            screen.blit(pygame.transform.rotate(player_frames[self.walkcount], 90), self.cur_pos)
        if self.player_facing == 2:
            screen.blit(pygame.transform.rotate(player_frames[self.walkcount], 180), self.cur_pos)
        if self.player_facing == 3:
            screen.blit(pygame.transform.rotate(player_frames[self.walkcount], -90), self.cur_pos)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.bullet = bullet
        self.direction = direction
        self.velocity = 45

    def draw(self,screen):
        if self.direction == 0:
            self.velocity = -45
            if self.y <= 960 and self.y >= 0:
                screen.blit(pygame.transform.rotate(self.bullet, 0), (self.x, self.y))
        if self.direction == 1:
            self.velocity = -45
            if self.x <= 1280 and self.x >= 0:
                screen.blit(pygame.transform.rotate(self.bullet, 90), (self.x, self.y))
        if self.direction == 2:
            self.velocity = 45
            if self.y <= 960 and self.y >= 0:
                screen.blit(pygame.transform.rotate(self.bullet, 180), (self.x, self.y))
        if self.direction == 3:
            self.velocity = 45
            if self.x <= 1280 and self.x >= 0:
                screen.blit(pygame.transform.rotate(self.bullet, -90), (self.x, self.y))