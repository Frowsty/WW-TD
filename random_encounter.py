import pygame
import random
import os
from os import path
import map_logic

_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert()
    return image


class random_Encounter():
    def __init__(self, screen):
        self.looping = True
        self.loop(screen)



    def loop(self,screen):
        while self.looping:
            pygame.event.pump()
            screen.fill((0,0,0))
            image = get_image('./images/cards/broken_wheel.png')
            screen.blit(image, (100,100) )

            pygame.display.flip()
            pass

    def select_map(self):
        pass

    def select_encounter(self):
        pass

    def select_posture(self):
        #randomly selects hostile or passive or friendly
        #only triggures on encounters with people or animals
        pass



