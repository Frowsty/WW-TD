import FroPy as fp
import pygame

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 150)
GREEN = (0, 150, 0)
RED = (150, 0, 0)
MENU_MAIN = (232, 190, 122)
MENU_OUTLN = (178, 136, 69)

menu_bg = pygame.transform.scale(pygame.image.load("pictures/menu_bg.jpg"), (1280, 960))

# Initialize Main Menu objects
menu_box = fp.GroupBox(1280/2 - 150, 960/2 - 300, 300, 500, "Main Menu")
menu_start = fp.Button(GREEN, 260, 180, 250, 50, "Start game")
menu_howto = fp.Button(BLUE, 260, 250, 250, 50, "How to play")
menu_quit = fp.Button(RED, 260, 320, 250, 50, "Quit!")

def update_mm():
    menu_start.x = menu_box.x + 25
    menu_start.y = menu_box.y + 150

    menu_howto.x = menu_box.x + 25
    menu_howto.y = menu_box.y + 250

    menu_quit.x = menu_box.x + 25
    menu_quit.y = menu_box.y + 350

def draw_mm(screen, mouse_x, mouse_y):
    screen.blit(menu_bg, (0,0))
    menu_box.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)
    menu_start.draw(screen)
    menu_howto.draw(screen)
    menu_quit.draw(screen)

def menu_system(mouse_x, mouse_y):
    
    if menu_quit.clicked(mouse_x, mouse_y):
        return "QUIT"
    if menu_start.clicked(mouse_x, mouse_y):
        return "START"
    if menu_howto.clicked(mouse_x, mouse_y):
        return "HOWTO"