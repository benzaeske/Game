import time

import pygame
from model.entitygroup import SquareGroup
from model.gridspace import GridSpace


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

        # Global screen variables
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

        # Initialize a game state
        self._entities = []
        self._entity_groups = []

    def add_entity(self, entity):
        self._entities.append(entity)

    def add_square_group(self, magnitude, color, size, mass, frequency):
        self._entity_groups.append(
            SquareGroup(
                magnitude,
                self.SCREEN_SIZE,
                self.SCREEN_SIZE,
                color,
                size,
                mass,
                frequency,
            )
        )

    def fill_background(self):
        """Fills the whole screen by re drawing the entire background"""
        self.background.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.background, (0, 0))

    def draw_background(self):
        """Re-draws the background but only over the list of entities on screen"""
        for entity in self._entities:
            self.screen.blit(self.background, entity.get_rect())

    def update_entities(self, dt):
        for entity in self._entities:
            entity.move_with_unit_vector(
                self.grid_space.get_force_vector_at_position(
                    entity.get_rect().centerx, entity.get_rect().centery
                ),
                dt,
            )

    def manage_entity_groups(self, dt):
        for entity_group in self._entity_groups:
            entity_group.tick(dt)
            if entity_group.can_spawn():
                self._entities.extend(entity_group.spawn())

    def draw_entities(self):
        for entity in self._entities:
            self.screen.blit(entity.get_surface(), entity.get_rect())

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
            self.update_entities(dt)
            self.manage_entity_groups(dt)
            self.draw_entities()
            pygame.display.update()

            self.clock.tick(self.FPS)
