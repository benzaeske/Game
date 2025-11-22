import sys
import time

import pygame

from model.shapes import Square


class Game:
    """Basic representation of a game. Defines a pygame setup and game loop"""

    def __init__(self):
        """Initialize a new game with display set to full screen and 60 FPS"""
        pygame.init()
        self.DISPLAY_INFO = pygame.display.Info()
        self.DISPLAY_W, self.DISPLAY_H = (
            self.DISPLAY_INFO.current_w,
            self.DISPLAY_INFO.current_h,
        )
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.background = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.background.fill(self.BACKGROUND_COLOR)
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.prev_frame_start = time.time()
        self.dt = 0
        # Initialize a player at the middle
        self.player = Square(50, (0, 102, 0))
        self.player.set_position(self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        # Initialize entities to draw
        self.entities = [self.player]

    def add_entity(self, entity):
        self.entities.append(entity)

    @staticmethod
    def check_for_terminate():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()

    def fill_background(self):
        """Fills the whole screen by re drawing the entire background"""
        self.background.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))

    def draw_background(self):
        """Re-draws the background but only over the list of entities on screen"""
        for entity in self.entities:
            self.screen.blit(self.background, entity.get_rect())

    def update_player(self):
        keys = pygame.key.get_pressed()
        self.player.move_with_unit_vector(
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
            keys[pygame.K_UP] - keys[pygame.K_DOWN],
            self.dt,
        )

    def draw_entities(self):
        for entity in self.entities:
            self.screen.blit(entity.get_surface(), entity.get_rect())

    def run(self):
        """Run the game loop"""
        self.fill_background()
        while True:
            self.clock.tick(self.FPS)

            # Calculate delta time
            now = time.time()
            self.dt = now - self.prev_frame_start
            self.prev_frame_start = now

            self.check_for_terminate()

            # Update game by a single frame
            self.draw_background()
            self.update_player()
            self.draw_entities()
            pygame.display.update()
