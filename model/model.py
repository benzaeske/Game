from pygame import Vector2

from model.entities.gameentity import GameEntity


class Model:
    def __init__(self, screen_width, screen_height):
        self.screen_width: int = screen_width
        self.screen_height: int = screen_height
        self.entities: list[GameEntity] = []

        print("Initialized model")

    def update_model(self, dt: float, mouse_pos: Vector2) -> None:
        for entity in self.entities:
            entity.apply_forces(self.entities, mouse_pos)
        for entity in self.entities:
            entity.update_position(self.screen_width, self.screen_height, dt)
