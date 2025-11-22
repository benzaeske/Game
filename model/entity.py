from utils import calculate_unit_vector
from abc import ABC, abstractmethod


class Entity(ABC):
    """The most basic unit for representing an entity in the game.

     Contains positional information in the form of a basic rectangular hitbox. Currently represented as a pygame.rect

    Contains a surface that represents the entity as it will be drawn on the screen. Currently represented by a pygame.Surface that fills the entity's rect hitbox
    """

    def __init__(self, rect, surface, speed):
        self.rect = rect
        self.surface = surface
        self.speed = speed

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self.surface

    def set_position(self, x, y):
        """Updates the bottom left position of the entity's rectangular hitbox"""
        self.rect.left = x
        self.rect.bottom = y

    def move(self, x: int, y: int):
        """Moves the entity's bottom left position by the amount specified by the inputs.
        Inputs are automatically rounded to the nearest integer"""
        self.rect.left = self.rect.left + int(round(x))
        self.rect.bottom = self.rect.bottom - int(round(y))

    def move_with_unit_vector(self, vec_x: int, vec_y: int, dt: float):
        """Moves this entity in the direction of the unit vector calculated by the input vector x and y.
        Moves with magnitude equal to this entity's speed multiplied by input delta time
        """
        uv = calculate_unit_vector(vec_x, vec_y)
        magnitude = self.speed * dt
        movement_vec = uv * magnitude
        self.move(movement_vec[0], movement_vec[1])

    @abstractmethod
    def draw(self, screen):
        """Draws this entity on the screen"""
        pass
