from typing import Tuple

import pygame
from pygame import Surface

from model.entities.gameentity import GameEntity


class GridCell:
    def __init__(
        self,
        size: float,
        row: int,
        col: int,
        camera_height: float,
        background_surface: Surface = None,
    ):
        self.size: float = size
        self.entities: list[GameEntity] = []
        if background_surface is None:
            self.background_surface: Surface = pygame.Surface((size, size))
            self.background_surface.fill((0, 0, 0))
        else:
            self.background_surface: Surface = background_surface
        # Background position adjusted to be drawn on the view
        self.background_draw_pos: Tuple[float, float] = col * size, camera_height - (
            (row + 1) * size
        )
