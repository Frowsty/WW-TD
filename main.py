import FroPy as fp
import pygame
from pygame import font
import random
import ui_components as ui
import game_entities as entities
from time import sleep
import math
from math import atan2

import settings
from settings import *
import camera
import tilemap
from tilemap import *
import wang
import a_star
import os
from os import path
import map_logic

vec = pygame.math.Vector2

# initializers
if __name__ == 'main':
    pygame.init()


# sprite groups
all_Sprite_Group = pygame.sprite.Group()
map_Sprite_Group = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
mpi_Group = pygame.sprite.Group()
player_Sprite_Group = pygame.sprite.Group()
enemy_Sprite_Group = pygame.sprite.Group()
walls_Group = pygame.sprite.Group()
projectile_Group = pygame.sprite.Group()
objective_Group = pygame.sprite.Group()
item_Group = pygame.sprite.Group()
pickup_Effect_Group = pygame.sprite.Group()

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

# Set screen size
size = [1280, 960]
screen = pygame.display.set_mode(size)

# ash's constants
_Multiplier = 1
SCREEN_WIDTH = 1280 * _Multiplier
SCREEN_HEIGHT = 1024 * _Multiplier
BLANK = None
DEBUG = False
Map_Shown = False

# Set window title
pygame.display.set_caption("WW - TD")


# Define Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)
big_font = pygame.font.SysFont("Arial", 60)
ammo_font = pygame.font.SysFont("Arial", 30)

start_game = False
how_to = False
settings_menu = False

def play_sound(file):
    if ui.enable_sound.get_state():
        pygame.mixer.Sound(file).set_volume(0)
    else:
        pygame.mixer.Sound(file).set_volume(0.3)

previous_state = False




# ASH - image function, loads image into an array and if it has already been loaded, it loads the previous loaded image
# instead of wasting memory on a new image. if it hasn't been it loads it.
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

# toggle fullscreen (ON/OFF)
def toggle_fullscreen(fullscreen):
    if fullscreen:
        screen = pygame.display.set_mode(
            (size[0], size[1]), pygame.RESIZABLE
        )
    else:
        screen = pygame.display.set_mode(
            (size[0], size[1]), pygame.FULLSCREEN
        )
    return not fullscreen

gun_flashes = []
for img in settings.MUZZLE_FLASHES:
    gun_flashes.append(get_image_convert_alpha(img))
dt = clock.tick(60) / 1000.0

# Initialize our player
#passing in groups to player instance for inheritence
player = entities.Player(dt, ammo_font, walls_Group, projectile_Group, all_Sprite_Group, player_Sprite_Group, item_Group, gun_flashes, screen, False, -10, -10)

#removed enemies from manually being placed on board, now enemies spawn on markers in tile maps from the maplogic

map = map_logic.GameMapController(map_Sprite_Group, _Multiplier, screen, terrain_sprites, mpi_Group, player_Sprite_Group, player, all_Sprite_Group, enemy_Sprite_Group, projectile_Group, objective_Group, walls_Group, dt)
map_Sprite_Group.add(map)


menu_bg = pygame.transform.scale(get_image("pictures/menu_bg.jpg"), (1280, 960))
bullet_img = pygame.transform.scale(get_image_convert_alpha("pictures/bullet.png"), (10, 10))
shell_img = get_image_convert_alpha("pictures/shell.png")
small_shell_img = pygame.transform.scale(get_image_convert_alpha("pictures/shell.png"), (45, 45))
bullet_hit_tick = 0
powerup_tick = pygame.time.get_ticks()
powerup_list = []
menu_input = ""



