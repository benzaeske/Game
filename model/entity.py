from abc import ABC, abstractmethod

from numpy.typing import NDArray


class Entity(ABC):
    """The most basic unit for representing an entity in the game.

     Contains positional information in the form of a basic rectangular hitbox. Currently represented as a pygame.rect

    Contains a surface that represents the entity as it will be drawn on the screen. Currently represented by a pygame.Surface that fills the entity's rect hitbox
    """

    def __init__(self, rect, surface, mass):
        self._rect = rect
        self._surface = surface
        self._mass = mass

    def get_rect(self):
        return self._rect

    def get_surface(self):
        return self._surface

    def set_position(self, x, y):
        """Updates the bottom left position of the entity's rectangular hitbox"""
        self._rect.left = x
        self._rect.bottom = y

    def move(self, x: int, y: int):
        """Moves the entity's bottom left position by the amount specified by the inputs.
        Inputs are automatically rounded to the nearest integer"""
        self._rect.left = self._rect.left + int(round(x))
        self._rect.bottom = self._rect.bottom + int(round(y))

    def move_with_unit_vector(self, vector: NDArray[float], dt: float):
        magnitude = self._mass * dt
        self.move(vector[0] * magnitude, vector[1] * magnitude)

    @abstractmethod
    def draw(self, screen):
        """Draws this entity on the screen"""
        pass
