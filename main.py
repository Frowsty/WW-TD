import FroPy as fp
import pygame
from pygame import font
import random
import ui_components as ui
import game_entities as entities
from time import sleep

import wang
import a_star
import os
from os import path
import map_logic

#initializers
if __name__ == 'main':
    pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
pygame.font.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()


#sprite groups
all_Sprite_Group = pygame.sprite.Group()
map_Sprite_Group = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
mpi_Group = pygame.sprite.Group()
player_Sprite_Group = pygame.sprite.Group()

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

#ash's constants
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

#ASH - image function, loads image into an array and if it has already been loaded, it loads the previous loaded image
#instead of wasting memory on a new image. if it hasn't been it loads it.
_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
    return image


# Initialize our player
player = entities.Player([300, 300])
player_Sprite_Group.add(player)
all_Sprite_Group.add(player)
map = map_logic.GameMapController(map_Sprite_Group, _Multiplier, screen, terrain_sprites, mpi_Group)
map_Sprite_Group.add(map)

menu_bg = pygame.transform.scale(get_image("pictures/menu_bg.jpg"), (1280, 960))

def draw_gamewindow(screen, mouse_x, mouse_y, kb_input):
    global start_game, how_to
    screen.fill(BLACK)

    # To prevent screen from blinking black we're calling draw_howto first if
    # player choose How To screen in main menu

    if start_game == True:
        screen.blit(menu_bg, (0,0))
        ui.ingame_interface(screen, mouse_x, mouse_y, player.bullets, ammo_font, clock)
        player.draw(screen)
        player.actions(screen, kb_input, ui.auto_reload.get_state())

        for bullet in player.bullets:
            bullet.draw(screen)
        #todo check bullets for sprite status, add them to their own group, add group to update and draw functions
        
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

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            quit()
    
        if pygame.key.get_pressed()[pygame.K_F3]:
                Map_Shown = not Map_Shown
                sleep(0.10)
        if Map_Shown:
            if pygame.key.get_pressed()[pygame.K_m]:
                for sprite in mpi_Group:
                    sprite.toggle_movement()
            mpi_Group.update()


    mouse_x, mouse_y = pygame.mouse.get_pos()
    keyboard_input = pygame.key.get_pressed()

    all_Sprite_Group.update()
    
    draw_gamewindow(screen, mouse_x, mouse_y, keyboard_input)
    
    pygame.display.update()
    # set max ticks per second (FPS)
    clock.tick(60)
