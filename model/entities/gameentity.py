import random
from typing import Tuple

import pygame
from pygame import Surface, Vector2, Rect

from model.utils.vectorutils import limit_magnitude, safe_normalize


class GameEntity:

    def __init__(
        self,
        surface: Surface,
        width: float = 1.0,
        height: float = 1.0,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        start_v: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
        max_force: float = 0.1,
        group_id: int = -1,  # It can be useful for certain flocking behavior to keep track of groups of GameEntities. -1 indicates the GameEntity does not have a group
    ):
        self.surface: Surface = surface
        self.width: float = width
        self.height: float = height
        self.pos_display_adjust: Vector2 = Vector2(self.width / 2, self.height / 2)

        # Physics-related variables:
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_v
        self.acceleration: Vector2 = Vector2(0.0, 0.0)
        self.max_speed: float = max_speed
        self.max_force: float = max_force
        self.group_id: int = group_id

    def apply_forces(self, entities: list["GameEntity"]) -> None:
        """
        Called in the model's update loop for each entity in the simulation.
        By default, GameEntities don't get any forces applied to them. If you want to automatically apply forces to a GameObject in the model's update loop you have to extend the class and override this method.
        :param entities: List of GameObject entities that are within range to interact with this entity when calculated forces on it
        """
        pass

    def update_position(self, screen_w: float, screen_h: float, dt: float) -> None:
        """
        Updates entities for a single frame.\n
        All coordinates are assumed to represent the center of entities and have an inverted y-axis\n
        By default, an entity's acceleration is set back to 0 after its position is updated
        """
        self.velocity += self.acceleration
        limit_magnitude(self.velocity, self.max_speed)
        self.position += self.velocity * dt
        self.position.x = (self.position.x + screen_w) % screen_w
        self.position.y = (self.position.y + screen_h) % screen_h
        self.acceleration *= 0.0

    def target(self, target_dir: Vector2, k: float) -> None:
        """
        Accelerates this entity in the target direction.
        """
        safe_normalize(target_dir)
        target_dir *= self.max_speed
        target_dir -= self.velocity
        limit_magnitude(target_dir, self.max_force)
        target_dir *= k
        self.acceleration += target_dir

    def get_rect(self) -> Rect:
        """
        Gets a pygame.Rect that has adjusted coordinates for pygame.blit
        """
        # Adjust the position from the middle of the object to the top left corner
        adjusted_pos: Vector2 = self.position - self.pos_display_adjust
        return Rect(adjusted_pos.x, adjusted_pos.y, self.width, self.height)

    def get_display_adjusted_pos(self) -> Tuple[float, float]:
        """
        Gets a tuple of floats that are ready to use as coordinates for a pygame.blit
        """
        # Adjust the position from the middle of the object to the top left corner
        adjusted_pos: Vector2 = self.position - self.pos_display_adjust
        return adjusted_pos.x, adjusted_pos.y


class RandomSquareEntity(GameEntity):
    """
    A white square with a random starting position and a random starting velocity of magnitude equal to the specified limit
    """

    def __init__(self, size, velocity, screen_w, screen_h):
        self.size = size
        color = (255, 255, 255)
        surface = pygame.Surface((self.size, self.size))
        surface.fill(color)
        starting_velocity = Vector2(
            random.randint(-int(velocity), int(velocity)),
            random.randint(-int(velocity), int(velocity)),
        )
        if starting_velocity.magnitude() != 0.0:
            starting_velocity.clamp_magnitude_ip(velocity, velocity)
        super().__init__(
            surface,
            self.size,
            self.size,
            Vector2(
                random.randint(int(self.size / 2), screen_w - int(self.size / 2)),
                random.randint(int(self.size / 2), screen_h - int(self.size / 2)),
            ),
            starting_velocity,
            velocity,
        )
