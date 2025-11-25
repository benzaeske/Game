import sys
import time

import pygame
from pygame.time import Clock

from model.model import Model, GameEntity
from view.view import View


class GameController:
    def __init__(self, fps: int = 60) -> None:
        pygame.init()
        self.view: View = View()
        self.model: Model = Model(self.view.screen_width, self.view.screen_height)
        self.clock: Clock = pygame.time.Clock()
        self.fps: int = fps
        self.game_start: float = -1
        self.dt: float = 0.0
        # Used to trigger logging when dt exceeds the max value required for 60fps
        self.max_dt: float = 0.017

    def start_game(self):
        self.game_start = time.time()
        # Loop frames
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self.check_for_terminate()
        model_update_time = time.time()
        self.update_model()
        model_update_time = time.time() - model_update_time
        view_update_time = time.time()
        self.draw_background()
        self.draw_game_entities()
        view_update_time = time.time() - view_update_time
        self.view.update_screen()
        self.dt = self.clock.tick(self.fps) / 1000
        # Print info when dt indicates we dropped below 60 fps
        self.fps_logging(model_update_time, view_update_time)

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
        self.model.update_model(self.dt)

    def draw_background(self) -> None:
        self.view.draw_background()
        self.view.print_fps(self.clock.get_fps())

    def draw_game_entities(self) -> None:
        for entity in self.model.entities:
            self.view.draw_surface(entity.surface, entity.get_display_adjusted_pos())

    def add_game_entity(self, entity: GameEntity) -> None:
        self.model.entities.append(entity)
