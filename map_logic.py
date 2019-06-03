import random
import pygame
from pygame import font
from pygame.math import Vector2
import wang
import a_star
import os
from os import path


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

#follow the rabit hole, all classes run their calls to functions in game and main talks to game
class CL_Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, value):
        pygame.sprite.Sprite.__init__(self)
        self.location = []
        self.location.append(x)
        self.location.append(y)
        img = []
        img.append(get_image(self.set_terrain_image(value)))
        self.image = img[0]
        self.rect = self.image.get_rect()
        self.rect.x = (self.location[1] * 82) + 42
        self.rect.y = (self.location[0] * 82) + 42

    def set_terrain_image(self, value):
        if value == 0:
            return './images/sprites/terrain/tile000.png'
        elif value == 1:
            return './images/sprites/terrain/tile001.png'
        elif value == 2:
            return './images/sprites/terrain/tile002.png'
        elif value == 3:
            return './images/sprites/terrain/tile003.png'
        elif value == 4:
            return './images/sprites/terrain/tile004.png'
        elif value == 5:
            return './images/sprites/terrain/tile005.png'
        elif value == 6:
            return './images/sprites/terrain/tile006.png'
        elif value == 7:
            return './images/sprites/terrain/tile007.png'
        elif value == 8:
            return './images/sprites/terrain/tile008.png'
        elif value == 9:
            return './images/sprites/terrain/tile009.png'
        elif value == 10:
            return './images/sprites/terrain/tile010.png'
        elif value == 11:
            return './images/sprites/terrain/tile011.png'
        elif value == 12:
            return './images/sprites/terrain/tile012.png'
        elif value == 13:
            return './images/sprites/terrain/tile013.png'
        elif value == 14:
            return './images/sprites/terrain/tile014.png'
        elif value == 15:
            return './images/sprites/terrain/tile015.png'


#part of the map

