import pygame
import os

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


class Player(pygame.sprite.Sprite):

    def __init__(self, start_pos=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.start_pos = start_pos
        self.cur_pos = start_pos
        self.images = []
        self.load_images()
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = start_pos[0]
        self.rect.y = start_pos[1]
        self.walkcount = 0
        self.reverse_frames = False
        self.player_facing = 0
        self.speed = 12

    def load_images(self):
        self.images.append(get_image("character_frames/frame1.png"))
        self.images.append(get_image("character_frames/frame2.png"))
        self.images.append(get_image("character_frames/frame3.png"))
        self.images.append(get_image("character_frames/frame4.png"))

    def cycle_animation(self):

        if self.reverse_frames == True:
            self.walkcount -= 1
        else:
            self.walkcount += 1

        if self.walkcount == 3:
            self.reverse_frames = True
        if self.walkcount == 0 and self.reverse_frames == True:
            self.reverse_frames = False


    def actions(self, screen, get_key):

        if pygame.key.get_pressed()[pygame.K_w]:
            self.rect.y -= self.speed
            self.cycle_animation()
            self.player_facing = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.rect.y += self.speed
            self.cycle_animation()
            self.player_facing = 2

        
        if pygame.key.get_pressed()[pygame.K_a]:
            self.rect.x -= self.speed
            self.cycle_animation()
            self.player_facing = 1

        if pygame.key.get_pressed()[pygame.K_d]:
            self.rect.x += self.speed
            self.cycle_animation()
            self.player_facing = 3
    
    def update(self):

        if self.player_facing == 0:
            self.image = self.images[self.walkcount]
        elif self.player_facing == 1:
            self.image = self.images[self.walkcount]
            self.image = pygame.transform.rotate(self.images[self.walkcount], 90)
        elif self.player_facing == 2:
            self.image = self.images[self.walkcount]
            self.image = pygame.transform.rotate(self.images[self.walkcount], 180)
        elif self.player_facing == 3:
            self.image = self.images[self.walkcount]
            self.image = pygame.transform.rotate(self.images[self.walkcount], -90)

    def draw(self, screen):
        pass