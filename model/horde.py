from random import randint

from model.shapes import Square


class Horde:

    def __init__(self, size, screen_w, screen_h):
        self.size = size
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.speed = 100

    def spawn_entities(self):
        entities = []
        enemy_size = 30
        # Spawn an enemy on each side of the map based on the size of the horde
        for x in range(0, self.size):
            enemy_top = Square(enemy_size, (200, 0, 0), self.speed)
            enemy_top.set_position(randint(0, self.screen_w - enemy_size), enemy_size)
            entities.append(enemy_top)
            enemy_bot = Square(enemy_size, (200, 0, 0), self.speed)
            enemy_bot.set_position(
                randint(0, self.screen_w - enemy_size), self.screen_h
            )
            entities.append(enemy_bot)
            enemy_left = Square(enemy_size, (200, 0, 0), self.speed)
            enemy_left.set_position(0, randint(enemy_size, self.screen_h))
            entities.append(enemy_left)
            enemy_right = Square(enemy_size, (200, 0, 0), self.speed)
            enemy_right.set_position(
                self.screen_w - enemy_size, randint(enemy_size, self.screen_h)
            )
            entities.append(enemy_right)
        return entities
