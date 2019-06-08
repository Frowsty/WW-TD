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
        self.pick_a_card()
        self.loop()


    def pick_a_card(self):
        self.type, self.card = random.choice(list(settings.CARDS.items()))

        print(self.type)





    def loop(self):

        while self.looping:
            pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.looping = False
            self.screen.fill((0,0,0))
            image = get_image(self.card)
            w, h = pygame.display.get_surface().get_size()
            self.screen.blit(image, ((w // 2) - (image.get_width()//2),
                                (h// 2) - (image.get_height() //2)))
            font = pygame.font.Font(self.player.font, 38)
            text = 'Press Enter to continue...'
            text = pygame.font.Font.render(font, text, False, settings.WHITE)
            self.screen.blit(text, (settings.SCREEN_WIDTH//2 - (text.get_width()//2), settings.SCREEN_HEIGHT - 80))



            pygame.display.flip()
            pygame.time.Clock().tick(60)

        self.select_map()
        self.select_encounter()




    def select_map(self):
        available_maps = ['./tilesets/random1.tmx', './tilesets/random2.tmx', './tilesets/random3.tmx']
        self.load_map(random.choice(available_maps))

    def load_map(self, filename):
        #needs random file selection per level, one level hard coded for testing
        self.map = tilemap.TiledMap(filename)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map.rect = self.map_rect


    def select_encounter(self):
        scenarios = {'attack': Scenario1, 'tip': Scenario2, 'wheel': Scenario3}

        scene = scenarios[self.type]

        self.scenario = scene(self.map, self.map_img, self.player,
                        self.objective_group, self.walls, self.all_Sprite_Group,
                        self.enemies, self.projectile_group, self.screen, self.dt,
                        self.player_group, self.type)

        pass

    def select_posture(self):
        #randomly selects hostile or passive or friendly
        #only triggures on encounters with people or animals
        pass





class Scenario1():
    def __init__(self, map, map_img, player, objective_group, walls, all_sprite_group, enemies, projectile,
                 screen, dt, player_group, type):
        print("defend the wagon")
        self.type = type
        #passed through variables
        self.player_group = player_group
        self.objective_group = objective_group
        self.projectile_group = projectile
        self.walls = walls
        self.all_Sprite_Group = all_sprite_group
        self.enemies = enemies
        self.map = map
        self.map_img = map_img
        self.map_rect = self.map_img.get_rect()
        self.map.rect = self.map_rect
        self.player = player
        self.screen = screen
        self.dt = dt

        #class variables
        self.draw_debug = False
        self.max_num_enemies = 0
        self.encounter = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.ammo_font = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()
        self.shell_img = get_image_convert_alpha("pictures/shell.png")
        self.player.reload('silent')
        #load map
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load('./sounds/under_attack_music.wav')
        self.load_map()


    def load_map(self):
        #setting up the map


        self.text_box = entities.Text_Box('./text/.json', self.screen)
        for sprite in self.enemies:
            sprite.kill()

        self.camcam = camera.Camera(self.map.width, self.map.height)
        self.player.in_camera(self.camcam)


        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.move_rect(obj_center.x, obj_center.y)
            if tile_object.name == 'enemy':
                self.max_num_enemies += 1
            if tile_object.name == 'map':
                entities.Objective(tile_object.x, tile_object.y,
                                   tile_object.width, tile_object.height, self.objective_group)
            if tile_object.name == 'wall':
                entities.Obstacle(tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height, self.walls)
        self.num_of_enemies = random.randint(1, self.max_num_enemies)
        if self.num_of_enemies > 1:
            pass
        else:
            self.num_of_enemies = 1
        self.counter = entities.Counter(self.num_of_enemies, self.all_Sprite_Group)
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if self.num_of_enemies == 0:
                break
            else:
                self.num_of_enemies -= 1
                if tile_object.name == 'enemy':
                    entities.Enemy(obj_center.x, obj_center.y, self.enemies, self.screen, self.player, self.walls,
                                   self.dt,
                                   self.camcam, self.all_Sprite_Group, self.counter)


        pygame.event.clear()
        self.player.vel = pygame.math.Vector2(0, 0)
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play(-1)
        #start the loop
        self.loop()

    def loop(self):
        while self.encounter:
            self.screen.fill((0, 0, 0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            # updates and keyinput
            events = pygame.event.get()
            self.player.pass_events(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    print(self.num_of_enemies)

            for sprite in self.all_Sprite_Group:
                self.camcam.update(sprite)
                sprite.update()
            for sprite in self.enemies:
                self.camcam.update(sprite)

            self.camcam.update(self.player)
            self.enemies.update()

            self.player.ammo_reload_toggle(ui.auto_reload.get_state())

            self.draw()


            # collision detection
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

            pygame.time.Clock().tick(60)

    def draw(self):
        # draw
        self.screen.blit(self.map_img, self.camcam.apply(self.map))
        ui.ingame_interface(self.screen, self.mouse_x, self.mouse_y, self.player.current_ammo,
                            self.ammo_font, self.font, self.clock, self.shell_img)

        for sprite in self.all_Sprite_Group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
            try:
                if ui.show_healthbar.get_state():
                    sprite.health_bar(self.camcam)
            except:
                pass
        self.screen.blit(self.counter.image, self.camcam.apply(self.counter.image))
        self.player.draw()
        for sprite in self.enemies:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
            if ui.show_healthbar.get_state():
                sprite.health_bar()


        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camcam.apply_rect(wall.rect), 2)
            for objective in self.objective_group:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camcam.apply_rect(objective.rect), 2)



class Scenario2():
    def __init__(self, map, map_img, player, objective_group, walls, all_sprite_group, enemies, projectile,
                 screen, dt, player_group, type):
        #passed through variables
        self.type = type
        print("Collect the items")
        self.player_group = player_group
        self.objective_group = objective_group
        self.projectile_group = projectile
        self.walls = walls
        self.all_Sprite_Group = all_sprite_group
        self.enemies = enemies
        self.map = map
        self.map_img = map_img
        self.map_rect = self.map_img.get_rect()
        self.map.rect = self.map_rect
        self.player = player
        self.screen = screen
        self.dt = dt

        #class variables
        self.draw_debug = False
        self.max_num_items = 1
        self.encounter = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.ammo_font = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()
        self.shell_img = get_image_convert_alpha("pictures/shell.png")
        self.player.reload('silent')
        #load map
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load('./sounds/tipped_music.wav')
        self.load_map()

    def load_map(self):
        #setting up the map
        self.text_box = entities.Text_Box('./text/lost_items.json', self.screen)
        self.camcam = camera.Camera(self.map.width, self.map.height)
        self.player.in_camera(self.camcam)


        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.move_rect(obj_center.x, obj_center.y)
            if tile_object.name == 'food':
                self.max_num_items += 1
            if tile_object.name == 'map':
                entities.Objective(tile_object.x, tile_object.y,
                                   tile_object.width, tile_object.height, self.objective_group)
            if tile_object.name == 'wall':
                entities.Obstacle(tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height, self.walls)
        if self.max_num_items > 1:
            self.max_num_items -= 1
        else:
            self.max_num_items = 1
        self.num_of_items = random.randint(1, self.max_num_items)
        self.counter = entities.Counter(self.num_of_items, self.all_Sprite_Group)
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if self.num_of_items == 0:
                break
            else:
                self.num_of_items -= 1
                if tile_object.name == 'food':
                    entities.food(obj_center.x, obj_center.y, self.enemies, self.screen, self.player, self.walls,
                                   self.dt,
                                   self.camcam, self.all_Sprite_Group, self.counter, self.player.item_group)

            hits = pygame.sprite.spritecollide(self.player, self.objective_group, False, collide_hit_rect)
            if hits:
                if len(self.enemies) < 1:
                    break

        pygame.event.clear()
        self.player.vel = pygame.math.Vector2(0, 0)

        #start the loop
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play(-1)
        self.loop()

    def loop(self):
        while self.encounter:

            self.screen.fill((0, 0, 0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            # updates and keyinput
            events = pygame.event.get()
            self.player.pass_events(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    print(self.num_of_items)

            for sprite in self.all_Sprite_Group:
                self.camcam.update(sprite)
                sprite.update()


            self.camcam.update(self.player)


            self.player.ammo_reload_toggle(ui.auto_reload.get_state())

            self.draw()


            # collision detection
            # enemy hits player
            hits = pygame.sprite.spritecollide(self.player, self.player.item_group, False, collide_hit_rect)
            for hit in hits:
                self.counter.adj(1)
                self.player.pickup_snd()
                hit.kill()




            hits = pygame.sprite.spritecollide(self.player, self.objective_group, False, collide_hit_rect)
            if hits:
                if len(self.player.item_group) < 1:
                    break

            pygame.display.flip()
            if self.draw_debug:
                print("flipping the display")

            pygame.time.Clock().tick(60)

    def draw(self):
        # draw
        self.screen.blit(self.map_img, self.camcam.apply(self.map))
        ui.ingame_interface(self.screen, self.mouse_x, self.mouse_y, self.player.current_ammo,
                            self.ammo_font, self.font, self.clock, self.shell_img)

        for sprite in self.all_Sprite_Group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
            try:
                if ui.show_healthbar.get_state():
                    sprite.health_bar(self.camcam)
            except:
                pass
        self.screen.blit(self.counter.image, self.camcam.apply(self.counter.image))
        self.player.draw()
        for sprite in self.player.item_group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))


        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camcam.apply_rect(wall.rect), 2)


class Scenario3():
    def __init__(self, map, map_img, player, objective_group, walls, all_sprite_group, enemies, projectile,
                 screen, dt, player_group, type):
        self.type = type
        #passed through variables
        print("Collect the scrap")
        self.player_group = player_group
        self.objective_group = objective_group
        self.projectile_group = projectile
        self.walls = walls
        self.all_Sprite_Group = all_sprite_group
        self.enemies = enemies
        self.map = map
        self.map_img = map_img
        self.map_rect = self.map_img.get_rect()
        self.map.rect = self.map_rect
        self.player = player
        self.screen = screen
        self.dt = dt

        #class variables
        self.draw_debug = False
        self.max_num_items = 1
        self.encounter = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 60)
        self.ammo_font = pygame.font.SysFont("Arial", 30)
        self.clock = pygame.time.Clock()
        self.shell_img = get_image_convert_alpha("pictures/shell.png")

        #load map
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.load('./sounds/scrap.wav')
        self.load_map()

    def load_map(self):
        #setting up the map
        self.text_box('./text/wagon_wheel.json')
        self.camcam = camera.Camera(self.map.width, self.map.height)
        self.player.in_camera(self.camcam)


        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player.move_rect(obj_center.x, obj_center.y)
            if tile_object.name == 'scrap':
                self.max_num_items += 1
            if tile_object.name == 'map':
                entities.Objective(tile_object.x, tile_object.y,
                                   tile_object.width, tile_object.height, self.objective_group)
            if tile_object.name == 'wall':
                entities.Obstacle(tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height, self.walls)
        if self.max_num_items > 1:
            self.max_num_items -= 1
        else:
            self.max_num_items = 1
        self.num_of_items = random.randint(1, self.max_num_items)
        self.counter = entities.Counter(self.num_of_items, self.all_Sprite_Group)
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if self.num_of_items == 0:
                break
            else:
                self.num_of_items -= 1
                if tile_object.name == 'scrap':
                    entities.scrap(obj_center.x, obj_center.y, self.enemies, self.screen, self.player, self.walls,
                                   self.dt,
                                   self.camcam, self.all_Sprite_Group, self.counter, self.player.item_group)

        pygame.event.clear()
        self.player.vel = pygame.math.Vector2(0, 0)

        #start the loop
        if pygame.mixer.music.get_busy():
            pass
        else:
            pygame.mixer.music.play(-1)
        self.loop()

    def loop(self):
        while self.encounter:

            self.screen.fill((0, 0, 0))
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            # updates and keyinput
            events = pygame.event.get()
            self.player.pass_events(events)
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
                    self.draw_debug = not self.draw_debug
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    print(self.num_of_items)

            for sprite in self.all_Sprite_Group:
                self.camcam.update(sprite)
                sprite.update()


            self.camcam.update(self.player)


            self.player.ammo_reload_toggle(ui.auto_reload.get_state())

            self.draw()


            # collision detection
            # enemy hits player
            hits = pygame.sprite.spritecollide(self.player, self.player.item_group, False, collide_hit_rect)
            for hit in hits:
                self.counter.adj(1)
                self.player.pickup_snd()
                hit.kill()




            hits = pygame.sprite.spritecollide(self.player, self.objective_group, False, collide_hit_rect)
            if hits:
                if len(self.player.item_group) < 1:
                    break

            pygame.display.flip()
            if self.draw_debug:
                print("flipping the display")

            pygame.time.Clock().tick(60)

    def draw(self):
        # draw
        self.screen.blit(self.map_img, self.camcam.apply(self.map))
        ui.ingame_interface(self.screen, self.mouse_x, self.mouse_y, self.player.current_ammo,
                            self.ammo_font, self.font, self.clock, self.shell_img)

        for sprite in self.all_Sprite_Group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))
            try:
                if ui.show_healthbar.get_state():
                    sprite.health_bar(self.camcam)
            except:
                pass
        self.screen.blit(self.counter.image, self.camcam.apply(self.counter.image))
        self.player.draw()
        for sprite in self.player.item_group:
            self.screen.blit(sprite.image, self.camcam.apply(sprite))


        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, settings.PURPLE, self.camcam.apply_rect(wall.rect), 2)