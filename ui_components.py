import FroPy as fp
import pygame

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 150)
GREEN = (0, 150, 0)
RED = (150, 0, 0)
BROWN = (204, 153, 0)
MENU_MAIN = (232, 190, 122)
MENU_OUTLN = (178, 136, 69)

story_line = ["You're a lost cowboy in", "the middle of nowhere. ", "Your objective is to",
              "follow the path to the end ",
              "while completing tasks", "and fighting to survive ", "the journey."]

controls_text = ["W = Walk Up", "S = Walk Down", "A = Walk Left", "D = Walk Right", "R = Reload", "Space = Shoot"]

show_story = False
show_ctrls = False
show_inventory = False
show_fps = False

# Initialize Main Menu objects
menu_box = fp.GroupBox(1280 / 2 - 150, 960 / 2 - 300, 300, 500, "Main Menu")
menu_start = fp.Button(GREEN, 260, 180, 250, 50, "Start game")
menu_howto = fp.Button(BLUE, 260, 250, 250, 50, "How to play")
menu_quit = fp.Button(RED, 260, 320, 250, 50, "Quit!")
menu_back = fp.Button(WHITE, 10, 10, 50, 20, "<<<")

# InGame interface
enable_sound = fp.Checkbox(RED, GREEN, 110, 10, 50, 1, "Mute Sound:", False)
auto_reload = fp.Checkbox(RED, GREEN, 250, 10, 50, 1, "Auto Reload:", False)
toggle_inventory = fp.Button(BROWN, 1280 - 213, 960 - 60, 210, 50, "Open Inventory")
player_inventory = fp.GroupBox(1280, 960 - 370, 200, 300, "Inventory")
toggle_show_fps = fp.Checkbox(RED, GREEN, 400, 10, 50, 1, "Show FPS:", False)

# Howto menu objects
howto_story_btn = fp.Button(GREEN, 200, 180, 250, 50, "Story")
howto_story = fp.GroupBox(203, 235, 240, 0, "Story")
howto_ctrls_btn = fp.Button(BLUE, 832, 180, 250, 50, "Controls")
howto_ctrls = fp.GroupBox(835, 235, 240, 0, "Controls")


def update_mm():
    menu_start.x = menu_box.x + 25
    menu_start.y = menu_box.y + 150

    menu_howto.x = menu_box.x + 25
    menu_howto.y = menu_box.y + 250

    menu_quit.x = menu_box.x + 25
    menu_quit.y = menu_box.y + 350


def howto_page(screen, mouse_x, mouse_y, story, ctrls, font):
    global story_line, controls_text

    if story == True:
        howto_story_btn.text = "Close"
        howto_story.height += 35
        howto_story.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)
        if howto_story.height >= 300:
            howto_story.height = 300
            pos = 0
            for i in range(len(story_line)):
                render_story = font.render(story_line[i], True, (0, 0, 0))
                pos += 30  # moves the following line down 30 pixels
                screen.blit(render_story, (howto_story.x + 10, howto_story.y + 60 + pos))
    else:
        howto_story.height -= 35
        if howto_story.height <= 0:
            howto_story.height = 0
            howto_story_btn.text = "Story"
        else:
            howto_story.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)
    if ctrls == True:
        howto_ctrls_btn.text = "Close"
        howto_ctrls.height += 35
        howto_ctrls.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)
        if howto_ctrls.height >= 300:
            howto_ctrls.height = 300
            pos = 0
            for i in range(len(controls_text)):
                render_ctrls = font.render(controls_text[i], True, (0, 0, 0))
                pos += 30  # moves the following line down 30 pixels
                screen.blit(render_ctrls, (howto_ctrls.x + 50, howto_ctrls.y + 60 + pos))
    else:
        howto_ctrls.height -= 35
        if howto_ctrls.height <= 0:
            howto_ctrls.height = 0
            howto_ctrls_btn.text = "Controls"
        else:
            howto_ctrls.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)


def draw_mm(screen, mouse_x, mouse_y, menu_bg):
    screen.blit(menu_bg, (0, 0))
    # Draw main menu components
    menu_box.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)
    menu_start.draw(screen)
    menu_howto.draw(screen)
    menu_quit.draw(screen)


def draw_howto(screen, mouse_x, mouse_y, font, did_game_start, menu_bg):
    global show_story, show_ctrls

    screen.blit(menu_bg, (0, 0))

    menu_back.draw(screen)

    howto_story_btn.draw(screen)
    howto_ctrls_btn.draw(screen)

    if howto_story_btn.clicked(mouse_x, mouse_y) == True:
        show_story = not show_story
    if howto_ctrls_btn.clicked(mouse_x, mouse_y) == True:
        show_ctrls = not show_ctrls

    if did_game_start == False:
        howto_page(screen, mouse_x, mouse_y, show_story, show_ctrls, font)


def menu_system(mouse_x, mouse_y, did_game_start):
    global show_ctrls, show_story

    if menu_quit.clicked(mouse_x, mouse_y) == True and did_game_start == False:
        return "QUIT"
    if menu_start.clicked(mouse_x, mouse_y) == True and did_game_start == False:
        return "START"
    if menu_howto.clicked(mouse_x, mouse_y) == True and did_game_start == False:
        return "HOWTO"
    if menu_back.clicked(mouse_x, mouse_y) == True and did_game_start == False:
        show_ctrls = False
        howto_ctrls.height = 0
        show_story = False
        howto_story.height = 0

        return "MAIN_MENU"


def draw_ammo(screen, bullets, font, shell_img):
    ammo_text = font.render(f"{5 - len(bullets)}x", True, BLACK)
    screen.blit(ammo_text, (45, 920))
    screen.blit(shell_img, (-20, 870))


def inventory(screen, mouse_x, mouse_y):
    global show_inventory

    if show_inventory == True:
        toggle_inventory.text = "Close Inventory"
        player_inventory.x -= 33
        if player_inventory.x <= (1280 - 210):
            player_inventory.x = (1280 - 210)
    else:
        toggle_inventory.text = "Open Inventory"
        player_inventory.x += 33
        if player_inventory.x >= 1280:
            player_inventory.x = 1280

    if player_inventory.x != 1280:
        player_inventory.draw(screen, mouse_x, mouse_y, MENU_OUTLN, MENU_MAIN, RED, 10)


def ingame_interface(screen, mouse_x, mouse_y, bullets, font, clock, shell_img):
    global show_inventory

    enable_sound.draw(screen, mouse_x, mouse_y, 2, text_color=BLACK)
    auto_reload.draw(screen, mouse_x, mouse_y, 2, text_color=BLACK)
    toggle_show_fps.draw(screen, mouse_x, mouse_y, 2, text_color=BLACK)
    toggle_inventory.draw(screen)

    if toggle_inventory.clicked(mouse_x, mouse_y):
        show_inventory = not show_inventory

    show_fps = toggle_show_fps.get_state()

    if show_fps == True:
        fps_text = font.render(f"FPS: {round(clock.get_fps())}", True, GREEN)
        screen.blit(fps_text, ((1280 - fps_text.get_width()) - 10, 5))

    inventory(screen, mouse_x, mouse_y)

    # Draw ammo counter
    draw_ammo(screen, bullets, font, shell_img)