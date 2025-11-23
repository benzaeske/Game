from abc import ABC, abstractmethod
from random import randint

from model.entity import Entity
from model.shapes import Square


class EntityGroup(ABC):

    def __init__(self, frequency):
        self._frequency = frequency
        self._time_period = frequency
        self._can_spawn = True

    def tick(self, dt):
        self._time_period += dt
        if self._time_period > self._frequency:
            self._time_period = 0
            self._can_spawn = True
        else:
            self._can_spawn = False

    def can_spawn(self) -> bool:
        return self._can_spawn

    @abstractmethod
    def spawn(self) -> list[Entity]:
        pass


###################################
######### Implementations #########
###################################


class SquareGroup(EntityGroup):
    def __init__(self, magnitude, screen_w, screen_h, color, size, mass, frequency):
        super().__init__(frequency)
        self._magnitude = magnitude
        self._screen_w = screen_w
        self._screen_h = screen_h
        self._color = color
        self._size = size
        self._mass = mass

    def spawn(self) -> list[Entity]:
        entities = []
        # Spawn an enemy on a random position along one of the 4 edges of the screen
        for x in range(0, self._magnitude):
            entity = Square(self._size, self._color, self._mass)
            switch = randint(0, 3)
            match switch:
                case 0:
                    # Top
                    entity.set_position(
                        randint(0, self._screen_w - self._size), self._size
                    )
                case 1:
                    # Bottom
                    entity.set_position(
                        randint(0, self._screen_w - self._size), self._screen_h
                    )
                case 2:
                    # Left
                    entity.set_position(0, randint(self._size, self._screen_h))
                case 3:
                    # Right
                    entity.set_position(
                        self._screen_w - self._size, randint(self._size, self._screen_h)
                    )
            entities.append(entity)
        return entities
