import sys

import pygame


class Game:
    """Basic representation of a game. Defines a pygame setup and game loop"""

    def __init__(self):
        """Initialize a new game with display set to full screen and 60 FPS"""
        pygame.init()
        self.DISPLAY_INFO = pygame.display.Info()
        self.WIDTH = self.DISPLAY_INFO.current_w
        self.HEIGHT = self.DISPLAY_INFO.current_h
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.FPS = 60
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

    @staticmethod
    def process_inputs():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def draw_background(self):
        # White background
        self.screen.fill(self.BACKGROUND_COLOR)

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
            self.process_inputs()
            self.draw_background()
            self.draw_entities()
            # Display changes
            pygame.display.update()
            # Drive FPS
            self.clock.tick(self.FPS)
