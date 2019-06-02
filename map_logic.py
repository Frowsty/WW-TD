import random
import pygame
from pygame import freetype
import wang
import a_star
import os
from os import path


#initializers
if __name__ == 'main':
    pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
if not pygame.freetype.was_init():
    pygame.freetype.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

#constants
_Multiplier = 1
SCREEN_WIDTH = 1280 * _Multiplier
SCREEN_HEIGHT = 960 * _Multiplier
BLANK = None
DEBUG = False


#color constants
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (12, 255, 0)
DK_GREEN = (51, 102, 0)
BLUE = (18, 0, 255)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#GLOBALS
_Fullscreen_flag = False





_image_library = {}

def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
    return image

#follow the rabit hole, all classes run their calls to functions in game and main talks to game


#part of the map

class Game_Map(pygame.sprite.Sprite):
    def __init__(self, map_Sprite_Group, _Multiplier, screen):
        pygame.sprite.Sprite.__init__(self)
        self.trail_Points, self.end_Point, self.start = self.generate_Map(screen, _Multiplier, map_Sprite_Group)
        self.list_Of_Poi = self.poi_Generation(self.trail_Points)


    def screen_Grid(self, screen, columns, rows,_Multiplier):

        width = 80 *_Multiplier
        height = 80 *_Multiplier
        margin = round(2 *_Multiplier)
        upper_Left_X = screen.get_width() - (((columns +1) * width) + ((columns + 2) * margin))
        upper_Left_Y = screen.get_height() - (((rows + 1) * height) + ((rows + 2) * margin))
        lower_Right_Y = upper_Left_Y + (rows * height) + ((rows + 1) * margin)
        lower_Right_X = upper_Left_X + (columns * width) + (columns * margin)
        lower_Left_Y = lower_Right_Y
        lower_Left_X = upper_Left_X
        upper_Right_X = lower_Right_X
        upper_Right_Y = upper_Left_Y



        pygame.draw.rect(screen, (WHITE), ((upper_Left_X, upper_Left_Y), (lower_Right_X - (width //2) - (margin * 3), lower_Right_Y - (height //2) - (margin * 8))))
        pygame.draw.line(screen, BLACK, (upper_Left_X, upper_Left_Y), (upper_Right_X, upper_Right_Y), margin)
        for row in range(rows):
            for column in range(columns):
                pygame.draw.line(screen, BLACK, (upper_Left_X, upper_Left_Y + (row * height) + (row * margin)),
                                 (upper_Right_X, upper_Right_Y + (row * height) + (row * margin)))  # horizontal line
                pygame.draw.line(screen, BLACK, (upper_Left_X + (column * width) + (column * margin), upper_Left_Y), ((upper_Left_X + (column * width) + (column * margin) , lower_Left_Y)))  # vertical line

        pygame.draw.line(screen, BLACK, (upper_Right_X, upper_Right_Y), (lower_Right_X, lower_Right_Y), margin)
        pygame.draw.line(screen, BLACK, (lower_Left_X, lower_Left_Y), (lower_Right_X, lower_Right_Y), margin)


    def generate_Map(self, screen, _Multiplier, map_Sprite_Group):
        map_Grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        margin = 2
        num_Of_Rows = 10
        num_Of_Col = 14

        # starting node's locational data
        start_x = 1114
        selection = [40, 122, 204, 286, 368, 450, 532, 614, 696, 778]
        start_y = random.choice(selection)
        self.start = node(start_x, start_y, './images/placeholder/start.png', screen, _Multiplier)
        map_Sprite_Group.add(self.start)

        # trail logic
        o_Trail = road(screen, _Multiplier, start_x, start_y)
        trail_Nodes = []
        trail_Nodes.append(o_Trail.moving())

        while trail_Nodes[-1][0] > 122:
            trail_Nodes.append(o_Trail.moving())

        # end point creation
        self.end_Point = node(50, trail_Nodes[-1][1], './images/placeholder/end.png', screen, _Multiplier)
        map_Sprite_Group.add(self.end_Point)

        return trail_Nodes, self.end_Point, self.start


    def poi_Generation(self, trail_Nodes):
        # poi generation
        num_Of_Poi = random.randint(12, 20)
        names_Of_Poi = ["Hunter's Quarry", "Johnson's Sack", "Havagard's Hole", "Rustic Peak", "EastWard Tumble",
                        "Frank's Redhot",
                        "William's Child", "Magestic Gultch", "Trader's Point", "Kirkland's Endevor", "Widow's Peak",
                        "Chicken Run",
                        "Dodge City", "Angel's Howl", "Desolation Vale", "Jaggedally", "Violence Worth", "Barehallow",
                        "Bonetooth",
                        "Hope's Peak", "Wrath Brook", "Sandflats", "Talon's River", "Bruisestead", "Harmony Crag",
                        "Snake Canyon",
                        "Lightbrook", "Skullalley", "Phantom Rock"
                        ]
        closest_Point = random.sample(trail_Nodes, num_Of_Poi)
        dir = 'not'

        self.list_Of_Poi = []

        for i in range(len(closest_Point)):
            r = random.randint(0, 10)

            if r % 2 == 0:
                y_coord = closest_Point[i][1] + random.randint(0, 15)
                dir = 'positive'
            else:
                y_coord = closest_Point[i][1] - random.randint(0, 15)
                dir = 'negative'
            x_coord = closest_Point[i][0]
            name_Choice = random.choice(names_Of_Poi)
            self.list_Of_Poi.append((name_Choice, (x_coord, y_coord), dir))
            names_Of_Poi.remove(name_Choice)

        return self.list_Of_Poi


    def draw_Poi(self, screen):
        for i in range(len(self.list_Of_Poi)):
            print(i)
            x_coord = self.list_Of_Poi[i][1][0]
            y_coord = self.list_Of_Poi[i][1][1]
            pygame.draw.circle(screen, GREEN, (x_coord, y_coord), 5)
            font = pygame.freetype.Font(None, 10)
            dir = self.list_Of_Poi[i][2]
            name_Choice = self.list_Of_Poi[i][0]
            if dir == 'positive':
                font.render_to(screen, (x_coord + 10, y_coord + 10), name_Choice)
            elif dir == 'negative':
                font.render_to(screen, (x_coord - 10, y_coord - 10), name_Choice)


    def update(self):
        pass

    def draw(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(150)
        overlay.fill((WHITE))
        screen.blit(overlay, (0, 0))
        screen_Grid(screen, 14, 10, _Multiplier)
        draw_Poi(screen)
        pygame.draw.line(screen, DK_PURPLE, (trail_Points[0][0], trail_Points[0][1]), (start.return_Coords()))
        for i in range(len(trail_Points) - 2):
            pygame.draw.line(screen, DK_PURPLE, (trail_Points[i][0], trail_Points[i][1]),
                             (trail_Points[i + 1][0], trail_Points[i + 1][1]))
        pygame.draw.line(screen, DK_PURPLE, (trail_Points[-2][0], trail_Points[-2][1]), (end_Point.return_Coords()))
        draw_Poi(list_Of_Poi, screen)

class node(pygame.sprite.Sprite):
    def __init__(self, x, y, img, screen, _Multiplier):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image = get_image(img)
        self.images.append(self.image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass

    def return_Coords(self):
        return (self.rect.centerx, self.rect.centery)


class road():
    def __init__(self, screen, _Multiplier, start_x, start_y):
        self.starting_x = start_x
        self.starting_y = start_y
        self.road_Points = []
        self.road_Points.append((self.starting_x, self.starting_y))
        self.x = self.starting_x
        self.y = self.starting_y
        self.moving()

    def moving(self):
        move_y = random.randint(16, 27)
        move_x = random.randint(16, 27)
        self.x -= move_x
        if move_y % 2 == 0:
            self.y -= move_y
        else:
            self.y += move_y

        if self.y > (778 + 80):
            self.y -= (move_y * 2)
        elif self.y < 42:
            self.y += (move_y * 2)

        if self.x < 122:
            self.x = 122

        self.road_Points.append((self.x, self.y))
        return self.road_Points[-1][0], self.road_Points[-1][1]

