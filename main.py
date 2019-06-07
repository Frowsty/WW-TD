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


# Initialize our player
player = entities.Player([300, 300])
player_Sprite_Group.add(player)
enemy = entities.Enemy([500, 300])
enemy_Sprite_Group.add(enemy)
all_Sprite_Group.add(player)
all_Sprite_Group.add(enemy)
map = map_logic.GameMapController(map_Sprite_Group, _Multiplier, screen, terrain_sprites, mpi_Group, player_Sprite_Group)
map_Sprite_Group.add(map)

menu_bg = pygame.transform.scale(get_image("pictures/menu_bg.jpg"), (1280, 960))
bullet_img = pygame.transform.scale(get_image_convert_alpha("pictures/bullet.png"), (10, 10))
shell_img = get_image_convert_alpha("pictures/shell.png")
small_shell_img = pygame.transform.scale(get_image_convert_alpha("pictures/shell.png"), (45, 45))

enemies = [entities.Enemy([500, 300]), entities.Enemy([700, 300])]
bullet_hit_tick = pygame.time.get_ticks()
powerup_tick = pygame.time.get_ticks()
powerup_list = []
menu_input = ""

def draw_gamewindow(screen, mouse_x, mouse_y, kb_input, fps):
    global start_game, settings_menu, how_to, menu_input, was_pushed , powerup_tick, increase_ammo_tick, increase_damage_tick
    screen.fill(BLACK)

    if start_game == True:
        screen.blit(menu_bg, (0, 0))

        if ui.settings_powerup_toggle.get_state() == True:
            if (pygame.time.get_ticks() - powerup_tick) / 1000 >= random.randint(20, 45):
                powerup_list.append(entities.PowerUp(screen, random.randint(1, 3), [random.randint(200, 1000), 50], pygame.time.get_ticks()))
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

        ui.ingame_interface(screen, mouse_x, mouse_y, player.ammo, player.bullets, ammo_font, font, clock, shell_img)
        player.draw(screen, ammo_font)
        player.actions(ui.auto_reload.get_state())
        for enemy in enemies:
            enemy.draw(screen, player.cur_pos, player.player_frames[0], fps, player.dead)
            enemy.update_settings(player.mode)
            if enemy.hit_player == True:
                player.health -= enemy.damage
                player.cur_pos += pygame.math.Vector2(75, 0).rotate(-enemy.direction)
                enemy.hit_player = False

        for bullet in player.bullets:
            bullet.draw(screen, bullet_img)
            for enemy in enemies:
                bullet.collision_check(enemy.cur_pos, enemy.player_frame)
                if bullet.hit_target == True:
                    enemy.health -= bullet.damage
                    if enemy.health <= 0:
                        enemies.pop(enemies.index(enemy))
                    bullet.hit_target = False
    
    if Map_Shown == True:
        terrain_sprites.draw(screen)
        for sprite in map_Sprite_Group:
            sprite.draw(screen)
        map_Sprite_Group.draw(screen)
        mpi_Group.draw(screen)

    if how_to == True:
        ui.draw_howto(screen, mouse_x, mouse_y, font, start_game, menu_bg)

    if settings_menu == True:
        ui.draw_settings(screen, mouse_x, mouse_y, menu_bg)

    # Main menu
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

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            quit()
        if pygame.key.get_pressed()[pygame.K_F12]:
            fullscreen = toggle_fullscreen(fullscreen)

        if pygame.key.get_pressed()[pygame.K_F3]:
            Map_Shown = not Map_Shown
            # player.bullets.clear()
            # enemies.clear()
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
    if player.health != 0:
        draw_gamewindow(screen, mouse_x, mouse_y, keyboard_input, fps)
    else:
        screen.fill(BLACK)
        screen.blit(game_over_text, (1280/2 - (game_over_text.get_width() / 2), 960/2 - (game_over_text.get_height() / 2)))


    all_Sprite_Group.update()
    pygame.display.update()
    # set max ticks per second (FPS)
    clock.tick(60)