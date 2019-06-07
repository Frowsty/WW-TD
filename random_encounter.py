import pygame
import random
import os
from os import path
import map_logic
import tilemap
import camera

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
    def __init__(self, screen, player, player_group, camcam):
        self.player = player
        self.player_group = player_group
        self.screen = screen
        self.looping = True
        self.camcam = camcam

        self.loop()






    def loop(self):
        ammo_font = pygame.font.SysFont("Arial", 30)
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Arial", 20)
        shell_img = get_image_convert_alpha("pictures/shell.png")
        while self.looping:
            pygame.event.get()
            self.screen.fill((0,0,0))
            image = get_image('./images/cards/broken_wheel.png')
            w, h = pygame.display.get_surface().get_size()
            self.screen.blit(image, ((w // 2) - (image.get_width()//2),
                                (h// 2) - (image.get_height() //2)))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.looping = False


            pygame.display.flip()
            pygame.time.Clock().tick(60)

        self.select_map()

        self.encounter = True
        self.camera = camera.Camera(1000,1000)

        while self.encounter:
            self.screen.fill((0, 0, 0))
            pygame.event.pump()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            keyboard_input = pygame.key.get_pressed()

            fps = clock.tick(60) / 1000.0

            self.screen.blit(self.map_img, self.camcam.apply(self.map))
            self.camcam.update(self.player)
            self.all_Sprite_Group.update()
            ui.ingame_interface(self.screen, mouse_x, mouse_y, self.player.current_ammo, ammo_font, font, clock, shell_img)
            self.player.ammo_reload_toggle(ui.auto_reload.get_state())
            # ammo_font and screen are passed in on creation

            for sprite in all_Sprite_Group:
                self.screen.blit(sprite.image, self.camcam.apply(sprite))

            # enemy hits player
            hits = pygame.sprite.spritecollide(self.player, enemies, False, collide_hit_rect)
            for hit in hits:
                if random < 0.7:
                    choice(self.player_hit_sounds).play()
                self.player.health -= settings.MOB_DAMAGE
                hit.vel = vec(0, 0)
            if hits:
                self.player.hit()
                player.rect += pygame.math.Vector2(75, 0).rotate(-hit.direction)
            # bullets hit enemys
            hits = pygame.sprite.groupcollide(enemies, projectile_Group, False, True)
            for enemy in hits:
                for bullet in hits[enemy]:
                    enemy.health -= bullet.damage
                enemy.vel = vec(0, 0)

            hits = pygame.sprite.spritecollide(player, objective_Group, False, collide_hit_rect)
            if hits:
                if len(enemies) < 1:
                    break

            pygame.display.flip()
            pygame.time.Clock().tick(60)


    def select_map(self):
        self.load_map('./tilesets/random1.tmx')

    def load_map(self, filename):
        #needs random file selection per level, one level hard coded for testing
        self.map = tilemap.TiledMap(filename)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()


    def select_encounter(self):
        pass

    def select_posture(self):
        #randomly selects hostile or passive or friendly
        #only triggures on encounters with people or animals
        pass

    def draw(self):
        #todo add camera class, then add $, self.camera.apply_rect(self.map_rect)$ to the variable below
        self.screen.blit(self.map_img, (0,0))


        for sprite in self.player_group:
            self.screen.blit(sprite.image, self.camera.apply(sprite))




