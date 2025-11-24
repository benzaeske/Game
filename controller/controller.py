import sys
import time

import pygame
from pygame import Surface
from pygame.time import Clock

from model.model import Model, ModelEntity
from view.view import View, ViewEntity


class GameController:
    def __init__(self, fps: int = 60):
        pygame.init()
        self.view: View = View()
        self.model: Model = Model(self.view.screen_width, self.view.screen_height)
        self.clock: Clock = pygame.time.Clock()
        self.fps = fps
        self.game_start: float = -1

    def start(self):
        self.game_start = time.time()
        # Loop frames
        while True:
            self.check_for_terminate()
            # delta time consumed in the previous frame loop in milliseconds
            dt = self.clock.get_time()
            self.model.update_model(dt)
            self.view.draw_background()
            self.view.update_screen()
            self.clock.tick(self.fps)

    @staticmethod
    def check_for_terminate():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()


class GameEntity:
    def __init__(self, surface: Surface):
        self.entity_model: ModelEntity = ModelEntity()
        self.entity_view: ViewEntity = ViewEntity()
