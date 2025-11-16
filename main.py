import sys

import pygame

WIDTH = 700
HEIGHT = 406
SPRITE_WIDTH = 30
SPRITE_HEIGHT = 30

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class GameObject:
    def __init__(self, asset, height, speed):
        self.speed = speed
        self.asset = asset
        self.pos = asset.get_rect().move(
            0, height
        )  # Get the Rect for the asset's Surface and move it

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed
        if self.pos.right > WIDTH:
            self.pos.left = 0
        if self.pos.top > HEIGHT - SPRITE_HEIGHT:
            self.pos.top = 0
        if self.pos.right < SPRITE_WIDTH:
            self.pos.right = WIDTH
        if self.pos.top < 0:
            self.pos.top = HEIGHT - SPRITE_HEIGHT


# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load background asset
background = pygame.image.load("images/background.bmp").convert()

# Load player asset
# player_radius = SPRITE_WIDTH / 2
# player = pygame.Surface(
# (player_radius * 2, player_radius * 2), pygame.SRCALPHA
# ).convert()
# pygame.draw.circle(player, GREEN, (player_radius, player_radius), player_radius)
player = pygame.image.load("images/turtle.png").convert_alpha()

# Load non-player assets
entity_radius = SPRITE_WIDTH / 2
entity = pygame.Surface(
    (entity_radius * 2, entity_radius * 2), pygame.SRCALPHA
).convert()
pygame.draw.circle(entity, RED, (entity_radius, entity_radius), entity_radius)

screen.blit(background, (0, 0))
objects = []
p = GameObject(player, 10, 3)  # create the player object
for x in range(10):  # create 10 objects</i>
    o = GameObject(entity, x * 40, x)
    objects.append(o)
while True:
    screen.blit(background, p.pos, p.pos)
    # for o in objects:
    # screen.blit(background, o.pos, o.pos)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p.move(up=True)
    if keys[pygame.K_DOWN]:
        p.move(down=True)
    if keys[pygame.K_LEFT]:
        p.move(left=True)
    if keys[pygame.K_RIGHT]:
        p.move(right=True)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(p.asset, p.pos)
    # for o in objects:
    # o.move()
    # screen.blit(o.asset, o.pos)
    pygame.display.update()
    clock.tick(60)
