import FroPy as fp
import pygame

import main_menu as menu
import game_entities as entities

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set screen size
size = [1280, 960]
screen = pygame.display.set_mode(size)

# Set window title
pygame.display.set_caption("WW - TD")

# Define Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)

start_game = False
how_to = False

# Initialize our player
player = entities.Player([300, 300])

def draw_gamewindow(screen, mouse_x, mouse_y, kb_input):
    global start_game, how_to
    screen.fill(BLACK)

    # To prevent screen from blinking black we're calling draw_howto first if
    # player choose How To screen in main menu

    if start_game == True:
        screen.blit(pygame.transform.scale(pygame.image.load("pictures/menu_bg.jpg"), (1280, 960)), (0,0))
        player.draw(screen)
        player.movement(screen, kb_input)

    if how_to == True:
        menu.draw_howto(screen, mouse_x, mouse_y, font)

    # Main menu
    menu_input = menu.menu_system(mouse_x, mouse_y)
    if start_game == False and how_to == False:
        menu.update_mm()
        menu.draw_mm(screen, mouse_x, mouse_y)
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

    # set max ticks per second (FPS)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            quit()

    mouse_x, mouse_y = pygame.mouse.get_pos()
    keyboard_input = pygame.key.get_pressed()

    draw_gamewindow(screen, mouse_x, mouse_y, keyboard_input)
    
    pygame.display.update()