import time

import pygame

from model.gridspace import GridSpace, GridSquare

pygame.init()
DISPLAY_INFO = pygame.display.Info()
DISPLAY_W, DISPLAY_H = (DISPLAY_INFO.current_w, DISPLAY_INFO.current_h)

now = time.time()
grid_space = GridSpace(DISPLAY_W, DISPLAY_H, 4)
print(time.time() - now)


space = grid_space.space

for row in space:
    vec_list = []
    for grid_square in row:
        if isinstance(grid_square, GridSquare):
            vec_list.append(grid_square.get_force_vector())
    print(vec_list)
