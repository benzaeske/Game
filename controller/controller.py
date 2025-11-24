import sys
import time

import pygame
from pygame.time import Clock

from model.model import Model, GameEntity
from view.view import View


class GameController:
    def __init__(self, fps: int = 60):
        pygame.init()
        self.view: View = View()
        self.model: Model = Model(self.view.screen_width, self.view.screen_height)
        self.clock: Clock = pygame.time.Clock()
        self.fps = fps
        self.game_start: float = -1
        self.dt = 0

    def start_game(self):
        self.game_start = time.time()
        # Loop frames
        while True:
            self.do_game_loop()

    def do_game_loop(self) -> None:
        self.check_for_terminate()
        self.update_model()
        self.draw_background()
        self.draw_game_entities()
        self.view.update_screen()
        self.dt = self.clock.tick(self.fps) / 1000
        if self.dt > 0.017:  # Print when we drop below 60 fps
            print("dt dropped below 60 fps:", self.dt)

    @staticmethod
    def check_for_terminate():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

    def update_model(self) -> None:
        self.model.update_model(self.dt)

    def draw_background(self) -> None:
        self.view.draw_background()

    def draw_game_entities(self) -> None:
        for entity in self.model.entities:
            self.view.draw_surface(entity.surface, entity.get_display_adjusted_pos())

    def add_game_entity(self, entity: GameEntity) -> None:
        self.model.entities.append(entity)
