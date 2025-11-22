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
        # Track input vectors
        self.up = self.down = self.left = self.right = 0
        # Initialize a player at the middle
        self.player = Square(50, (0, 102, 0))
        self.player.set_position(self.DISPLAY_W / 2, self.DISPLAY_H / 2)
        # Initialize entities to draw
        self.entities = [self.player]

    def add_entity(self, entity):
        self.entities.append(entity)

    def process_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        self.player.move_with_vector(
            (
                keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
                keys[pygame.K_UP] - keys[pygame.K_DOWN],
            ),
            self.dt,
        )

    def draw_background(self):
        # White background
        self.background.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))

    def draw_entities(self):
        for entity in self.entities:
            self.screen.blit(entity.get_surface(), entity.get_rect())

    def run(self):
        """Run the game loop
        1. looks at keyboard inputs
        2. draws a solid background
        3. draws entities
        4. updates screen and sets FPS"""
        while True:
            self.clock.tick(self.FPS)

            now = time.time()
            self.dt = now - self.prev_frame_start
            self.prev_frame_start = now

            self.process_inputs()
            self.draw_background()
            self.draw_entities()
            pygame.display.update()
