import sys

import pygame

pygame.init()
DISPLAY_INFO = pygame.display.Info()
DISPLAY_W, DISPLAY_H = (DISPLAY_INFO.current_w, DISPLAY_INFO.current_h)
BACKGROUND_COLOR = (255, 255, 255)
GREEN = (0, 255, 0)

grid_space_size = DISPLAY_W if DISPLAY_W < DISPLAY_H else DISPLAY_H
screen = pygame.display.set_mode(
    (grid_space_size, grid_space_size), pygame.FULLSCREEN | pygame.SCALED
)
screen.fill(BACKGROUND_COLOR)
background = pygame.Surface((grid_space_size, grid_space_size))
background.fill(GREEN)
screen.blit(background, (10, 10))
print(screen.get_size())
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        sys.exit()
