import pygame
import os
import math
from time import sleep
from random import uniform, choice, randint, random
import settings
from settings import *
from tilemap import collide_hit_rect
import ui_components as ui
import pytweening as tween
from itertools import chain

vec = pygame.math.Vector2

# Define colors
BLACK = (0, 0, 0)
GREY = (35, 35, 35)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_RED = (150, 0, 0)

YELLOW = (255, 255, 0)
DK_GREEN = (51, 102, 0)
ORANGE = (255, 186, 0)
SKYBLUE = (39, 145, 251)
PURPLE = (153, 51, 255)
DK_PURPLE = (102, 0, 204)
BROWN = (204, 153, 0)

def play_sound(file):
    if ui.enable_sound.get_state():
        return pygame.mixer.Sound(file).set_volume(0)
    else:
        return pygame.mixer.Sound(file).set_volume(0.3)


# ASH - image function, loads image into an array and if it has already been loaded, it loads the previous loaded image
# instead of wasting memory on a new image. if it hasn't been it loads it.
_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
    return image


def get_image_convert_alpha(path):
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path).convert_alpha()
    return image

vec = pygame.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y



class Player(pygame.sprite.Sprite):
    def __init__(self, dt, font, walls, projectile_Group, all_sprites, player_Sprite_Group, item_group, gun_flashes, screen, auto_reload, x, y):
        self.item_group = item_group
        self.walls = walls
        self.dt = dt
        self.projectile_group = projectile_Group
        self.all_Sprite_Group = all_sprites
        self.gun_flashes = gun_flashes
        self.player_Sprite_Group = player_Sprite_Group
        self.groups = self.all_Sprite_Group, self.player_Sprite_Group

        pygame.sprite.Sprite.__init__(self, self.groups)
        self.damaged = False
        self.auto_reload = auto_reload
        self.font = font
        self.screen = screen
        self.walkcount = 0
        self.player_frames = []
        self.frames = self.load_frames()
        self.image = self.player_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.reverse_frames = False
        self.ammo_max = 5
        self.current_ammo = 5
        self.reloading = False
        self.health = 100
        self.health_color = GREEN
        self.dead = False
        self.should_knockback = False
        self.knockback = 0
        self.weapon = 'pistol'
        self.clock = pygame.time.Clock()
        self.last_hit = self.fired_tick = self.reload_tick = pygame.time.get_ticks()
        self.bullets = []
        self.barrel_Offset = (25, 10) # in pixels
        self.dir_facing = 0 #dir in radians/angle
        self.mode = ''
        self.max_health = 100
        self.vel = pygame.math.Vector2(0,0)
        self.pos = pygame.math.Vector2(x,y)
        self.pressed_left = False
        self.pressed_right = False
        self.pressed_up = False
        self.pressed_down = False
        self.debug = False
        self.update_settings()
        self.sound_previous_state = False

        self.item_effect_current = False

        pygame.key.set_repeat(10,10)
        # Sound loading
        pygame.mixer.music.load(settings.BG_MUSIC)
        self.effects_sounds = {}
        for type in settings.EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(settings.EFFECTS_SOUNDS[type])
        self.weapon_sounds = {}
        for weapon in settings.WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in settings.WEAPON_SOUNDS[weapon]:
                s = pygame.mixer.Sound(snd)
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)

    def update_settings(self):

        if self.mode == "EASY":
            self.damage = 50
            self.health = 100
        if self.mode == "MEDIUM":
            self.damage = 34
            self.health = 75
        if self.mode == "HARD":
            self.damage = 25
            self.health = 50

    def pass_in(self, counter):
        self.counter = counter

    def in_camera(self, camcam):
        self.camcam = camcam

    def health_bar(self):

        if self.health > 75:
            self.health_color = GREEN
        elif self.health > 45 and self.health < 75:
            self.health_color = YELLOW
        elif self.health > 25 and self.health < 45:
            self.health_color = ORANGE
        elif self.health > 0 and self.health < 25:
            self.health_color = RED
        self.applied = self.camcam.apply_rect(self.rect)
        #print(self.applied)

        # The Healthbar
        pygame.draw.line(self.screen, self.health_color, (self.applied.x, self.applied.y - 15),
                         (self.applied.x + self.image.get_width() * (self.health / 100), self.applied.y - 15),
                         5)

        # Healthbar outline
        # TOP
        pygame.draw.line(self.screen, BLACK, (self.applied.x, self.applied.y - 18),
                         (self.applied.x + self.image.get_width() + 1, self.applied.y - 18), 2)
        # BOTTOM
        pygame.draw.line(self.screen, BLACK, (self.applied.x - 2, self.applied.y - 12),
                         (self.applied.x + self.image.get_width() + 2, self.applied.y - 12), 2)
        # LEFT
        pygame.draw.line(self.screen, BLACK, (self.applied.x - 2, self.applied.y - 18),
                         (self.applied.x - 2, self.applied.y - 12), 2)
        # RIGHT
        pygame.draw.line(self.screen, BLACK, (self.applied.x + self.image.get_width() + 1, self.applied.y - 18),
                         (self.applied.x + self.image.get_width() + 1, self.applied.y - 12), 2)

    def load_frames(self):
        self.player_frames.append(get_image("character_frames/character_main.png"))
        self.player_frames.append(get_image("character_frames/character_reload.png"))

    def hit(self):
        if pygame.time.get_ticks() - self.last_hit  > 500:
            self.health -= settings.MOB_DAMAGE
            self.last_hit = pygame.time.get_ticks()
            dir = randint(0, 360)
            self.damaged = True
            self.damage_alpha = chain(settings.DAMAGE_ALPHA * 4)
            self.pos += vec(MOB_KNOCKBACK, 0).rotate(dir)



    def ammo_reload_toggle(self, state):
        self.ammo_reload = state

    def update(self):

        self.get_keys()
        self.ammo_reload_toggle(ui.auto_reload.get_state())
        if self.debug:
            print("...updating...")
            print("ammo_reload checked")

        if self.health <= 0:
            self.health = 0
        if self.health > 0:
            self.dead = False
        else:
            self.dead = True

        if self.auto_reload == True and self.current_ammo == 0:
            self.reload()

        self.actions()
        if ui.enable_sound.get_state() == True and self.sound_previous_state == False:
            self.toggle_sound(0)
            self.sound_previous_state = True
        elif ui.enable_sound.get_state() == False and self.sound_previous_state == True:
            self.toggle_sound(0.3)
            self.sound_previous_state = False
        else:
            pass

        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False


    def move_rect(self, x, y):
        self.pos.x = x
        self.pos.y = y

    def pass_events(self, events):
        self.events = events

    def get_keys(self):

        if self.debug:
            print("getting_keys")

        for event in self.events:
            self.vel = vec(0,0)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:  # check for key presses
                if event.key == pygame.K_h:
                    self.debug = not self.debug
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:  # left arrow turns left
                    self.vel = pygame.math.Vector2(-settings.PLAYER_SPEED, 0)
                    self.image = pygame.transform.rotate(self.player_frames[self.walkcount], 180)
                    self.barrel_Offset = (-25, -10)
                    self.dir_facing = 180
                    if self.debug:
                        print("going left")
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:  # right arrow turns right
                    self.vel = pygame.math.Vector2(settings.PLAYER_SPEED, 0)
                    self.image = self.player_frames[self.walkcount]
                    self.barrel_Offset = (25, 10)
                    self.dir_facing = 0
                    if self.debug:
                        print("going right")
                if event.key == pygame.K_UP or event.key == pygame.K_w:  # up arrow goes up
                    self.vel = pygame.math.Vector2(0, -settings.PLAYER_SPEED)
                    self.image = pygame.transform.rotate(self.player_frames[self.walkcount], 90)
                    self.barrel_Offset = (10, -25)
                    self.dir_facing = 270
                    if self.debug:
                        print('going up')
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:  # down arrow goes down
                    self.vel = pygame.math.Vector2(0, settings.PLAYER_SPEED)
                    self.image = pygame.transform.rotate(self.player_frames[self.walkcount], -90)
                    self.barrel_Offset = (-10, 25)
                    self.dir_facing = 90
                    if self.debug:
                        print("going down")
                if event.key == pygame.K_SPACE:
                    self.shoot()

                if event.key == pygame.K_r:
                    self.reload()

    def toggle_sound(self, x):
        self.weapon_sounds = {}
        for weapon in settings.WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in settings.WEAPON_SOUNDS[weapon]:
                s = pygame.mixer.Sound(snd)
                s.set_volume(x)
                self.weapon_sounds[weapon].append(s)
        t = './sounds/shells.wav'
        pygame.mixer.Sound(t).set_volume(x)
        self.effects_sounds = {}
        for type in settings.EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(settings.EFFECTS_SOUNDS[type])
            self.effects_sounds[type].set_volume(x)





    def reload(self):
        if self.current_ammo < self.ammo_max:
            self.reloading = True
            while self.current_ammo != self.ammo_max:
                if (pygame.time.get_ticks() - self.reload_tick) >= 250:
                    t = './sounds/shells.wav'
                    u = pygame.mixer.Sound(t)
                    u.play()

                    self.current_ammo += 1
                    self.walkcount = 1
                    self.reload_tick = pygame.time.get_ticks()

            if self.current_ammo == self.ammo_max:
                self.reloading = False
                self.walkcount = 0


    def actions(self):
        if self.debug:
            print("getting actions")

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.walls, 'y')
        self.rect.center = self.hit_rect.center

    def shoot(self):
        if self.debug:
            print("shooting..")
        if (pygame.time.get_ticks() - self.fired_tick) >= 500:
            self.fired_tick = pygame.time.get_ticks()
            if self.current_ammo > 0:
                self.current_ammo -= 1

                self.bullets.append(Projectile(self, self.walls, self.projectile_group, self.gun_flashes,
                                               self.all_Sprite_Group, self.barrel_Offset, self.rect.center, self.dir_facing,
                                               self.damage, self.dt))
                snd = choice(self.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
                if self.debug:
                    print("Current_ammo " + str(self.current_ammo))
                    print("Auto reload set to " + str(self.auto_reload))
                    print("auto reload box set to " + str(self.ammo_reload_toggle(ui.auto_reload.get_state())))
            if self.current_ammo == 0 and self.auto_reload == True:
                reload()


    def draw(self):
        #print(ui.show_healthbar.get_state())
        if ui.show_healthbar.get_state():
            self.health_bar()





class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, enemy_Sprite_Group, screen, player, walls, dt, camcam, all_sprites, counter):
        self.counter = counter
        self.all_sprites = all_sprites
        self.camcam = camcam
        self.walls = walls
        self.dt = dt
        self.player = player
        self.enemies = enemy_Sprite_Group
        self.screen = screen
        self.enemy_Sprite_Group = enemy_Sprite_Group
        self.groups = self.enemy_Sprite_Group, self.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.orig_image = get_image("character_frames/enemy_knife.png")
        self.image = self.orig_image
        self.rect = self.image.get_rect()

        self.pos = vec(x, y)

        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0




        self.bullets = []
        self.walkcount = 0
        self.hit_rect = settings.MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        # self.frames = self.load_frames()
        self.health = settings.MOB_HEALTH
        self.speed = choice(settings.MOB_SPEEDS)
        self.accelerate = pygame.math.Vector2(0, 0)
        self.hit_target_tick = pygame.time.get_ticks()
        self.hit_player = False

        self.target = self.player
        self.splat = get_image(settings.SPLAT)

    def health_bar(self):

        if self.health > 75:
            self.health_color = GREEN
        elif self.health > 45 and self.health < 75:
            self.health_color = YELLOW
        elif self.health > 25 and self.health < 45:
            self.health_color = ORANGE
        elif self.health > 0 and self.health < 25:
            self.health_color = RED
        self.applied = self.camcam.apply_rect(self.rect)


        # The Healthbar
        pygame.draw.line(self.screen, self.health_color, (self.applied.x, self.applied.y - 15),
                         (self.applied.x + self.image.get_width() * (self.health / 100), self.applied.y - 15),
                         5)

        # Healthbar outline
        # TOP
        pygame.draw.line(self.screen, BLACK, (self.applied.x, self.applied.y - 18),
                         (self.applied.x + self.image.get_width() + 1, self.applied.y - 18), 2)
        # BOTTOM
        pygame.draw.line(self.screen, BLACK, (self.applied.x - 2, self.applied.y - 12),
                         (self.applied.x + self.image.get_width() + 2, self.applied.y - 12), 2)
        # LEFT
        pygame.draw.line(self.screen, BLACK, (self.applied.x - 2, self.applied.y - 18),
                         (self.applied.x - 2, self.applied.y - 12), 2)
        # RIGHT
        pygame.draw.line(self.screen, BLACK, (self.applied.x + self.image.get_width() + 1, self.applied.y - 18),
                         (self.applied.x + self.image.get_width() + 1, self.applied.y - 12), 2)



    def draw(self):
        self.screen.blit(self.image, self.rect)
        if ui.show_healthbar.get_state():
            self.health_bar()

    def update(self):
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < settings.DETECT_RADIUS ** 2:
            #if random() < 0.002:
            #    choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pygame.transform.rotate(self.orig_image, self.rot)
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            try:
                self.acc.scale_to_length(self.speed)
            except:
                self.acc = vec(0,0)
            self.acc += self.vel * -1
            self.vel += self.acc * self.dt
            self.pos += (self.vel * self.dt) + (0.5 * self.acc * self.dt ** 2)
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            #choice(self.game.zombie_hit_sounds).play()
            if self.counter == False:
                pass
            else:
                self.counter.counter_adj(1)
            self.kill()
            #self.map_img.blit(self.splat, self.pos - vec(32, 32))

    def avoid_mobs(self):
        for mob in self.enemies:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < settings.AVOID_RADIUS:
                    self.acc += dist.normalize()

    def health_hit(self, amt):
        self.health -= amt

