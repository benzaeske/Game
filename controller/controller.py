import sys
import time
from typing import Tuple

import pygame
from pygame import Vector2
from pygame.time import Clock

from model.model import GameEntity
from model.spatial_partitioning_model import SpatialPartitioningModel
from view.view import View


class GameController:
    """
    Orchestration class for running the current state of the game. Contains a model which is the simulated world and a view that is responsible for drawing on the screen.
    In the current implementation, the simulated world and the screen size are the same, but eventually the screen will only be displaying part of a larger simulation.
    :param world_width: The size of the world model. This must be divisible by the grid cell size
    :param world_height: The size of the world model. This must be divisible by the grid cell size
    :param grid_cell_size: The map will be divided into grids of this size. In order for flocking to work, must be at least as large as the smallest coherence radius of the boids being used
    """

    def __init__(
        self,
        world_width: float = 1000.0,
        world_height: float = 600.0,
        grid_cell_size: float = 100.0,
        fps: int = 60,
    ) -> None:
        pygame.init()
        self.view: View = View()
        self.model: SpatialPartitioningModel = SpatialPartitioningModel(
            world_width, world_height, grid_cell_size
        )
        self.clock: Clock = pygame.time.Clock()
        self.fps: int = fps
        self.game_start: float = -1
        self.dt: float = 0.0
        # Used to trigger logging when dt exceeds the max value required for 60fps
        self.max_dt: float = 0.017
        # Tracking mouse pos in case I want it for input
        self.mouse_pos: Tuple[int, int] = (0, 0)

    def start_game(self):
        self.game_start = time.time()
        # Loop frames
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self.check_for_terminate()
        self.mouse_pos = pygame.mouse.get_pos()
        model_update_time = time.time()
        self.update_model()
        model_update_time = time.time() - model_update_time
        view_update_time = time.time()
        self.draw_background()
        self.draw_game_entities()
        view_update_time = time.time() - view_update_time
        self.view.update_screen()
        self.dt = self.clock.tick(self.fps) / 1000

    @staticmethod
    def check_for_terminate():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

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

    def update_model(self) -> None:
        self.model.update_model(self.dt, Vector2(self.mouse_pos))

    def draw_background(self) -> None:
        self.view.draw_background()
        # Display FPS in top left
        self.view.print_fps(self.clock.get_fps())

    def draw_game_entities(self) -> None:
        for row in range(self.model.grid_height):
            for col in range(self.model.grid_width):
                for entity in self.model.grid_space[row][col]:
                    self.view.draw_surface(
                        entity.surface, entity.get_display_adjusted_pos()
                    )

    def add_game_entity(self, entity: GameEntity) -> None:
        self.model.add_game_entity(entity)
