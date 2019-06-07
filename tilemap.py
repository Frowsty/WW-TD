import pytmx
import pygame
import settings
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

class TiledMap:
    def __init__(self, filename):
        tm =  pytmx.load_pygame(filename, pixelalpha=True)
        # width is how many tiles across and tilewidth is how many pixels across each tile is
        self.width = tm.width * tm.tilewidth
        #height is how many tiles down and tile height is how many pixels high each tile is
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))


    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    def get_wh(self):
        return (self.width, self.height)