class Projectile(pygame.sprite.Sprite):
    """
    Projectile - spawns a projectile from a given position at a given direction that does a given amount of damage
    first pass through the groups:
               player
               walls
               bullets
               gun_flashes
               all_sprites
    then pass in the position
               pos
    the direction
               dir
    then finally the damage
               damage

    """


    def __init__(self, player, walls, bullets, gun_flashes, all_sprites, barrel_offset, pos, dir, damage, dt):
        #groups and player instance that spawned the projectile are passed in for easy reference
        #pygame sprite is initialized to give sprite functionality to the instance and allows for
        #the sprite to auto added to the groups without naming it
        self.dt = dt
        self.gun_flashes = gun_flashes
        self.player = player
        self.walls = walls
        self.bullets = bullets
        self.all_sprites = all_sprites
        self.groups = self.all_sprites, self.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        #bullet image is set to bullet image
        self.image = get_image_convert_alpha('./images/bullet.png')
        # position is calculated as a position along a vector from the math module
        self.x = pos[0]
        self.y = pos[1]
        self.x = self.x + barrel_offset[0]
        self.y = self.y + barrel_offset[1]

        self.pos = pygame.math.Vector2(self.x, self.y)
        #rect is the actual space the bullet takes up (0,0, width, height)

        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pos
        self.hit_rect = self.rect
        #hit_rect is used for collision detection, same as rect but can be different
        self.hit_rect = self.rect



        #spread allows for random direction from the gun mimicking possible aimming difficulty
        #while still shooting the basic direction of the gun
        dir = vec(1,0).rotate(dir)
        spread = uniform(-settings.WEAPONS[self.player.weapon]['spread'], settings.WEAPONS[self.player.weapon]['spread'])
        self.dir = dir.rotate(spread)
        #math used to determine velocity based on the speed, direction and then a small uniform range
        self.vel = self.dir * settings.WEAPONS[self.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        #sets the spawn time
        self.spawn_time = pygame.time.get_ticks()
        #sets the damage of the bullet
        self.damage = damage
        self.flash = MuzzleFlash((self.x, self.y), self.all_sprites, self.gun_flashes)

    def update(self):
        #updates position by adding velocity and the delta time to the position
        self.pos += self.vel * self.dt
        #updates the rect to the bullets position, the rect updating is what updates the image that's beeing blitted
        self.rect.center = self.pos
        #sets the bullet to kill itself if it hits a wall or runs out of life (max distance)
        if pygame.sprite.spritecollideany(self, self.walls):
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > settings.WEAPONS[self.player.weapon]['bullet_lifetime']:
            self.kill()



class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, walls):
        self.walls = walls
        self.groups = self.walls
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def move(self, x, y):
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y



