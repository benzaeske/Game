from typing import Tuple

import pygame
from pygame import Surface, Vector2
from pygame.key import ScancodeWrapper

from model.utils.vectorutils import limit_magnitude


class Player:

    def __init__(
        self,
        surface: Surface,
        width: float,
        height: float,
        camera_width: float,
        camera_height: float,
        world_boundary: Tuple[float, float],
        start_pos: Vector2 = Vector2(0.0, 0.0),
        max_speed: float = 1.0,
    ) -> None:
        self.surface: Surface = surface
        self.width: float = width
        self.height: float = height
        self.camera_width: float = camera_width
        self.camera_height: float = camera_height
        self.camera_w_adjust: float = camera_width / 2
        self.camera_h_adjust: float = camera_height / 2
        self.world_boundary: Tuple[float, float] = world_boundary
        self.position: Vector2 = start_pos
        self.max_speed: float = max_speed

    def move_player(
        self,
        key_presses: ScancodeWrapper,
        dt: float,
    ) -> None:
        """
        Moves the player according to the keys pressed. Movement is scaled with delta time like all other entities.
        Limits the camera position to be confined within positive x,y coordinates and under the provided world boundary.
        """
        velocity: Vector2 = Vector2(0.0, 0.0)
        # Calculate velocity as the sum of key presses
        if key_presses[pygame.K_LEFT]:
            velocity += Vector2(-self.max_speed, 0)
        if key_presses[pygame.K_RIGHT]:
            velocity += Vector2(self.max_speed, 0)
        if key_presses[pygame.K_UP]:
            velocity += Vector2(0, self.max_speed)
        if key_presses[pygame.K_DOWN]:
            velocity += Vector2(0, -self.max_speed)
        limit_magnitude(velocity, self.max_speed)
        self.position += velocity * dt
        # Don't let the camera go outside the world boundary
        if self.position.x - self.camera_w_adjust < 0:
            self.position.x = self.camera_w_adjust
        if self.position.x + self.camera_w_adjust >= self.world_boundary[0]:
            self.position.x = self.world_boundary[0] - self.camera_w_adjust - 1
        if self.position.y - self.camera_h_adjust < 0:
            self.position.y = self.camera_h_adjust
        if self.position.y + self.camera_h_adjust >= self.world_boundary[1]:
            self.position.y = self.world_boundary[1] - self.camera_h_adjust - 1

    def get_camera_adjusted_position(self) -> Tuple[float, float]:
        """
        Returns the coordinates of the top left corner of the player in the center of the screen
        """
        return (
            self.camera_w_adjust - self.width / 2,
            self.camera_h_adjust - self.height / 2,
        )


class Turtle(Player):
    def __init__(
        self,
        camera_width: float,
        camera_height: float,
        world_boundary: Tuple[float, float],
    ) -> None:
        turtle_size: float = 100.0
        turtle_speed: float = 500.0
        turtle_color: Tuple[int, int, int] = (0, 200, 0)
        turtle_surface: Surface = Surface((turtle_size, turtle_size))
        turtle_surface.fill(turtle_color)
        super().__init__(
            turtle_surface,
            turtle_size,
            turtle_size,
            camera_width,
            camera_height,
            world_boundary,
            Vector2(world_boundary[0] / 2, world_boundary[1] / 2),
            turtle_speed,
        )
