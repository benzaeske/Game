import random
from typing import Tuple

import pygame
from pygame import Vector2, Surface

from model.entities.gameentity import GameEntity
from model.utils.vectorutils import limit_magnitude


class FlockingParameters:
    """
    Parameters for controlling how an entity behaves with its flock
    """

    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        cohere_k: float,
        avoid_k: float,
        align_k: float,
    ) -> None:
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k


class Boid(GameEntity):
    def __init__(
        self,
        flocking_parameters: FlockingParameters,
        surface: Surface,
        width: float,
        height: float,
        start_pos: Vector2,
        start_v: Vector2,
        max_speed: float,
        max_force: float,
    ) -> None:
        self.cohere_distance: float = flocking_parameters.cohere_distance
        self.avoid_distance: float = flocking_parameters.avoid_distance
        self.cohere_k: float = flocking_parameters.cohere_k
        self.avoid_k: float = flocking_parameters.avoid_k
        self.align_k: float = flocking_parameters.align_k
        super().__init__(
            surface, width, height, start_pos, start_v, max_speed, max_force
        )

    def apply_forces(self, entities: list[GameEntity]) -> None:
        self.apply_flocking_forces(entities)

    def apply_flocking_forces(self, others: list[GameEntity]) -> None:
        """
        Updates this entity according to the three rules of Boid's algorithm.\n
        #. Each entity moves away from other entities that are within its avoidance range.\n
        #. Each entity aligns its velocity with other entities in its coherence range.\n
        #. Each entity moves towards the average position of other entities in its coherence range.\n
        :param others: Other boid entities that forces on this entity will be calculated with
        """
        sum_separate: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for other in others:
            d: float = self.position.distance_to(other.position)
            if (d > 0) and d < self.cohere_distance:
                sum_align += other.velocity
                sum_cohere += other.position
                count_n += 1
            if (d > 0) and (d < self.avoid_distance):
                diff: Vector2 = self.position - other.position
                diff.normalize_ip()
                diff /= d
                sum_separate += diff
                count_s += 1
        if count_s > 0:
            self.target(sum_separate, self.avoid_k)
        if count_n > 0:
            self.target(sum_align, self.align_k)
            sum_cohere /= float(count_n)
            sum_cohere -= self.position
            self.target(sum_cohere, self.cohere_k)


class BoidFactory:
    """
    Creates Boids with the specified settings
    :param position_x_range: A tuple specifying the range of x coordinates that a random boid can be created at
    :param position_y_range: A tuple specifying the range of y coordinates that a random boid can be created at
    """

    def __init__(
        self,
        parameters: FlockingParameters,
        width: float,
        height: float,
        max_speed: float,
        max_force: float,
        position_x_range: Tuple[float, float],
        position_y_range: Tuple[float, float],
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.parameters: FlockingParameters = parameters
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_force: float = max_force
        self.position_x_range: Tuple[float, float] = position_x_range
        self.position_y_range: Tuple[float, float] = position_y_range
        self.color: Tuple[int, int, int] = color

    def create_random_boid(self) -> Boid:
        """
        Creates a Boid at a random position using settings from this factory. The boid has a random starting velocity that is limited by its max speed.
        """
        surface: Surface = pygame.Surface((self.width, self.height))
        surface.fill(self.color)
        start_velocity: Vector2 = Vector2(
            random.uniform(-self.max_speed, self.max_speed),
            random.uniform(-self.max_speed, self.max_speed),
        )
        limit_magnitude(start_velocity, self.max_speed)
        return Boid(
            self.parameters,
            surface,
            self.width,
            self.height,
            Vector2(
                random.uniform(self.position_x_range[0], self.position_x_range[1]),
                random.uniform(self.position_y_range[0], self.position_y_range[1]),
            ),
            start_velocity,
            self.max_speed,
            self.max_force,
        )
