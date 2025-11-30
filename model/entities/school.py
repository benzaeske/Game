import copy
import uuid
from uuid import UUID

import pygame.image
from pygame import Vector2, Surface

from model.entities.fish import FishOptions, Fish, FishType
from model.utils.vectorutils import limit_magnitude


class SchoolingParameters:
    def __init__(
        self,
        cohere_distance: float,
        avoid_distance: float,
        interaction_cell_radius: int = 1,
        cohere_k: float = 1.0,
        avoid_k: float = 1.8,
        align_k: float = 1.0,
    ) -> None:
        self.cohere_distance: float = cohere_distance
        self.avoid_distance: float = avoid_distance
        self.interaction_cell_radius: int = interaction_cell_radius
        self.cohere_k: float = cohere_k
        self.avoid_k: float = avoid_k
        self.align_k: float = align_k


class ShoalingParameters:

    def __init__(
        self,
        shoal_location: Vector2 | None = None,
        shoal_k: float = 1.0,
        shoal_radius: int = 1,
        spawn_radius: int = 1,
        spawn_amount: int = 32,
    ):
        self.shoal_location: Vector2 | None = shoal_location
        self.shoal_k: float = shoal_k
        self.shoal_radius: int = shoal_radius
        self.spawn_radius: int = spawn_radius
        self.spawn_amount: int = spawn_amount


class School:
    def __init__(
        self,
        schooling_params: SchoolingParameters,
        shoaling_params: ShoalingParameters,
        fish_settings: FishOptions,
    ) -> None:
        self.school_id: UUID = uuid.uuid4()
        self.schooling_params: SchoolingParameters = schooling_params
        self.shoaling_params: ShoalingParameters = shoaling_params
        self.fish_settings: FishOptions = fish_settings
        self.fish_surface = self.load_fish_surface()

    def load_fish_surface(self) -> Surface:
        match self.fish_settings.fish_type:
            case FishType.RED:
                surface = pygame.image.load("images/red_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishType.GREEN:
                surface = pygame.image.load("images/green_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )
            case FishType.YELLOW:
                surface = pygame.image.load("images/yellow_fish.png").convert_alpha()
                return pygame.transform.scale(
                    surface, (self.fish_settings.width, self.fish_settings.height)
                )

    def hatch_fish(self) -> Fish:
        fish_options: FishOptions = copy.copy(self.fish_settings)
        fish_options.initial_position = Vector2(
            0.0, 0.0
        )  # TODO random location in spawn radius
        fish_options.initial_velocity = Vector2(
            self.fish_settings.max_speed, self.fish_settings.max_speed
        )
        limit_magnitude(fish_options.initial_velocity, self.fish_settings.max_speed)
        return Fish(
            fish_options,
            self.school_id,
            self.fish_surface,
        )
