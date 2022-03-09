# import pygame
import pygame
import random

# import key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("pygame_spaceship/pic/plane.png").convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf, 0, 1/16)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # move sprite
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# enemy object
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("pygame_spaceship/pic/missile.png").convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf, 90, 1/18)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 12)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# cloud object
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("pygame_spaceship/pic/cloud{}.png".format(random.randint(1,3))).convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf , 0, 1/3)
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH+20, SCREEN_WIDTH+100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()


# initialize
pygame.init()

# screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# custom event for adding new enemy and cloud
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# instantiate player
player = Player()

# create sprite groups
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
# add player to sprite groups
all_sprites.add(player)

# setup clock for framerate
clock = pygame.time.Clock()

# main loop
running = True
while running:
    # loop every event
    for event in pygame.event.get():
        # key is pressed
        if event.type == KEYDOWN:
            # escape key is press
            if event.key == K_ESCAPE:
                running = False

        # click close button
        elif event.type == QUIT:
            running = False

        # add new enemy
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # add new cloud
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # get keypress and update player sprite
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # update position of enemy and cloud
    enemies.update()
    clouds.update()

    # fill the screen with blue
    screen.fill((135, 206, 250))

    # draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # check if any enemies have collided with player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # update display
    pygame.display.flip()

    clock.tick(60)