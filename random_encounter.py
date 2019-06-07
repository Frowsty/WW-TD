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


class random_Encounter():
    def __init__(self, screen, player_group):

        self.looping = True

        for sprite in player_group:
            self.player = sprite
        self.loop(screen, player_group)






    def loop(self,screen, player_group):
        while self.looping:
            pygame.event.get()
            screen.fill((0,0,0))
            image = get_image('./images/cards/broken_wheel.png')
            w, h = pygame.display.get_surface().get_size()
            screen.blit(image, ((w // 2) - (image.get_width()//2),
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
            pygame.event.pump()
            self.player.actions()
            screen.fill((0,0,0))

            self.camera.update(self.player)

            self.draw(screen, player_group)  #draws the map

            self.player.draw(screen)

            pygame.display.flip()
            pygame.time.Clock().tick(60)


    def select_map(self):
        self.load_map('./tilesets/temptown.tmx')

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

    def draw(self, screen, player_group):
        #todo add camera class, then add $, self.camera.apply_rect(self.map_rect)$ to the variable below
        screen.blit(self.map_img, (0,0))


        for sprite in player_group:
            screen.blit(sprite.image, self.camera.apply(sprite))





