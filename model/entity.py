import numpy


class Entity:
    """The most basic unit for representing an entity in the game.

     Contains positional information in the form of a basic rectangular hitbox. Currently represented as a pygame.rect

    Contains a surface that represents the entity as it will appear on the screen. Currently represented by a pygame.Surface
    """

    def __init__(self, rect, surface):
        self.rect = rect
        self.surface = surface
        self.speed = 500

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self.surface

    def set_position(self, x, y):
        """Updates the bottom left position of the entity's rectangular hitbox"""
        self.rect.left = x
        self.rect.bottom = y

    def move(self, x, y):
        self.rect.left = self.rect.left + x
        self.rect.bottom = self.rect.bottom - y

    def move_with_vector(self, vector, dt):
        """Moves this entity according to the angle calculated by the input vector: (x, y).
        The distance moved is calculated with this object's speed and the input delta time
        """
        angle = numpy.arctan2(vector[1], vector[0])
        x_diff = round(numpy.cos(angle), 10) * self.speed * dt * abs(vector[0])
        y_diff = round(numpy.sin(angle), 10) * self.speed * dt * abs(vector[1])
        self.move(x_diff, y_diff)
