import random
from enum import Enum
from typing import Tuple

import pygame
from pygame import Vector2, Surface

from model.entities.gameentity import GameEntity
from model.utils.vectorutils import limit_magnitude


class FlockingParameters:
    """
    Parameters for controlling how an entity behaves with its flock
    :param cohere_distance: The maximum distance at which boids will try to cohere with their 'friends'
    :param avoid_distance: The maximum distance at which boids will try to avoid their neighbors
    :param cohere_k: A constant that represents how much a boid will prioritize cohering with friends
    :param align_k: A constant that represents how much a boid will prioritize aligning with friends
    :param flock_id: Unique identifier for a flock. Currently not used, but will be used to have multiple flocks that don't cohere to each other
    :param target_mouse: Whether the flock will move towards the mouse - temporary for testing
    :param target_k: How much the boids will prioritize moving towards their 'target' (currently just the mouse) - temporary for testing
    """

    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        cohere_k: float = 1.0,
        avoid_k: float = 1.5,
        align_k: float = 1.0,
        flock_id: int = -1,
        target_location: Vector2 | None = None,
        target_k: float = 1.0,
    ) -> None:
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k
        self.flock_id: int = flock_id
        self.target_location: Vector2 | None = target_location
        self.target_k: float = target_k


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
        max_acceleration: float,
        interaction_range: int = 1,
    ) -> None:
        self.cohere_distance: float = flocking_parameters.cohere_distance
        self.avoid_distance: float = flocking_parameters.avoid_distance
        self.cohere_k: float = flocking_parameters.cohere_k
        self.avoid_k: float = flocking_parameters.avoid_k
        self.align_k: float = flocking_parameters.align_k
        self.target_location: Vector2 | None = flocking_parameters.target_location
        self.target_k: float = flocking_parameters.target_k
        super().__init__(
            surface,
            width,
            height,
            start_pos,
            start_v,
            max_speed,
            max_acceleration,
            flocking_parameters.flock_id,
            interaction_range,
        )

    def apply_forces(self, entities: list[GameEntity], mouse_pos: Vector2) -> None:
        self.apply_flocking_forces(entities)
        if self.target_location is not None:
            self.flock_to_target_location(self.target_location)

    def apply_flocking_forces(self, others: list[GameEntity]) -> None:
        """
        Updates this entity according to the three rules of Boid's algorithm.\n
        #. Each entity moves away from other entities that are within its avoidance range.\n
        #. Each entity aligns its velocity with other entities in its coherence range.\n
        #. Each entity moves towards the average position of other entities in its coherence range.\n
        :param others: Other boid entities that forces on this entity will be calculated with
        """
        sum_avoid: Vector2 = Vector2(0.0, 0.0)
        sum_align: Vector2 = Vector2(0.0, 0.0)
        sum_cohere: Vector2 = Vector2(0.0, 0.0)
        count_n: int = 0
        count_s: int = 0
        for other in others:
            if self.group_id > 0 and self.group_id == other.group_id:
                # TODO add check to make sure not to check this entity against itself
                d: float = self.position.distance_to(other.position)
                if (d > 0) and d < self.cohere_distance:
                    sum_align += other.velocity
                    sum_cohere += other.position
                    count_n += 1
                if (d > 0) and (d < self.avoid_distance):
                    diff: Vector2 = self.position - other.position
                    diff.normalize_ip()
                    diff /= d
                    sum_avoid += diff
                    count_s += 1
        if count_s > 0:
            self.target(sum_avoid, self.avoid_k)
        if count_n > 0:
            self.target(sum_align, self.align_k)
            sum_cohere /= float(count_n)
            sum_cohere -= self.position
            self.target(sum_cohere, self.cohere_k)

    def flock_to_target_location(self, target_location: Vector2) -> None:
        diff = target_location - self.position
        d = self.position.distance_to(target_location)
        if d > (self.cohere_distance * 2):
            self.target(diff, self.target_k)
        else:
            self.target(diff, -1 * self.target_k)


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
        max_acceleration: float,
        position_x_range: Tuple[float, float],
        position_y_range: Tuple[float, float],
        interaction_range: int = 1,
        surface: Surface = None,
    ) -> None:
        self.parameters: FlockingParameters = parameters
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.position_x_range: Tuple[float, float] = position_x_range
        self.position_y_range: Tuple[float, float] = position_y_range
        self.interaction_range: int = interaction_range
        if surface is None:
            self.surface: Surface = pygame.Surface((self.width, self.height))
            self.surface.fill((255, 255, 255))
        else:
            self.surface = surface

    def create_random_boid(self) -> Boid:
        """
        Creates a Boid at a random position using settings from this factory. The boid has a random starting velocity that is limited by its max speed.
        """
        start_velocity: Vector2 = Vector2(
            random.uniform(-self.max_speed, self.max_speed),
            random.uniform(-self.max_speed, self.max_speed),
        )
        limit_magnitude(start_velocity, self.max_speed)
        return Boid(
            self.parameters,
            self.surface,
            self.width,
            self.height,
            Vector2(
                random.uniform(self.position_x_range[0], self.position_x_range[1]),
                random.uniform(self.position_y_range[0], self.position_y_range[1]),
            ),
            start_velocity,
            self.max_speed,
            self.max_acceleration,
            self.interaction_range,
        )


class FishTypes(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2


class FishFactory(BoidFactory):

    def __init__(
        self,
        fish_type: FishTypes,
        parameters: FlockingParameters,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        position_x_range: Tuple[float, float],
        position_y_range: Tuple[float, float],
        interaction_range: int = 1,
    ) -> None:
        surface: Surface | None = None
        if fish_type == FishTypes.RED:
            surface: Surface = pygame.image.load("images/red_fish.png").convert_alpha()
        elif fish_type == FishTypes.GREEN:
            surface: Surface = pygame.image.load(
                "images/green_fish.png"
            ).convert_alpha()
        elif fish_type == FishTypes.YELLOW:
            surface: Surface = pygame.image.load(
                "images/yellow_fish.png"
            ).convert_alpha()
        surface = pygame.transform.scale(surface, (width, height))
        super().__init__(
            parameters,
            width,
            height,
            max_speed,
            max_acceleration,
            position_x_range,
            position_y_range,
            interaction_range,
            surface,
        )
