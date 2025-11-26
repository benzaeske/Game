from typing import Tuple

from pygame import Vector2

from model.entities.gameentity import GameEntity


class SpatialPartitioningModel:
    """
    Implementation of spatial partitioning. The 'world' is divided into a grid of cells. The size of a cell determines how far entities in the simulation can 'see'.\n
    When applying forces to entities, calculations are only performed on neighbors within the entity's cell and the 8 cells surrounding it instead of every entity that exists.\n
    The world width and height must be evenly divisible by cell_size, or array out of bounds issues will occur\n
    """

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
        # Move entities:
        # This must be done after all forces have been applied and entity velocities are updated for this frame
        update_cells: list[Tuple[int, int, GameEntity]] = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for i in range(len(self.grid_space[row][col]) - 1, -1, -1):
                    e = self.grid_space[row][col][i]
                    e.update_position(self.world_width, self.world_height, dt)
                    # Check if we are in a new grid cell. If we are, move the entity to the other grid cell's list
                    new_r = int(e.position.y / self.cell_size)
                    new_c = int(e.position.x / self.cell_size)
                    if new_r != row or new_c != col:
                        del self.grid_space[row][col][i]
                        # Track which entities moved grid cells
                        update_cells.append((new_r, new_c, e))
        # Update grid cells with entities that moved into new cells:
        # This must be done after all entities have moved otherwise we run the risk of processing an entity's position update twice
        for cell_entity in update_cells:
            self.grid_space[cell_entity[0]][cell_entity[1]].append(cell_entity[2])

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
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                neighbors.extend(self.grid_space[grid_r][grid_c])
        entity.apply_forces(neighbors, mouse_pos)

    def add_game_entity(self, entity: GameEntity) -> None:
        self.grid_space[int(entity.position.y / self.cell_size)][
            int(entity.position.x / self.cell_size)
        ].append(entity)
