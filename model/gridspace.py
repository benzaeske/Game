import math

from numpy.typing import NDArray

from utils import calculate_unit_vector


class GridSpace:
    def __init__(self, screen_w, screen_h, fractal_size):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.fractal_size = fractal_size
        # the size of the grid space's outer edges
        self.grid_space_edge_size = (
            self.screen_w if self.screen_w < self.screen_h else self.screen_h
        )
        self.screen_center_x = self.grid_space_edge_size / 2
        self.screen_center_y = self.grid_space_edge_size / 2
        # the number of grid squares along the outside edge of the grid space
        self.grid_square_edge_count = int(math.pow(2, self.fractal_size))
        # the edge size of each individual grid square in pixels
        self.grid_square_edge_size = (
            self.grid_space_edge_size / self.grid_square_edge_count
        )
        self.space = [[] for _ in range(self.grid_square_edge_count)]
        self._initialize_grid_space()

    def _initialize_grid_space(self):
        for x in range(self.grid_square_edge_count):
            for y in range(self.grid_square_edge_count):
                self.space[x].append(
                    GridSquare(x, y, self._calculate_force_vector(x, y))
                )

    def _calculate_force_vector(self, x, y) -> NDArray[float]:
        grid_square_center_x = (x * self.grid_square_edge_size) + (
            self.grid_square_edge_size / 2
        )
        grid_square_center_y = (y * self.grid_square_edge_size) + (
            self.grid_square_edge_size / 2
        )
        return calculate_unit_vector(
            self.screen_center_x - grid_square_center_x,
            self.screen_center_y - grid_square_center_y,
        )

    def get_force_vector_at_position(self, x, y):
        i = int(x // self.grid_square_edge_size)
        j = int(y // self.grid_square_edge_size)
        if i < 0:
            i = 0
        if j < 0:
            j = 0
        if i >= self.grid_square_edge_count:
            i = self.grid_square_edge_count - 1
        if j >= self.grid_square_edge_count:
            j = self.grid_square_edge_count - 1
        return self.space[i][j].get_force_vector()


class GridSquare:
    def __init__(self, i, j, force_vector):
        self._i = i
        self._j = j
        self._force_vector = force_vector
        self._entities = []

    def get_force_vector(self):
        return self._force_vector

    def get_entities(self):
        return self._entities

    def add_entity(self, entity):
        self._entities.append(entity)