def Map_screen():

    map.showing = True
    player.bullets.clear()
    enemy_Sprite_Group.clear(screen, (0,0,settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    sleep(0.10)

    while map.showing:
        map.player_icon.moving = True
        mpi_Group.update(screen)
        terrain_sprites.draw(screen)
        for sprite in map_Sprite_Group:
            sprite.draw(screen)
        map_Sprite_Group.draw(screen)
        mpi_Group.draw(screen)

        pygame.display.update()
        clock.tick(60)


def load_map():
    filename = './tilesets/temptown.tmx'
    # needs random file selection per level, one level hard coded for testing
    tile_of_map = tilemap.TiledMap(filename)
    map_img = tile_of_map.make_map()
    map_rect = map_img.get_rect()
    return tile_of_map, map_img, map_rect


def start_town(mouse_x, mouse_y):

    global walls_Group, enemey_Sprite_Group, powerup_tick, previous_state, dt

    enemies = enemy_Sprite_Group

    tile_of_map, map_img, map_rect = load_map()
    tile_of_map.rect = map_rect
    encounter = True

    if ui.settings_powerup_toggle.get_state() == True:
        if (pygame.time.get_ticks() - powerup_tick) / 1000 >= random.randint(20, 45):
            powerup_list.append(entities.PowerUp(screen, random.randint(1, 3), [random.randint(200, 1000), 50],
                                                 pygame.time.get_ticks()))
            for powerup in powerup_list:
                powerup.activate = True
            powerup_tick = pygame.time.get_ticks()

        if len(powerup_list) > 0:
            for powerup in powerup_list:
                if powerup.activate == True:
                    powerup.run(small_shell_img)
                    powerup.return_attribute(mouse_x, mouse_y)

                if (pygame.time.get_ticks() - powerup.called_tick) / 1000 >= 5 and powerup.clicked_tick == 0:
                    powerup_list.pop(powerup_list.index(powerup))

                if powerup.activate_attrib == "increase ammo":
                    if (pygame.time.get_ticks() - powerup.clicked_tick) / 1000 <= 10:
                        if player.mode == "EASY":
                            player.ammo = 10
                        if player.mode == "MEDIUM":
                            player.ammo = 9
                        if player.mode == "HARD":
                            player.ammo = 7
                        powerup.draw = False
                    else:
                        player.ammo = 5
                        powerup_list.pop(powerup_list.index(powerup))
                elif powerup.activate_attrib == "increase damage":
                    if (pygame.time.get_ticks() - powerup.clicked_tick) / 1000 <= 10:
                        if player.mode == "EASY":
                            player.damage = 100
                        if player.mode == "MEDIUM":
                            player.damage = 50
                        if player.mode == "HARD":
                            player.damage = 34
                        powerup.draw = False
                    else:
                        if player.mode == "EASY":
                            player.damage = 50
                        if player.mode == "MEDIUM":
                            player.damage = 34
                        if player.mode == "HARD":
                            player.damage = 25
                        powerup_list.pop(powerup_list.index(powerup))
                elif powerup.activate_attrib == "increase health":
                    if player.mode == "EASY":
                        player.health += 60
                    if player.mode == "MEDIUM":
                        player.health += 45
                    if player.mode == "HARD":
                        player.health += 30
                    powerup_list.pop(powerup_list.index(powerup))

    camcam = camera.Camera(tile_of_map.width, tile_of_map.height)
    num_of_items = 0


    for tile_object in tile_of_map.tmxdata.objects:
        obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                         tile_object.y + tile_object.height / 2)
        if tile_object.name == 'player':
            player.move_rect(obj_center.x, obj_center.y)
        if tile_object.name == 'map':
            entities.Objective(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, objective_Group)
        if tile_object.name == 'enemy':
            entities.Enemy(obj_center.x, obj_center.y, enemy_Sprite_Group , screen, player, walls_Group, dt, camcam, all_Sprite_Group, counter = False)
        if tile_object.name == 'wall':
            entities.Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, walls_Group)
        if tile_object.name == 'food':
            num_of_items +=1
    counter = entities.Counter(num_of_items, all_Sprite_Group)
    for tile_object in tile_of_map.tmxdata.objects:
        obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                         tile_object.y + tile_object.height / 2)

        if tile_object.name == 'food':
            entities.food(obj_center.x, obj_center.y, enemy_Sprite_Group, screen, player, walls_Group,
                          dt, camcam, all_Sprite_Group, counter, player.item_group)




    player.in_camera(camcam)
    instructions = entities.Text_Box('./text/opening_scene.json', screen)
    while encounter:
        screen.fill((0, 0, 0))
        events = pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()



        camcam.update(player)
        player.pass_events(events)
        all_Sprite_Group.update()
        pickup_Effect_Group.update()

        for sprite in enemy_Sprite_Group:
            sprite.update()
        player.ammo_reload_toggle(ui.auto_reload.get_state())


        screen.blit(map_img, camcam.apply(tile_of_map))


        #ammo_font and screen are passed in on creation


        player.draw()
        for sprite in enemy_Sprite_Group:
            screen.blit(sprite.image, camcam.apply(sprite))
            if ui.show_healthbar.get_state():
                sprite.health_bar()
        for sprite in all_Sprite_Group:
            screen.blit(sprite.image, camcam.apply(sprite))
            try:
                if ui.show_healthbar.get_state():
                    sprite.health_bar(camcam)
            except:
                pass

        for sprite in pickup_Effect_Group:
            print(sprite.image)
            screen.blit(sprite.image, camcam.apply(sprite))
        ui.ingame_interface(screen, mouse_x, mouse_y, player.current_ammo, ammo_font, font, clock, shell_img)






        #enemy hits player
        hits = pygame.sprite.spritecollide(player, enemies, False, collide_hit_rect)
        for hit in hits:
            if random.random() < 0.7:
                random.choice(phs).play()
            hit.vel = vec(0, 0)
        if hits:
            player.hit()
        #bullets hit enemys
        hits = pygame.sprite.groupcollide(enemies, projectile_Group, False, True)
        for enemy in hits:
            for bullet in hits[enemy]:
                enemy.health_hit(bullet.damage)
            enemy.vel = vec(0,0)
        hits = pygame.sprite.spritecollide(player, player.item_group, False, collide_hit_rect)
        for hit in hits:
            counter.counter_adj(1)
            if not player.item_effect_current:
                item_effect = entities.item_pick_up(player.rect.x, player.rect.y, player, pickup_Effect_Group)
                player.item_effect_current = True
            hit.kill()

        hits = pygame.sprite.spritecollide(player, objective_Group, False, collide_hit_rect)
        if hits:
            break

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    Map_screen()



