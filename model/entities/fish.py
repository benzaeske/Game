import random
from enum import Enum
from typing import Tuple
from uuid import UUID

import pygame
from pygame import Vector2, Surface

from model.entities.gameentity import GameEntity
from model.entities.school import SchoolingParameters
from model.utils.vectorutils import limit_magnitude


class FishType(Enum):
    RED = 0
    GREEN = 1
    YELLOW = 2


class FishOptions:
    def __init__(
        self,
        fish_type: FishType,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        initial_position: Vector2 = Vector2(0.0, 0.0),
        initial_velocity: Vector2 = Vector2(0.0, 0.0),
        cell_interaction_range: int = 1,
    ) -> None:
        self.fish_type: FishType = fish_type
        self.width: float = width
        self.height: float = height
        self.max_speed: float = max_speed
        self.max_acceleration: float = max_acceleration
        self.initial_position: Vector2 = initial_position
        self.initial_velocity: Vector2 = initial_velocity
        self.cell_interaction_range: int = cell_interaction_range


class Fish(GameEntity):
    def __init__(
        self,
        fish_options: FishOptions,
        school_id: UUID,
        fish_sprite: Surface,
    ) -> None:
        self.fish_options: FishOptions = fish_options
        self.school_id: UUID = school_id
        self.fish_sprite: Surface = fish_sprite
        super().__init__(
            fish_sprite,
            school_id,
            fish_options.width,
            fish_options.height,
            fish_options.initial_position,
            fish_options.initial_velocity,
            fish_options.max_speed,
            fish_options.max_acceleration,
            fish_options.cell_interaction_range,
        )

    def apply_forces(self, entities: list[GameEntity]) -> None:
        self.apply_schooling_forces(entities)
        if self.target_location is not None:
            self.school_to_target_location(self.target_location)

    def apply_schooling_forces(self, others: list[GameEntity]) -> None:
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
            if self.group_id == other.group_id:
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

    def school_to_target_location(self, target_location: Vector2) -> None:
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
        parameters: SchoolingParameters,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        position_x_range: Tuple[float, float],
        position_y_range: Tuple[float, float],
        interaction_range: int = 1,
        surface: Surface = None,
    ) -> None:
        self.parameters: SchoolingParameters = parameters
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

    def create_random_boid(self) -> Fish:
        """
        Creates a Boid at a random position using settings from this factory. The boid has a random starting velocity that is limited by its max speed.
        """
        start_velocity: Vector2 = Vector2(
            random.uniform(-self.max_speed, self.max_speed),
            random.uniform(-self.max_speed, self.max_speed),
        )
        limit_magnitude(start_velocity, self.max_speed)
        return Fish(
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


class FishFactory(BoidFactory):

    def __init__(
        self,
        fish_type: FishType,
        parameters: SchoolingParameters,
        width: float,
        height: float,
        max_speed: float,
        max_acceleration: float,
        position_x_range: Tuple[float, float],
        position_y_range: Tuple[float, float],
        interaction_range: int = 1,
    ) -> None:
        surface: Surface | None = None
        if fish_type == FishType.RED:
            surface: Surface = pygame.image.load("images/red_fish.png").convert_alpha()
        elif fish_type == FishType.GREEN:
            surface: Surface = pygame.image.load(
                "images/green_fish.png"
            ).convert_alpha()
        elif fish_type == FishType.YELLOW:
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
