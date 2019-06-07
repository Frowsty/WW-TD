import FroPy as fp
import pygame
from pygame import font
import random
import ui_components as ui
import game_entities as entities
from time import sleep
import tilemap

import camera
import wang
import a_star
import os
from os import path
import map_logic
import settings
from settings import *



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







class Game():
    def __init__(self):
        # initializers
        pygame.init()
        if not pygame.display.get_init():
            pygame.display.init()
        pygame.font.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.pre_init(44100, -16, 4, 2048)
        size = [settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)

        # Set window title
        pygame.display.set_caption("WW - TD")
        self.fullscreen = False

        # Define Clock
        self.clock = pygame.time.Clock()
        self.dt = clock.tick(settings.FPS) / 1000.0
        self._image_library = {}
        self.font = pygame.font.SysFont("Arial", 20)
        self.ammo_font = pygame.font.SysFont("Arial", 30)

        self.new_game = False
        self.how_to_screen = False
        self.hud_font = './images/Impacted2.0.ttf'
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = self.get_image_convert_alpha('./images/bullet.png')
        self.bullet_images['sm'] = pygame.transform.scale(self.bullet_images['lg'], (10,10))
        self.mob_img = self.get_image_convert_alpha('./character_frames/enemy_knife.png')


        self.Map_Shown = False

        # sprite groups
        self.all_Sprite_Group = pygame.sprite.Group()
        self.map_Sprite_Group = pygame.sprite.Group()
        self.terrain_sprites = pygame.sprite.Group()
        self.mpi_Group = pygame.sprite.Group()
        self.player_Sprite_Group = pygame.sprite.Group()
        self.enemy_Sprite_Group = pygame.sprite.Group()
        self.projectile_Sprite_Group = pygame.sprite.Group()
        self.wall_Group = pygame.sprite.Group()

        self.menu_bg = pygame.transform.scale(self.get_image("pictures/menu_bg.jpg"), (1280, 960))
        self.map_instance = map_class(self, self.screen)
        self.splat = self.get_image_convert_alpha(settings.SPLAT)
        self.splat = pygame.transform.scale(self.splat, (64, 64))

        self.gun_flashes = []
        for img in settings.MUZZLE_FLASHES:
            self.gun_flashes.append(self.get_image(img))
        self.item_images = {}
        #for item in ITEM_IMAGES:
        #    self.item_images[item] = self.get_image_convert_alpha(settings.ITEM_IMAGES[item])

        #lighting effects
        self.fog = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.fog.fill(settings.NIGHT_COLOR)
        self.light_mask = self.get_image_convert_alpha(settings.LIGHT_MASK)
        self.light_mask = pygame.transform.scale(self.light_mask, settings.LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        #todo remove zombie references, replace with indian
        #Sound loading
        pygame.mixer.music.load(settings.BG_MUSIC)
        self.effects_sounds = {}
        #for type in settings.EFFECTS_SOUNDS:
        #    self.effects_sounds[type] = pygame.mixer.Sound(settings.EFFECTS_SOUNDS[type])
        self.weapon_sounds = {}
        for weapon in settings.WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in settings.WEAPON_SOUNDS[weapon]:
                s = pygame.mixer.Sound(snd)
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        # self.zombie_moan_sounds = []
        # for snd in settings.ZOMBIE_MOAN_SOUNDS:
        #     s = pygame.mixer.Sound(snd)
        #     s.set_volume(0.2)
        #     self.zombie_moan_sounds.append(s)
        # self.player_hit_sounds = []
        # for snd in settings.PLAYER_HIT_SOUNDS:
        #     self.player_hit_sounds.append(pygame.mixer.Sound(snd))
        # self.zombie_hit_sounds = []
        # for snd in settings.ZOMBIE_HIT_SOUNDS:
        #     self.zombie_hit_sounds.append(pygame.mixer.Sound(snd))
        self.player = entities.Player(self, self.screen, 300, 300)




    def get_image_convert_alpha(self, path):
        image = self._image_library.get(path)
        if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path).convert_alpha()
        return image

    def get_image(self, path):
        image = self._image_library.get(path)
        if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path).convert_alpha()
        return image


    def draw(self):
        self.screen.fill(BLACK)


    def update(self):
        # Main menu

        self.menu_input = ui.menu_system(self.mouse_x, self.mouse_y, self.new_game)
        if self.new_game == False and self.how_to_screen == False:
            ui.update_mm()
            ui.draw_mm(self.screen, self.mouse_x, self.mouse_y, self.menu_bg)
        if self.menu_input == "QUIT":
            quit()
        if self.menu_input == "START":
            self.new_game = True
        if self.menu_input == "HOWTO":
            self.how_to_screen = True
        if self.menu_input == "MAIN_MENU":
            self.how_to_screen = False
            self.new_game = False

        if self.how_to_screen == True:
            self.how_to()
        if self.new_game == True:
            self.start_game = topgame(self, self.screen)

        if self.Map_Shown == True:
            self.map_instance.show()

        self.all_Sprite_Group.update()
        pygame.display.update()
        # set max ticks per second (FPS)
        self.clock.tick(60)

    def events(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.keyboard_input = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                quit()
            if pygame.key.get_pressed()[pygame.K_F12]:
                fullscreen = toggle_fullscreen(fullscreen)

            if pygame.key.get_pressed()[pygame.K_F3]:
                self.Map_Shown = not self.Map_Shown

                sleep(0.10)

    def how_to(self):
        while self.how_to_screen:
            self.events()
            self.menu_input = ui.menu_system(self.mouse_x, self.mouse_y, self.new_game)
            if self.menu_input == "MAIN_MENU":
                self.how_to_screen = False
            ui.draw_howto(self.screen, self.mouse_x, self.mouse_y, self.font, self.new_game, self.menu_bg)
            pygame.display.update()
            self.clock.tick(60)

    def draw_player_health(self, surf, x, y , pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = settings.GREEN
        elif pct > 0.3:
            col = settings.YELLOW
        else:
            col = settings.RED
        pygame.draw.rect(surf, col, fill_rect)
        pygame.draw.rect(surf, settings.WHITE, outline_rect, 2)


class map_class():
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        self.map = map_logic.GameMapController(self.game, self.screen)
        self.running = False

    def events(self):
        events = pygame.event.get()
        for event in events:
            if pygame.key.get_pressed()[pygame.K_m]:
                for sprite in self.game.mpi_Group:
                    sprite.toggle_movement()
                sleep(0.10)
            self.game.mpi_Group.update(self.screen)

    def update(self):
        self.game.mpi_Group.update(self.screen)
        pass

    def show(self):
        self.running = True
        self.loop()

    def draw(self):

        self.screen.fill(settings.BROWN)
        self.game.terrain_sprites.draw(self.screen)
        for sprite in self.game.map_Sprite_Group:
            sprite.draw(self.screen)
        self.game.map_Sprite_Group.draw(self.screen)
        self.game.mpi_Group.draw(self.screen)
        pygame.display.update()
        self.game.clock.tick(60)




    def loop(self):
        while self.running:
            self.events()
            self.update()
            self.draw()




class topgame():
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.fullscreen = False

        # Initialize our player
        self.start_game()


    def start_game(self):
        self.select_map()
        self.camera = camera.Camera(self.map.width, self.map.height)
        while self.game.new_game:
            self.events()
            self.update()
            self.draw()



    def select_map(self):
        self.load_map('./tilesets/temptown.tmx')

    def load_map(self, filename):
        # needs random file selection per level, one level hard coded for testing
        self.map = tilemap.TiledMap(filename)
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = pygame.math.Vector2(tile_object.x + tile_object.width / 2,
                                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.game.player.x = obj_center.x
                self.game.player.y = obj_center.y
            if tile_object.name == 'indian':
                entities.Mob(self.game, self.screen, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                entities.Obstacle(self.game, tile_object.x, tile_object.y,
                                  tile_object.width, tile_object.height)
            if tile_object.name in ['health', 'shotgun']:
                Item(self, obj_center, tile_object.name)



    # toggle fullscreen (ON/OFF)
    def toggle_fullscreen(self, fullscreen):
        if fullscreen:
            self.screen = pygame.display.set_mode(
                (size[0], size[1]), pygame.RESIZABLE
            )
        else:
            self.screen = pygame.display.set_mode((1280,960), pygame.FULLSCREEN)
        return not fullscreen


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                quit()
            if pygame.key.get_pressed()[pygame.K_F12]:
                self.fullscreen = self.toggle_fullscreen(self.fullscreen)

            if pygame.key.get_pressed()[pygame.K_F3]:
                self.game.Map_Shown = not self.game.Map_Shown
                self.game.map_instance.show()








    def update(self):

        self.game.player.ammo_reload_toggle(ui.auto_reload.get_state())
        self.game.all_Sprite_Group.update()
        self.game.player.ammo_reload_toggle(ui.auto_reload.get_state())
        self.camera.update(self.game.player)


    def draw(self):

        self.screen.blit(self.map_img, self.camera.apply(self.map))
        self.game.draw_player_health(self.screen, 10, 50, self.game.player.health / settings.PLAYER_HEALTH)
        ui.ingame_interface(self.screen, self.game.mouse_x, self.game.mouse_y, self.game.player.ammo_loaded,
                            self.game.ammo_font, self.game.font, self.game.clock, self.game.player.shell_img)


        self.game.all_Sprite_Group.draw(self.screen)

        pygame.display.update()
        self.game.clock.tick(60)








g = Game()

while True:
    g.events()
    g.update()
    g.draw()