#not sure why kb_input and fps is passed in
def draw_gamewindow(screen, mouse_x, mouse_y, kb_input, fps):
    global start_game, settings_menu, how_to, menu_input, was_pushed , powerup_tick, increase_ammo_tick, increase_damage_tick
    screen.fill(BLACK)


    if start_game == True:
        start_town(mouse_x, mouse_y)


    if how_to == True:
        ui.draw_howto(screen, mouse_x, mouse_y, font, start_game, menu_bg)

    if settings_menu == True:
        ui.draw_settings(screen, mouse_x, mouse_y, menu_bg)

    if start_game == False:
        menu_input = ui.menu_system(mouse_x, mouse_y, settings_menu)
    if start_game == False and how_to == False and settings_menu == False:
        ui.update_mm()
        ui.draw_mm(screen, mouse_x, mouse_y, menu_bg, menu_input)

    if menu_input == "QUIT":
        quit()
    if menu_input == "SETTINGS":
        settings_menu = True
    if menu_input == "HOWTO":
        how_to = True
    if menu_input == "MAIN_MENU":
        how_to = False
        start_game = False
        settings_menu = False

    if menu_input == "START_EASY":
        player.mode = "EASY"
        player.update_settings()
        start_game = True
        settings_menu = False
    if menu_input == "START_MEDIUM":
        player.mode = "MEDIUM"
        player.update_settings()
        start_game = True
        settings_menu = False
    if menu_input == "START_HARD":
        player.mode = "HARD"
        player.update_settings()
        start_game = True
        settings_menu = False

    menu_input = ""

    fullscreen = False

    game_over_text = big_font.render("GAME OVER!", True, RED)

def main():
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
                quit()
            if pygame.key.get_pressed()[pygame.K_F12]:
                fullscreen = toggle_fullscreen(fullscreen)
        player.pass_events(events)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        keyboard_input = pygame.key.get_pressed()
        all_Sprite_Group.update()
        pygame.display.update()

        #actually Delta Time... not fps
        fps = clock.tick(60) / 1000.0

        # player_Sprite_Group.draw(screen)
        if player.health != 0:
            draw_gamewindow(screen, mouse_x, mouse_y, keyboard_input, fps)
        else:
            screen.fill(BLACK)
            screen.blit(game_over_text,
                        (1280 / 2 - (game_over_text.get_width() / 2), 960 / 2 - (game_over_text.get_height() / 2)))


        # set max ticks per second (FPS)
        clock.tick(60)


main()