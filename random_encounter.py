import pygame
import random

import os
from os import path
import map_logic
import tilemap
from tilemap import *
import camera
import ui_components as ui
import game_entities as entities
import settings

from settings import *

vec = pygame.math.Vector2

_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
    return image


def get_image_convert_alpha(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
    return image


class random_Encounter():
    def __init__(self, screen, player, player_group, all_sprite_group, enemies, projectile_group, objective_group, walls, dt):
        self.all_Sprite_Group = all_sprite_group
        self.dt = dt
        self.enemies = enemies
        self.player = player
        self.player_group = player_group
        self.screen = screen
        self.looping = True
        self.projectile_group = projectile_group
        self.objective_group = objective_group
        self.walls = walls
        self.draw_debug = False
        for wall in self.walls:
            wall.move(-1000, -1000)
            del wall
        for enemy in self.enemies:
            enemy.kill()
        self.loop()








    def loop(self):

        while self.looping:
            pygame.event.get()
            self.screen.fill((0,0,0))
            image = get_image('./images/cards/broken_wheel.png')
            w, h = pygame.display.get_surface().get_size()
            self.screen.blit(image, ((w // 2) - (image.get_width()//2),
                                (h// 2) - (image.get_height() //2)))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.looping = False


            pygame.display.flip()
            pygame.time.Clock().tick(60)

        self.select_map()
        self.camcam = camera.Camera(self.map.width, self.map.height)
        self.max_num_enemies = 0
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.move_rect(obj_center.x, obj_center.y)
            if tile_object.name == 'enemy':
                self.max_num_enemies +=1
            if tile_object.name == 'map':
                entities.Objective(tile_object.x, tile_object.y,
                                   tile_object.width, tile_object.height, self.objective_group)
            if tile_object.name == 'wall':
                entities.Obstacle(tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height, self.walls)
        self.num_of_enemies = random.randint(1, self.max_num_enemies)
        for tile_object in self.map.tmxdata.objects:
            if self.num_of_enemies == 0:
                break
            else:
                self.num_of_enemies -= 1
                if tile_object.name == 'enemy':
                    entities.Enemy(obj_center.x, obj_center.y, self.enemies, self.screen, self.player, self.walls, self.dt,
                                   self.camcam, self.all_Sprite_Group)


        self.encounter = True

        pygame.event.clear()


        self.player.vel = pygame.math.Vector2(0,0)
        while self.encounter:
            self.screen.fill((0, 0, 0))
            #updates and keyinput
            events = pygame.event.get()
            self.player.pass_events(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                        self.draw_debug = not self.draw_debug
            self.all_Sprite_Group.update()

            for sprite in self.enemies:
                self.camcam.update(sprite)

            self.camcam.update(self.player)
            self.enemies.update()

            self.player.ammo_reload_toggle(ui.auto_reload.get_state())

            self.draw()

            #collision detection
            # enemy hits player
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False, collide_hit_rect)
            for hit in hits:
                if random.random() < 0.7:
                    random.choice(phs).play()
                self.player.health -= settings.MOB_DAMAGE
                hit.vel = vec(0, 0)
            if hits:
                self.player.hit()
                self.player.vel += pygame.math.Vector2(75, 0).rotate(-hit.rot)
            # bullets hit enemys
            hits = pygame.sprite.groupcollide(self.enemies, self.projectile_group, False, True)
            for enemy in hits:
                for bullet in hits[enemy]:
                    enemy.health -= bullet.damage
                enemy.vel = vec(0, 0)

            hits = pygame.sprite.spritecollide(self.player, self.objective_group, False, collide_hit_rect)
            if hits:
                if len(self.enemies) < 1:
                    break



            pygame.display.flip()
            if self.draw_debug:
                print("flipping the display")
            print(len(self.enemies))
            pygame.time.Clock().tick(60)


    def select_map(self):
        self.load_map('./tilesets/random1.tmx')

    def load_map(self, filename):
        #needs random file selection per level, one level hard coded for testing
        self.map = tilemap.TiledMap(filename)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map.rect = self.map_rect


    def select_encounter(self):
        pass

    def select_posture(self):
        #randomly selects hostile or passive or friendly
        #only triggures on encounters with people or animals
        pass

    def draw(self):
        # draw
        mouse_x, mouse_y = pygame.mouse.get_pos()
        ammo_font = pygame.font.SysFont("Arial", 30)
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 20)
        shell_img = get_image_convert_alpha("pictures/shell.png")
        self.screen.blit(self.map_img, self.camcam.apply(self.map))
        ui.ingame_interface(self.screen, mouse_x, mouse_y, self.player.current_ammo, ammo_font, font, clock, shell_img)

        for sprite in self.all_Sprite_Group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
        for sprite in self.enemies:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
        for sprite in self.player_group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))


        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camcam.apply_rect(wall.rect), 2)



