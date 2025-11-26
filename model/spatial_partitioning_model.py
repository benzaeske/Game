from typing import Callable

from pygame import Vector2

from model.entities.gameentity import GameEntity


class SpatialPartitioningModel:
    def __init__(
        self,
        world_width: float,
        world_height: float,
        cell_size: float,
    ):
        self.world_width: float = world_width
        self.world_height: float = world_height
        self.cell_size: float = cell_size
        self.grid_width: int = int(self.world_width / self.cell_size)
        self.grid_height: int = int(self.world_height / self.cell_size)
        self.grid_space: list[list[list[GameEntity]]] = [
            [[] for _ in range(self.grid_width)] for _ in range(self.grid_height)
        ]

    def update_model(self, dt: float, mouse_pos: Vector2) -> None:
        # Apply forces to all entities
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for entity in self.grid_space[row][col]:
                    self.apply_forces_to_entity(entity, mouse_pos)
        # Move entities and update their location in the grid space if it has changed.
        # This must be done after all forces have already been applied to each entity's velocity
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for i in range(len(self.grid_space[row][col])):
                    e = self.grid_space[row][col][i]
                    e.update_position(self.world_width, self.world_height, dt)
                    # Check if we are in a new grid cell and move this entity to that grid cell's list if so
                    new_r = int(e.position.y / self.cell_size)
                    new_c = int(e.position.x / self.cell_size)
                    if new_r != row or new_c != col:
                        del self.grid_space[row][col][i]
                        self.grid_space[new_r][new_c].append(e)

    def apply_forces_to_entity(self, entity: GameEntity, mouse_pos: Vector2) -> None:
        """
        Finds this entity's relevant neighbors and applies forces using only the list of relevant neighbors
        """
        # Relevant neighbors are any entities in the 'cell_range' grid squares surrounding the current entity's grid square
        cell_range: int = 1
        neighbors: list[GameEntity] = []
        r: int = int(entity.position.y / self.cell_size)
        c: int = int(entity.position.x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = grid_r + self.grid_height % self.grid_height
                grid_c: int = c + dc
                grid_c = grid_c + self.grid_width % self.grid_width
                neighbors.extend(self.grid_space[grid_r][grid_c])
        entity.apply_forces(neighbors, mouse_pos)

    def add_game_entity(self, entity: GameEntity) -> None:
        self.grid_space[int(entity.position.y / self.cell_size)][
            int(entity.position.x / self.cell_size)
        ].append(entity)

    def loop_entities(self, callback: Callable[[GameEntity], None]) -> None:
        """
        Loops over entities in the grid space and executes the provided function callback for each one
        :param callback: The function that will execute with each entity
        """
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for entity in self.grid_space[row][col]:
                    callback(entity)
