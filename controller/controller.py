import sys
import time
from typing import Tuple

import pygame
from pygame import Vector2
from pygame.key import ScancodeWrapper
from pygame.time import Clock

from model.entities.player import Turtle
from model.model import GameEntity
from model.spatial_partitioning_model import SpatialPartitioningModel
from view.view import View


class ControllerOptions:
    """
    :param world_width: The size of the world model. This must be divisible by the grid cell size
    :param world_height: The size of the world model. This must be divisible by the grid cell size
    :param grid_cell_size: The map will be divided into grids of this size. In order for flocking to work, must be at least as large as the smallest coherence radius of the boids being used
    """

    def __init__(
        self,
        world_width: float,
        world_height: float,
        grid_cell_size: float,
        background_color: Tuple[int, int, int],
    ) -> None:
        self.world_width: float = world_width
        self.world_height: float = world_height
        self.grid_cell_size: float = grid_cell_size
        self.background_color: Tuple[int, int, int] = background_color


class GameController:
    """
    Orchestration class for running the current state of the game. Contains a model which is the simulated world and a view that is responsible for drawing on the screen.
    In the current implementation, the simulated world and the screen size are the same, but eventually the screen will only be displaying part of a larger simulation.
    """

    def __init__(
        self,
        options: ControllerOptions,
    ) -> None:
        pygame.init()
        self.view: View = View(
            options.background_color,
        )
        self.model: SpatialPartitioningModel = SpatialPartitioningModel(
            options.world_width,
            options.world_height,
            options.grid_cell_size,
            Turtle(
                self.view.screen_width,
                self.view.screen_height,
                (options.world_width, options.world_height),
            ),
        )
        self.clock: Clock = pygame.time.Clock()
        self.fps: int = 60
        self.game_start: float = -1
        self.dt: float = 0.0
        # Used to trigger logging when dt exceeds the max value required for 60fps
        self.max_dt: float = 0.017
        # Tracking player inputs
        self.mouse_pos: Tuple[int, int] = (0, 0)
        self.key_presses: ScancodeWrapper = ScancodeWrapper(())

    def start_game(self):
        self.game_start = time.time()
        # Loop frames
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self.key_presses = pygame.key.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.check_for_terminate()
        model_update_time = time.time()
        self.update_model()
        model_update_time = time.time() - model_update_time
        view_update_time = time.time()
        self.draw_background()
        self.draw_game_entities()
        self.view.update_screen()
        view_update_time = time.time() - view_update_time
        self.fps_logging(model_update_time, view_update_time)
        self.dt = self.clock.tick(self.fps) / 1000

    def check_for_terminate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if self.key_presses[pygame.K_ESCAPE]:
            sys.exit()

    def update_model(self) -> None:
        self.model.update_model(self.dt, Vector2(self.mouse_pos), self.key_presses)

    def draw_background(self) -> None:
        self.view.draw_background()
        self.view.print_fps(self.clock.get_fps())

    def draw_game_entities(self) -> None:
        for entity in self.model.get_entities_in_camera_range():
            self.view.draw_surface(
                entity.surface,
                entity.get_camera_adjusted_position(
                    self.model.player.position,
                    self.model.player.camera_width,
                    self.model.player.camera_height,
                ),
            )
        self.view.draw_surface(
            self.model.player.surface, self.model.player.get_camera_adjusted_position()
        )

    def add_game_entity(self, entity: GameEntity) -> None:
        self.model.add_game_entity(entity)

    def fps_logging(self, model_t: float, view_t: float) -> None:
        if self.dt > self.max_dt:
            print(
                "Frame dt was too slow to meet",
                self.fps,
                "fps. dt:",
                self.dt,
                "\nModel update time ms:",
                model_t,
                "\nView update time ms:",
                view_t,
                "\n",
            )
