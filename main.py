import FroPy as fp
import pygame
from pygame import font
import random
import ui_components as ui
import game_entities as entities
from time import sleep
import settings
from settings import *

import camera
import tilemap
import wang
import a_star
import os
from os import path
import map_logic

# initializers
if __name__ == 'main':
    pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
pygame.font.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# sprite groups
all_Sprite_Group = pygame.sprite.Group()
map_Sprite_Group = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
mpi_Group = pygame.sprite.Group()
player_Sprite_Group = pygame.sprite.Group()
enemy_Sprite_Group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()

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
ammo_font = pygame.font.SysFont("Arial", 30)

start_game = False
how_to = False

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


# Initialize our player

player = entities.Player(ammo_font, all_Sprite_Group, gun_flashes, [300, 300])
player_Sprite_Group.add(player)
all_Sprite_Group.add(player)

map = map_logic.GameMapController(map_Sprite_Group, _Multiplier, screen, terrain_sprites, mpi_Group, player_Sprite_Group)
map_Sprite_Group.add(map)

menu_bg = pygame.transform.scale(get_image("pictures/menu_bg.jpg"), (1280, 960))
bullet_img = pygame.transform.scale(get_image_convert_alpha("pictures/bullet.png"), (10, 10))
shell_img = get_image_convert_alpha("pictures/shell.png")
bullet_hit_tick = 0



def load_map():
    filename = './tilesets/temptown.tmx'
    # needs random file selection per level, one level hard coded for testing
    map = tilemap.TiledMap(filename)
    map_img = map.make_map()
    map_rect = map_img.get_rect()
    return map, map_img, map_rect


def start_town(walls_group, enemies):
    map, map_img, map_rect = load_map()

    encounter = True


    for tile_object in map.tmxdata.objects:
        obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                         tile_object.y + tile_object.height / 2)
        if tile_object.name == 'player':
            player.rect.x = obj_center.x
            player.rect.y = obj_center.y
        if tile_object.name == 'indian':
            entities.Enemy(obj_center.x, obj_center.y, enemy_Sprite_Group)
        if tile_object.name == 'wall':
            entities.Obstacle(tile_object.x, tile_object.y,
                     tile_object.width, tile_object.height, walls_group)
    camcam = camera.Camera(map.width, map.height)


    while encounter:
        screen.fill((0, 0, 0))
        pygame.event.pump()
        ui.ingame_interface(screen, mouse_x, mouse_y, player.bullets, ammo_font, font, clock, shell_img)
        player.ammo_reload_toggle(ui.auto_reload.get_state())
        player.actions()

        for enemy in enemies:
            enemy.draw(screen, player.cur_pos, player.player_frames[0], fps, player.dead)
            if enemy.hit_player == True:
                player.health -= 15
                player.cur_pos += pygame.math.Vector2(75, 0).rotate(-enemy.direction)
                enemy.hit_player = False

        for bullet in player.bullets:
            bullet.draw(screen, bullet_img)
            for enemy in enemies:
                bullet.collision_check(enemy.cur_pos, enemy.player_frame)
                if bullet.hit_target == True:
                    enemy.health -= bullet.damage
                    enemies.pop(enemies.index(enemy))
                    bullet.hit_target = False

        camcam.update(player)

        screen.blit(map_img, (0, 0))

        for sprite in player_Sprite_Group:
            screen.blit(sprite.image, camcam.apply(sprite))

        player.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)









def draw_gamewindow(screen, mouse_x, mouse_y, kb_input, fps, walls_group, enemies):
    global start_game, how_to, was_pushed
    screen.fill(BLACK)

    if start_game == True:
        start_town(walls_group, enemies)


    if how_to == True:
        ui.draw_howto(screen, mouse_x, mouse_y, font, start_game, menu_bg)

    if Map_Shown == True:
        terrain_sprites.draw(screen)
        for sprite in map_Sprite_Group:
            sprite.draw(screen)
        map_Sprite_Group.draw(screen)
        mpi_Group.draw(screen)

    # Main menu
    menu_input = ui.menu_system(mouse_x, mouse_y, start_game)
    if start_game == False and how_to == False:
        ui.update_mm()
        ui.draw_mm(screen, mouse_x, mouse_y, menu_bg)
    if menu_input == "QUIT":
        quit()
    if menu_input == "START":
        start_game = True
    if menu_input == "HOWTO":
        how_to = True
    if menu_input == "MAIN_MENU":
        how_to = False
        start_game = False

fullscreen = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            quit()
        if pygame.key.get_pressed()[pygame.K_F12]:
            fullscreen = toggle_fullscreen(fullscreen)

        if pygame.key.get_pressed()[pygame.K_F3]:
            Map_Shown = not Map_Shown

            player.bullets.clear()
            enemies.clear()
            sleep(0.10)
        if Map_Shown:
            if pygame.key.get_pressed()[pygame.K_m]:
                for sprite in mpi_Group:
                    sprite.toggle_movement()
                sleep(0.10)
            mpi_Group.update(screen)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    keyboard_input = pygame.key.get_pressed()

    fps = clock.tick(60) / 1000.0

    #player_Sprite_Group.draw(screen)
    draw_gamewindow(screen, mouse_x, mouse_y, keyboard_input, fps, walls_group, enemy_Sprite_Group)


    all_Sprite_Group.update()
    pygame.display.update()
    # set max ticks per second (FPS)
    clock.tick(60)

