class Entity:
    """The most basic unit for representing an entity in the game.

     Contains positional information in the form of a basic rectangular hitbox. Currently represented as a pygame.rect

    Contains a surface that represents the entity as it will appear on the screen. Currently represented by a pygame.Surface
    """

    def __init__(self, rect, surface):
        self.rect = rect
        self.surface = surface

    def get_rect(self):
        return self.rect

    def get_surface(self):
        return self.surface

    def set_position(self, x, y):
        """Updates the bottom left position of the entity's rectangular hitbox"""
        self.rect.left = x
        self.rect.bottom = y
