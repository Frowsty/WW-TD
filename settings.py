import pygame


if not pygame.display.get_init():
    pygame.display.init()
pygame.font.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()


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

TILESIZE = 64
start_game = False
how_to = False
PLAYER_SPEED = 200
PLAYER_HIT_RECT = pygame.Rect(0,0, 40, 40)
PLAYER_HEALTH = 100
PLAYER_ROT_SPEED = 10
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
BARREL_OFFSET = pygame.math.Vector2(30, 10)

BULLET_IMG = './images/bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 500,
                     'rate': 250,
                     'kickback': 20,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1}
WEAPONS['shotgun'] = {'bullet_speed': 400,
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
MOB_SPEEDS = [50, 60, 75, 90]
MOB_HIT_RECT = pygame.Rect(6,0, 25, 43)
MOB_HEALTH = 100
MOB_DAMAGE = 15
MOB_KNOCKBACK = 80
AVOID_RADIUS = 40
DETECT_RADIUS = 400
SPLAT = './images/splatgreen.png'
# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Effects


FLASH_DURATION = 15

NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "./images/light_350_soft.png"


#todo add items
# Items

#ITEM_IMAGES = {'health': 'health_pack.png',
#               'shotgun': 'obj_shotgun.png'}

ITEM_IMAGES = {'pepper': './images/food/1.png', 'candy': './images/food/2.png', 'jello': './images/food/3.png',
               'cake': './images/food/4.png', 'blue potion': './images/food/5.png',
               'orange potion': './images/food/6.png', 'green potion': './images/food/7.png',
               'purple potion': './images/food/8.png', 'red potion': './images/food/9.png',
               'orange ball': './images/food/10.png',
                'blue ball': './images/food/11.png',
                'purple ball': './images/food/12.png',
                'green ball': './images/food/13.png', 'red ball': './images/food/14.png',
                'half of a pear': './images/food/15.png', 'half an apple': './images/food/16.png',
                'half of an orange': './images/food/17.png', 'half a tomato': './images/food/18.png',
                'sliced pear': './images/food/19.png', 'sliced apple': './images/food/20.png',
                'sliced orange': './images/food/21.png', 'sliced tomato': './images/food/22.png',
                'pear': './images/food/23.png', 'apple': './images/food/24.png',
                'tomato': './images/food/25.png', 'orange': './images/food/26.png',
                'carrot': './images/food/27.png', 'half a carrot': './images/food/28.png',
                'peeled bannana': './images/food/29.png', 'bannana': './images/food/30.png',
                'grapes': './images/food/31.png', 'cherry': './images/food/32.png',
                'lemon': './images/food/33.png', 'peach': './images/food/34.png',
                'raddish': './images/food/35.png'}

SCRAP_IMAGES = {'shield': './images/scrap/icon_04.png',
                'spike': './images/scrap/icon_16.png',
                'spike2': './images/scrap/icon_43.png',
                'scrap door': './images/scrap/icon_44.png'
                }


CARDS =  {'wheel': './images/cards/broken_wheel.png', 'tip': './images/cards/wagon_tip.png',
          'attack': './images/cards/attack.png'}
V_EFFECTS = {'item_pickup': './images/effects/tile00'}

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 32
BOB_SPEED = 0.6

#todo change sounds
# Sounds
BG_MUSIC = './sounds/12th_Street_Rag_1919.ogg'
PLAYER_HIT_SOUNDS = ['./sounds/pain/8.wav', './sounds/pain/9.wav', './sounds/pain/10.wav', './sounds/pain/11.wav']

ZOMBIE_HIT_SOUNDS = ['./sounds/splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['./sounds/barreta.wav']}
                 #'shotgun': ['./sounds/shotgun.wav']}
EFFECTS_SOUNDS = {'level_start': './sounds/level_start.wav'}

phs = []
for snd in PLAYER_HIT_SOUNDS:
    phs.append(pygame.mixer.Sound(snd))