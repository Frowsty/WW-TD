import pygame





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

# Set screen size
size = [1280, 960]
FPS = 60


# ash's constants
_Multiplier = 1
SCREEN_WIDTH = 1280 * _Multiplier
SCREEN_HEIGHT = 1024 * _Multiplier
BLANK = None
DEBUG = False
Map_Shown = False

# Define Clock
clock = pygame.time.Clock()


start_game = False
how_to = False
PLAYER_SPEED = 10
PLAYER_HIT_RECT = pygame.Rect(0,0, 40, 40)
PLAYER_HEALTH = 100
PLAYER_ROT_SPEED = 10
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
BARREL_OFFSET = pygame.math.Vector2(30, 10)

BULLET_IMG = './images/bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 50,
                     'bullet_lifetime': 500,
                     'rate': 250,
                     'kickback': 20,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 40,
                      'bullet_lifetime': 350,
                      'rate': 900,
                      'kickback': 30,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12}
MUZZLE_FLASHES = ['./images/whitePuff15.png', './images/whitePuff16.png', './images/whitePuff17.png',
                  './images/whitePuff18.png']
# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [7, 15, 14, 9]
MOB_HIT_RECT = pygame.Rect(6,0, 25, 43)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 20
DETECT_RADIUS = 40
SPLAT = './images/splatgreen.png'
# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Effects


FLASH_DURATION = 50

NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "./images/light_350_soft.png"


#todo add items
# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'shotgun': 'obj_shotgun.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 10
BOB_SPEED = 0.3

#todo change sounds
# Sounds
BG_MUSIC = './sounds/12th_Street_Rag_1919.ogg'
PLAYER_HIT_SOUNDS = ['./sounds/pain/8.wav', './sounds/pain/9.wav', './sounds/pain/10.wav', './sounds/pain/11.wav']

ZOMBIE_HIT_SOUNDS = ['./sounds/splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['./sounds/barreta.wav']}
                 #'shotgun': ['./sounds/shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': './sounds/level_start.wav'}