class Base_grid(pygame.sprite.Sprite):
    def __init__(self, screen, _Multiplier):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image('images/placeholder/empty.png')
        self.rect = self.image.get_rect()



    def screen_Grid(self, screen, columns, rows, _Multiplier):

        width = 80 * _Multiplier
        height = 80 * _Multiplier
        margin = round(2 * _Multiplier)
        upper_Left_X = screen.get_width() - (((columns + 1) * width) + ((columns + 2) * margin))
        upper_Left_Y = screen.get_height() - (((rows + 1) * height) + ((rows + 2) * margin))
        lower_Right_Y = upper_Left_Y + (rows * height) + ((rows + 1) * margin)
        lower_Right_X = upper_Left_X + (columns * width) + (columns * margin)
        lower_Left_Y = lower_Right_Y
        lower_Left_X = upper_Left_X
        upper_Right_X = lower_Right_X
        upper_Right_Y = upper_Left_Y

        pygame.draw.rect(screen, (WHITE), ((upper_Left_X, upper_Left_Y), (
        lower_Right_X - (width // 2) - (margin * 3), lower_Right_Y - (height // 2) - (margin * 8))))
        pygame.draw.line(screen, BLACK, (upper_Left_X, upper_Left_Y), (upper_Right_X, upper_Right_Y), margin)
        for row in range(rows):
            for column in range(columns):
                pygame.draw.line(screen, BLACK, (upper_Left_X, upper_Left_Y + (row * height) + (row * margin)),
                                 (
                                 upper_Right_X, upper_Right_Y + (row * height) + (row * margin)))  # horizontal line
                pygame.draw.line(screen, BLACK, (upper_Left_X + (column * width) + (column * margin), upper_Left_Y),
                                 ((upper_Left_X + (column * width) + (column * margin),
                                   lower_Left_Y)))  # vertical line

        pygame.draw.line(screen, BLACK, (upper_Right_X, upper_Right_Y), (lower_Right_X, lower_Right_Y), margin)
        pygame.draw.line(screen, BLACK, (lower_Left_X, lower_Left_Y), (lower_Right_X, lower_Right_Y), margin)

    def draw(self, screen):
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(150)
        overlay.fill((WHITE))
        screen.blit(overlay, (0, 0))
        self.screen_Grid(screen, 14, 10, _Multiplier)

class counter(pygame.sprite.Sprite):
    def __init__(self, screen, pos, start_time):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.load_images()

    def load_images(self):
        #todo img = get_image('./images/counter/')
        pass

class map_Player_Icon(pygame.sprite.Sprite):
    def __init__(self, screen, pos, waypoints):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.load_images()
        self.image = self.images[0]
        self.img_counter = 0
        self.speed = 1
        self.vel = Vector2(0,0)
        self.rect = self.image.get_rect(center=pos)
        self.max_speed = 10
        self.pos = Vector2(pos)
        self.waypoints = waypoints
        self.waypoint_index = 0
        self.target = self.waypoints[self.waypoint_index]
        self.target_radius = 50
        self.moving = False

    def load_images(self):
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon1.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon2.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon3.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon4.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon5.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon6.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon7.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon8.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon9.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon10.png')
        img = pygame.transform.scale(img, (50, 50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon11.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon12.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon13.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon14.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon15.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)
        img = get_image('./images/placeholder/map_icon/cowboy_map_icon16.png')
        img = pygame.transform.scale(img, (50,50))
        self.images.append(img)

    def update(self):
        if self.moving == True:
            #vector pointing to the target
            heading = self.target - self.pos
            #distance to target
            distance = heading.length()

            heading.normalize_ip()
            if distance <= 4:
                #get closer than 4 pixels (so basically right on it
                self.waypoint_index = (self.waypoint_index + 1) % len(self.waypoints)
                self.target = self.waypoints[self.waypoint_index]
            if distance <= self.target_radius:
                #if we're approaching, then slow down
                self.vel = heading * (distance / self.target_radius * self.max_speed)
            else:
                self.vel = heading * self.max_speed

            self.pos += self.vel
            self.rect.center = self.pos
        else:
            self.pos = self.pos

    def draw(self):
        if self.moving == True:
            self.img_counter += 1
            if self.img_counter > len(self.images):
                self.img_counter = 0
            self.image = self.images[self.img_counter]
        else:
            self.image = self.images[0]
            self.img_counter = 0

    def toggle_movement(self):
        self.moving = not self.moving


class GameMapController(pygame.sprite.Sprite):
    def __init__(self, map_Sprite_Group, _Multiplier, screen, terrain_sprites, mpi_Group):
        pygame.sprite.Sprite.__init__(self)
        self.trail_Points, self.end_Point, self.start = self.generate_Map(screen, _Multiplier, map_Sprite_Group, terrain_sprites, mpi_Group)
        self.list_Of_Poi = self.poi_Generation(self.trail_Points)
        self.image = get_image('./images/placeholder/plain.png')
        self.rect = self.image.get_rect()
        self.rect.x = -200
        self.rect.y = 200

    def generate_Map(self, screen, _Multiplier, map_Sprite_Group, terrain_sprites, mpi_Group):
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

        self.terrain_list = list()
        self.terrain = wang.wang_set(width = 14, height = 10)
        for i in range(len(self.terrain)):
            for j in range(len(self.terrain[0])):
                x = i
                y = j
                value = self.terrain[i][j]
                self.terrain_list.append(CL_Terrain(x, y, value))
                terrain_sprites.add(self.terrain_list[-1])


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
        self.trail_Nodes = []
        self.trail_Nodes.append(o_Trail.moving())

        while self.trail_Nodes[-1][0] > 122:
            self.trail_Nodes.append(o_Trail.moving())

        # end point creation
        self.end_Point = node(50, self.trail_Nodes[-1][1], './images/placeholder/end.png', screen, _Multiplier)
        map_Sprite_Group.add(self.end_Point)

        self.player_icon = map_Player_Icon(screen, self.start.return_Coords(), self.trail_Nodes)
        mpi_Group.add(self.player_icon)

        return self.trail_Nodes, self.end_Point, self.start


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

            if 120 > closest_Point[i][1]:
                dir = 'positive'
                y_coord = closest_Point[i][1] + random.randint(0, 15)
            elif closest_Point[i][1] > 120:
                dir = 'negative'
                y_coord = closest_Point[i][1] - random.randint(0, 15)
            else:
                dir = 'negative'
            x_coord = closest_Point[i][0]
            name_Choice = random.choice(names_Of_Poi)
            self.list_Of_Poi.append((name_Choice, (x_coord, y_coord), dir))
            names_Of_Poi.remove(name_Choice)

        return self.list_Of_Poi


    def draw_Poi(self, screen):
        for i in range(len(self.list_Of_Poi)):
            x_coord = self.list_Of_Poi[i][1][0]
            y_coord = self.list_Of_Poi[i][1][1]
            pygame.draw.circle(screen, GREEN, (x_coord, y_coord), 5)
            font = pygame.font.Font(None, 22)
            dir = self.list_Of_Poi[i][2]
            name_Choice = self.list_Of_Poi[i][0]
            if dir == 'positive':
                f = font.render(name_Choice, True, BLACK)
                f = pygame.transform.rotate(f, 90)
                screen.blit(f, (x_coord, y_coord - 140))
            elif dir == 'negative':
                f = font.render(name_Choice, True, BLACK)
                f = pygame.transform.rotate(f, -90)
                screen.blit(f, (x_coord, y_coord + 30))





    def update(self):
        pass

    def draw(self, screen):
        self.draw_Poi(screen)
        pygame.draw.line(screen, DK_PURPLE, (self.trail_Points[0][0], self.trail_Points[0][1]), (self.start.return_Coords()), 5)
        for i in range(len(self.trail_Points) - 2):
            pygame.draw.line(screen, DK_PURPLE, (self.trail_Points[i][0], self.trail_Points[i][1]),
                             (self.trail_Points[i + 1][0], self.trail_Points[i + 1][1]), 5)
        pygame.draw.line(screen, DK_PURPLE, (self.trail_Points[-2][0], self.trail_Points[-2][1]), (self.end_Point.return_Coords()), 5)





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

    def draw(self, screen):
        pass


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