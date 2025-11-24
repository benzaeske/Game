import random
from typing import Tuple

import pygame
from pygame import Vector2, Rect, Surface

# Flocking settings
neighbor_dist: float = 132.0
separate_dist: float = 66.0
separate_k = 1.8


class Model:
    def __init__(self, screen_width, screen_height):
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.entities: list[GameEntity] = []

        print("Initialized model")

    def update_model(self, dt: float) -> None:
        for entity in self.entities:
            entity.apply_forces(self.entities)
            entity.update_position(self.screen_width, self.screen_height, dt)


class GameEntity:

    def __init__(
        self,
        surface: Surface,
        width: float = 20.0,
        height: float = 20.0,
        start_pos: Vector2 = Vector2(0.0, 0.0),
        start_v: Vector2 = Vector2(0.0, 0.0),
        speed_limit: float = 5.0,
        fixed_acceleration: Vector2 = None,
    ):
        self.surface: Surface = surface
        self.width: float = width
        self.height: float = height
        self.pos_display_adjust: Vector2 = Vector2(self.width / 2, self.height / 2)

        # Physics-related variables:
        self.position: Vector2 = start_pos
        self.velocity: Vector2 = start_v
        self.acceleration: Vector2 = Vector2(0.0, 0.0)
        self.fixed_acceleration: Vector2 = fixed_acceleration
        self.max_speed: float = speed_limit
        self.max_force: float = 0.3

    def update_position(self, screen_w: float, screen_h: float, dt: float) -> None:
        """
        Updates entities for a single frame.\n
        All coordinates are assumed to represent the center of entities and have an inverted y-axis as dictated by pygame.
        """
        self.velocity += self.acceleration
        if self.velocity.magnitude() != 0.0:
            self.velocity.clamp_magnitude_ip(self.max_speed)
        self.position += self.velocity * dt
        self.position.x = (self.position.x + screen_w) % screen_w
        self.position.y = (self.position.y + screen_h) % screen_h
        self.acceleration *= 0.0
        if self.velocity.magnitude() >= self.max_speed:
            print(self.velocity.x, self.velocity.y, self.velocity.magnitude())

    def apply_forces(self, entities: list["GameEntity"]) -> None:
        """
        Calculates this GameEntity's acceleration for the current frame.\n
        Acceleration is removed at the end of each frame and must be continually applied.
        """
        self.calculate_flocking_forces(entities)

    def calculate_flocking_forces(self, flock: list["GameEntity"]) -> None:
        sum_separate: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for other in flock:
            d: float = self.position.distance_to(other.position)
            if (d > 0) and d < neighbor_dist:
                sum_align += other.velocity
                sum_cohere += other.position
                count_n += 1
            if (d > 0) and (d < separate_dist):
                diff: Vector2 = self.position - other.position
                diff.normalize_ip()
                diff /= d
                sum_separate += diff
                count_s += 1
        if count_s > 0:
            self.target(sum_separate, separate_k)

    def target(self, target_dir: Vector2, k: float) -> None:
        target_dir.normalize_ip()
        target_dir *= self.max_speed
        target_dir -= self.velocity
        if target_dir.magnitude() != 0.0:
            target_dir.clamp_magnitude_ip(self.max_force)
        target_dir *= k
        self.acceleration += target_dir

    def get_rect(self) -> Rect:
        """
        Gets a pygame.Rect that has adjusted coordinates for pygame.blit
        """
        # Adjust the position from the middle of the object to the top left corner
        adjusted_pos: Vector2 = self.position - self.pos_display_adjust
        return pygame.Rect(adjusted_pos.x, adjusted_pos.y, self.width, self.height)

    def get_display_adjusted_pos(self) -> Tuple[float, float]:
        """
        Gets a tuple of floats that are ready to use as coordinates for a pygame.blit
        """
        # Adjust the position from the middle of the object to the top left corner
        adjusted_pos: Vector2 = self.position - self.pos_display_adjust
        return adjusted_pos.x, adjusted_pos.y


class RandomSquareAgent(GameEntity):
    """
    A white square with a random starting position and a random starting velocity of magnitude equal to the specified limit
    """

    def __init__(self, size, velocity, screen_w, screen_h):
        self.size = size
        color = (255, 255, 255)
        surface = pygame.Surface((self.size, self.size))
        surface.fill(color)
        starting_velocity = Vector2(
            random.randint(0, int(velocity)),
            random.randint(0, int(velocity)),
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
