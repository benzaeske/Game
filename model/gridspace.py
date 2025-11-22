import math

from numpy.typing import NDArray

from utils import calculate_unit_vector


class GridSpace:
    def __init__(self, screen_w, screen_h, fractal_size):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen_center_x = screen_w / 2
        self.screen_center_y = screen_h / 2
        self.fractal_size = fractal_size
        # the size of the grid space's outer edges
        self.grid_space_edge_size = (
            self.screen_w if self.screen_w < self.screen_h else self.screen_h
        )
        self.border_x = (self.screen_w - self.grid_space_edge_size) / 2
        self.border_y = (self.screen_h - self.grid_space_edge_size) / 2
        # the number of grid squares along the outside edge of the grid space
        self.grid_square_edge_count = int(math.pow(2, self.fractal_size))
        # the edge size of each individual grid square in pixels
        self.grid_square_edge_size = (
            self.grid_space_edge_size / self.grid_square_edge_count
        )
        self.space = [[] for _ in range(self.grid_square_edge_count)]
        self._initialize_grid_space()

    def _initialize_grid_space(self):
        for i in range(self.grid_square_edge_count):
            for j in range(self.grid_square_edge_count):
                self.space[i].insert(
                    j, GridSquare(i, j, self._calculate_force_vector(j, i))
                )

    def _calculate_force_vector(self, i, j) -> NDArray[float]:
        # All positions calculated based on true screen position
        grid_square_center_x = (
            self.border_x
            + (i * self.grid_square_edge_size)
            + (self.grid_square_edge_size / 2)
        )
        grid_square_center_y = (
            self.border_y
            + (j * self.grid_square_edge_size)
            + (self.grid_square_edge_size / 2)
        )
        return calculate_unit_vector(
            self.screen_center_x - grid_square_center_x,
            self.screen_center_y - grid_square_center_y,
        )


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
