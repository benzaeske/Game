import time

import pygame

from model.gridspace import GridSpace

pygame.init()
DISPLAY_INFO = pygame.display.Info()
DISPLAY_W, DISPLAY_H = (DISPLAY_INFO.current_w, DISPLAY_INFO.current_h)
print(DISPLAY_W, DISPLAY_H)

now = time.time()
grid_space = GridSpace(DISPLAY_W, DISPLAY_H, 4)


space = grid_space.space


x = 200
y = 500

print(grid_space.get_force_vector_at_position(x, y))


for row in space:
    vec_list = []
    for grid_square in row:
        vec_list.append(grid_square.get_force_vector())
    print(vec_list)
