import pygame

from model.entity import Entity


class Square(Entity):
    """Initializes a square Entity with edge size and color"""

    def __init__(self, size, color, mass):
        self._size = size
        self._color = color
        super().__init__(
            pygame.Rect(0, 0, self._size, self._size),
            pygame.Surface((self._size, self._size)),
            mass,
        )
        self._surface.fill(self._color)

    def set_size(self, size):
        self._rect.width = size
        self._rect.height = size

    def set_color(self, color):
        self._color = color
        self._surface.fill(self._color)

    def draw(self, screen):
        screen.blit(self._surface, self._rect)
