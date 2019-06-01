import FroPy as fp
import pygame
from main_menu import *

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
type_text = font.render("", True, (255,255,255))

start_game = False
how_to = False

while True:

    # set max ticks per second (FPS)
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            quit()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    screen.fill(BLACK)

    # Main menu
    menu_input = menu_system(mouse_x, mouse_y)
    if start_game == False and how_to == False:
        update_mm()
        draw_mm(screen, mouse_x, mouse_y)
    if menu_input == "QUIT":
        quit()
    if menu_input == "START":
        start_game = True
    if menu_input == "HOWTO":
        how_to = True
    
    # if start_game == True:
        # call game function
    # if how_to == True:
        # call how to screen

    pygame.display.update()