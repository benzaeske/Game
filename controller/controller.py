import sys
import time

import pygame

from model.gridspace import GridSpace
from model.horde import Horde


class Game:
    """Basic representation of a game. Defines a pygame setup and game loop"""

    def __init__(self):
        """Initialize a new game with display set to full screen and 60 FPS"""
        pygame.init()

        # Global dimensions
        self.DISPLAY_INFO = pygame.display.Info()
        self.DISPLAY_W, self.DISPLAY_H = (
            self.DISPLAY_INFO.current_w,
            self.DISPLAY_INFO.current_h,
        )
        self.SCREEN_SIZE = (
            self.DISPLAY_W if self.DISPLAY_W < self.DISPLAY_H else self.DISPLAY_H
        )
        self.BACKGROUND_COLOR = (255, 255, 255)

        # Screen variables
        self.screen = pygame.display.set_mode(
            (self.SCREEN_SIZE, self.SCREEN_SIZE), pygame.FULLSCREEN | pygame.SCALED
        )
        self.background = pygame.Surface((self.SCREEN_SIZE, self.SCREEN_SIZE))
        self.background.fill(self.BACKGROUND_COLOR)

        # Global FPS and clock
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_start = 0

        # Grid system
        self.grid_space = GridSpace(self.DISPLAY_W, self.DISPLAY_H, 5)

        # Initialize a player at the middle
        # self.player = Square(50, (0, 102, 0), 500)
        # self.player.set_position(self.DISPLAY_W / 2, self.DISPLAY_H / 2)

        # Initialize a list of enemy entities
        self.enemies = []

        # Initialize a horde
        self.red_horde = Horde(30, self.SCREEN_SIZE, self.SCREEN_SIZE)
        self.hordes_spawned = 0

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
        # self.screen.blit(self.background, self.player.get_rect())
        for enemy in self.enemies:
            self.screen.blit(self.background, enemy.get_rect())

    def update_player(self, dt):
        keys = pygame.key.get_pressed()
        self.player.move_with_unit_vector(
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
            keys[pygame.K_UP] - keys[pygame.K_DOWN],
            dt,
        )

    def update_enemies(self, dt):
        for enemy in self.enemies:
            enemy.move_with_unit_vector(
                self.grid_space.get_force_vector_at_position(
                    enemy.get_rect().centerx, enemy.get_rect().centery
                ),
                dt,
            )

    def manage_hordes(self):
        # spawn a horde every 10 seconds
        game_time = time.time() - self.game_start
        if game_time / 10 > self.hordes_spawned:
            self.enemies.extend(self.red_horde.spawn_entities())
            self.hordes_spawned += 1

    def draw_entities(self):
        # self.screen.blit(self.player.get_surface(), self.player.get_rect())
        for enemy in self.enemies:
            self.screen.blit(enemy.get_surface(), enemy.get_rect())

    def run(self):
        """Run the game loop"""
        self.fill_background()
        # Track game run time
        self.game_start = prev_frame_start = time.time()
        while True:
            # Calculate delta time
            now = time.time()
            dt = now - prev_frame_start
            prev_frame_start = now

            self.check_for_terminate()

            # Update game by a single frame
            self.draw_background()
            self.update_enemies(dt)
            self.manage_hordes()
            self.draw_entities()
            pygame.display.update()

            self.clock.tick(self.FPS)