class Objective(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, objective):
        self.objective = objective
        self.groups = self.objective
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, pos, all_sprites, gun_flashes):
        self.gun_flashes = gun_flashes
        self.all_sprites = all_sprites

        self.groups = self.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        size = randint(20, 50)
        self.image = pygame.transform.scale(choice(self.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > settings.FLASH_DURATION:
            self.kill()

#todo add a counter class with number of enemies left
#todo hook the ui into the random encounters encounter
#todo make 3 more quick levels for the random encounters
#todo make a few more scenarios...
class Counter(pygame.sprite.Sprite):
    def __init__(self, count, all_sprite):
        self.count = count
        self.all_sprite = all_sprite
        self.groups = self.all_sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = get_image('./images/target_left.png')
        self.rect = self.image.get_rect()
        self.rect.x = settings.SCREEN_WIDTH - 80
        self.rect.y = settings.SCREEN_HEIGHT - 80
        self.font = pygame.font.SysFont("Arial", 20)

    def counter_adj(self, amt):
        self.count -= amt

    def text(self):
        self.text_cont = self.font.render(f"{self.count}x", True, BLACK)

    def update(self):
        self.text()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.screen.blit(self.text_cont, (settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT - ((80-(80 - 64))//2)))

class food(pygame.sprite.Sprite):
    def __init__(self, x, y, enemies, screen, player, walls, dt, camcam, all_Sprite_Group, counter, item_group):
        print("dropped an item")
        self.x = x
        self.y = y
        self.enemies = enemies
        self.screen = screen
        self.player = player
        self.walls = walls
        self.dt = dt
        self.camcam = camcam
        self.all_Sprite_Group = all_Sprite_Group
        self.counter = counter
        self.item_Group = item_group


        self.groups = self.all_Sprite_Group, self.item_Group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.type, self.img = choice(list(settings.ITEM_IMAGES.items()))
        self.image = get_image_convert_alpha(self.img)
        self.rect = self.image.get_rect()
        self.pos = vec(0,0)
        self.pos.x = x
        self.pos.y = y
        self.rect.center = self.pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = settings.BOB_RANGE * (self.tween(self.step / settings.BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += settings.BOB_SPEED
        if self.step > settings.BOB_RANGE:
            self.step = 0
            self.dir *= -1

class item_pick_up(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, player):
        self.player = player
        self.x = x
        self.y = y
        self.all_sprites = all_sprites
        self.groups = self.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.img = []
        self.load_images()
        self.image = self.img[0]
        self.rect = self.image.get_rect()
        self.count = 0
        self.div_count = 0

    def load_images(self):
        for i in range(8):
            temp = get_image('./images/effects/tile00%s.png' % i)
            self.img.append(temp)

    def update(self):
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.count += 1
        if self.count % 16 == 0:
            self.div_count = self.count % 16
        if self.div_count == 9:
            self.kill()
        self.image = self.img[self.div_count]
