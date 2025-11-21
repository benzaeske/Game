import pygame

from model.entity import Entity


class Square(Entity):
    """Initializes a square Entity with edge size and color"""

    def __init__(self, size, color):
        self.size = size
        self.color = color
        super().__init__(
            pygame.Rect(0, 0, self.size, self.size),
            pygame.Surface((self.size, self.size)),
        )
        self.surface.fill(self.color)

    def set_size(self, size):
        self.rect.width = size
        self.rect.height = size

    def set_color(self, color):
        self.color = color
        self.surface.fill(self.color)
