import pygame

# initializers
if __name__ == 'main':
    pygame.init()
if not pygame.display.get_init():
    pygame.display.init()
pygame.font.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

# sprite groups
all_Sprite_Group = pygame.sprite.Group()
map_Sprite_Group = pygame.sprite.Group()
terrain_sprites = pygame.sprite.Group()
mpi_Group = pygame.sprite.Group()
player_Sprite_Group = pygame.sprite.Group()
projectile_Sprite_Group = pygame.sprite.Group()
enemy_Sprite_Group = pygame.sprite.Group()

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


# ash's constants
_Multiplier = 1
SCREEN_WIDTH = 1280 * _Multiplier
SCREEN_HEIGHT = 1024 * _Multiplier
BLANK = None
DEBUG = False
Map_Shown = False

# Define Clock
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 20)
ammo_font = pygame.font.SysFont("Arial", 30)

start_game = False
how_to = False
PLAYER_SPEED = 100