import pygame
import os

class Player():

    def __init__(self, start_pos=[0,0]):
        self.start_pos = start_pos
        self.cur_pos = start_pos
        self.frames = [pygame.image.load("character_frames/frame_1.gif"), pygame.image.load("character_frames/frame_2.gif"),
                       pygame.image.load("character_frames/frame_3.gif"), pygame.image.load("character_frames/frame_4.gif")]
        self.walkcount = 0
        self.reverse_frames = False
        self.player_facing = 0

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
            self.cur_pos[1] -= 10
            self.cycle_animation()
            self.player_facing = 0

        if pygame.key.get_pressed()[pygame.K_s]:
            self.cur_pos[1] += 10
            self.cycle_animation()
            self.player_facing = 2
        
        if pygame.key.get_pressed()[pygame.K_a]:
            self.cur_pos[0] -= 10
            self.cycle_animation()
            self.player_facing = 1

        if pygame.key.get_pressed()[pygame.K_d]:
            self.cur_pos[0] += 10
            self.cycle_animation()
            self.player_facing = 3
    
    def draw(self, screen):

        if self.player_facing == 0:
            screen.blit(self.frames[self.walkcount], self.cur_pos)
        if self.player_facing == 1:
            screen.blit(pygame.transform.rotate(self.frames[self.walkcount], 90), self.cur_pos)
        if self.player_facing == 2:
            screen.blit(pygame.transform.rotate(self.frames[self.walkcount], 180), self.cur_pos)
        if self.player_facing == 3:
            screen.blit(pygame.transform.rotate(self.frames[self.walkcount], -90), self.cur_pos)