import FroPy
import pygame
import random
import os
from os import path
import map_logic
import tilemap
import camera
import settings
from settings import *
import game_entities as entities


class random_Encounter():
    def __init__(self, screen, game):
        self.player = game.player
        self.screen = screen
        self.game = game
        self.bullets = self.game.projectile_Sprite_Group
        self.mobs = self.game.enemy_Sprite_Group
        self.debug = False

        self.looping = True
        self.paused = False
        self.loop()

    def loop(self):
        # put in new random encounter

        while self.looping:
            pygame.event.get()
            self.screen.fill((0,0,0))

            cont_butt = FroPy.Button(settings.DK_PURPLE, (settings.SCREEN_WIDTH//2), (settings.SCREEN_HEIGHT - 100), 100, 40, text='Continue')
            if cont_butt.clicked(self.game.mouse_x, self.game.mouse_y):
                self.looping = False

            image = self.game.get_image('./images/cards/broken_wheel.png')
            w, h = pygame.display.get_surface().get_size()
            self.screen.blit(image, ((w // 2) - (image.get_width()//2),
                                (h// 2) - (image.get_height() //2)))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.looping = False
                    if event.key == pygame.K_h:
                        self.debug = not self.debug


            pygame.display.flip()
            pygame.time.Clock().tick(60)

        self.select_map()

        self.encounter = True
        self.camera = camera.Camera(self.map.width, self.map.height)
        self.player.x = 100
        self.player.y = 100

        while self.encounter:
            pygame.event.pump()

            self.screen.fill((0,0,0))
            if not self.paused:
                self.update()

            self.draw()  #draws the map

            pygame.time.Clock().tick(60)

    def update(self):
        self.game.all_Sprite_Group.update()
        self.camera.update(self.player)
        # mobs hit player

        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, tilemap.collide_hit_rect)
        for hit in hits:
            # todo add sound
            #if random() < 0.7:
                #choice(self.player_hit_sounds).play()
            self.player.health -= settings.MOB_DAMAGE
            hit.vel = pygame.math.Vector2(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += pygame.math.Vector2(settings.MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs

        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)



    def select_map(self):
        self.load_map('./tilesets/temptown.tmx')

    def load_map(self, filename):
        #needs random file selection per level, one level hard coded for testing
        self.map = tilemap.TiledMap(filename)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.x = obj_center.x
                self.player.y = obj_center.y
            if tile_object.name == 'indian':
                entities.Mob(self.game, self.screen, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                entities.Obstacle(self.game, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)


    def select_encounter(self):
        pass

    def select_posture(self):
        #randomly selects hostile or passive or friendly
        #only triggures on encounters with people or animals
        pass

    def draw(self):

        #todo add camera class, then add $, self.camera.apply_rect(self.map_rect)$ to the variable below
        self.screen.blit(self.map_img, (0,0))
        for sprite in self.game.all_Sprite_Group:
            if isinstance(sprite, entities.Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.debug:
                pygame.draw.rect(self.screen, settings.CYAN, self.camera.apply(sprite.hit_rect), 1 )
            if isinstance(sprite, entities.Bullet):
                sprite.draw(self.screen)
        if self.debug:
            for wall in self.game.wall_Group:
                pygame.draw.rect(self.screen, settings.CYAN, self.camera.apply_rect(wall.rect), 1)
        pygame.display.flip()







