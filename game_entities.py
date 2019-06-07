import pygame
from tilemap import collide_hit_rect
from random import uniform, choice, randint, random
import os
import math
from time import sleep
import settings
from settings import *

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

# def collision(player, enemy, bullet):
#     # collisions
#
#     if enemy.hit_player == True:
#         player.health -= 15
#         player.cur_pos += pygame.math.Vector2(75, 0).rotate(-enemy.direction)
#         enemy.hit_player = False
#
#     for enemy in self.game.enemy_Sprite_Group:
#         bullet.collision_check(enemy.cur_pos, enemy.player_frame)
#         if bullet.hit_target == True:
#             enemy.health -= bullet.damage
#             enemies.pop(enemies.index(enemy))
#             bullet.hit_target = False


class Player(pygame.sprite.Sprite):

    def __init__(self, game, screen, x, y, auto_reload = False ):
        self.screen = screen
        self.groups = game.all_Sprite_Group, game.player_Sprite_Group
        self.game = game
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.auto_reload = auto_reload
        self.font = self.game.ammo_font

        self.player_frames = []
        self.frames = self.load_frames()

        self.image = self.player_frames[0]

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.hit_rect = settings.PLAYER_HIT_RECT

        self.vel = pygame.math.Vector2(0,0)
        self.pos = pygame.math.Vector2(self.rect.centerx,self.rect.centery)
        self.rot = 0  #rotation
        self.last_shot = pygame.time.get_ticks()
        self.health = settings.PLAYER_HEALTH
        self.weapon = 'pistol'
        self.walkcount = 0

        self.ammo_loaded = 6
        self.bullets = []
        self.reload_tick = pygame.time.get_ticks()
        self.reloading = False
        self.damaged = False
        self.health_color = GREEN
        self.dead = False
        self.should_knockback = False
        self.knockback = 0
        self.bullet_img = pygame.transform.scale(self.game.get_image_convert_alpha("pictures/bullet.png"), (10, 10))
        self.shell_img = self.game.get_image_convert_alpha("pictures/shell.png")



    def load_frames(self):
        self.player_frames.append(self.game.get_image("character_frames/character_main.png"))
        self.player_frames.append(self.game.get_image("character_frames/character_reload.png"))


    def ammo_reload_toggle(self, state):
        self.ammo_reload = state

    def get_keys(self):
        self.rot_speed = 0
        self.vel = pygame.math.Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rot_speed = settings.PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rot_speed = -settings.PLAYER_ROT_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = pygame.math.Vector2(settings.PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = pygame.math.Vector2(-settings.PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pygame.K_SPACE]:
            if self.ammo_loaded > 0:
                self.shoot()
            elif self.ammo_reload:
                self.reload()

        if keys[pygame.K_r]:
            if self.ammo_loaded != 6:
                self.reload()

    def reload(self):
        for i in range(6-self.ammo_loaded):
            if (pygame.time.get_ticks() - self.reload_tick) >= 250:
                self.ammo_loaded += 1
                self.walkcount = 1
                self.reload_tick = pygame.time.get_ticks()
        self.walkcount = 0

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(settings.DAMAGE_ALPHA * 4)

    def update(self):
        #todo see fi this works...
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.image, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.pos += self.vel * self.game.dt  #position is = position + velocity * deltatime
        self.hit_rect.centerx = self.pos.x - (self.image.get_width()//2) - 13
        collide_with_walls(self, self.game.wall_Group, 'x')
        self.hit_rect.centery = self.pos.y - (self.image.get_height()//2)
        collide_with_walls(self, self.game.wall_Group, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            self.ammo_loaded -=1
            dir = pygame.math.Vector2(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = pygame.math.Vector2(-settings.WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(settings.WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-settings.WEAPONS[self.weapon]['spread'], settings.WEAPONS[self.weapon]['spread'])
                Bullet(self.game, self, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                #todo add sound
                #snd = choice(self.game.weapon_sounds[self.weapon])
                # if snd.get_num_channels() > 2:
                #     snd.stop()
                # snd.play()
            MuzzleFlash(self.game, pos)



class Mob(pygame.sprite.Sprite):
    def __init__(self, game, screen, x, y):
        self.game = game
        self.screen = screen
        self._layer = settings.MOB_LAYER
        self.groups = self.game.all_Sprite_Group, game.enemy_Sprite_Group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = self.game.get_image("character_frames/enemy_knife.png").copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.hit_rect = settings.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.rect.center = self.pos
        self.walkcount = 0
        self.rot = 0
        self.health = settings.MOB_HEALTH
        self.speed = choice(settings.MOB_SPEEDS)
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.enemy_Sprite_Group:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < settings.AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < settings.DETECT_RADIUS**2:
            if random() < 0.002:
                choice(self.game.zombie_moan_sounds).play()
                #todo replace zombie sound with indian sound
            self.rot = target_dist.angle_to(pygame.math.Vector2(1, 0))
            self.image = pygame.transform.rotate(self.game.mob_img, self.rot)
            self.rect.center = self.pos
            self.acc = pygame.math.Vector2(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            #todo replace with indian sounds
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - pygame.math.Vector2(32, 32))

    def draw_health(self):
        if self.health > 60:
            col = GREEN
        elif self.health > 30:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / settings.MOB_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < settings.MOB_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)




class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, player, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_Sprite_Group, game.projectile_Sprite_Group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = player
        self.image = self.game.bullet_images[settings.WEAPONS[self.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pygame.math.Vector2(pos)
        self.rect.center = pos
        #spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir * WEAPONS[self.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pygame.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pygame.sprite.spritecollideany(self, self.game.wall_Group ):
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > WEAPONS[self.player.weapon]['bullet_lifetime']:
            self.kill()



class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_Sprite_Group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pygame.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > settings.FLASH_DURATION:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = self.game.wall_Group
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y