import random
from typing import Tuple

import pygame
from pygame import Surface
from pygame.key import ScancodeWrapper

from model.entities.gameentity import GameEntity
from model.player.player import Player
from model.world.grid_cell import GridCell


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
        player: Player,
    ):
        self.world_width: float = world_width
        self.world_height: float = world_height
        self.cell_size: float = cell_size
        self.grid_width: int = int(self.world_width / self.cell_size)
        self.grid_height: int = int(self.world_height / self.cell_size)
        self.player: Player = player
        self.grid_space: list[list[GridCell]] = self.initialize_grid_space()

    def initialize_grid_space(self) -> list[list[GridCell]]:
        grid_space: list[list[GridCell]] = []
        for row in range(self.grid_height):
            grid_space.append([])
            for col in range(self.grid_width):
                background: Surface = pygame.Surface((self.cell_size, self.cell_size))
                noise: int = random.randint(0, 25)
                background.fill((0, 50 + noise, 115 + noise * 2))
                grid_space[row].append(
                    GridCell(
                        self.cell_size, row, col, self.player.camera_height, background
                    )
                )
        return grid_space

    def update_model(self, dt: float, key_presses: ScancodeWrapper) -> None:
        # Apply forces to all entities
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for entity in self.grid_space[row][col].entities:
                    self.apply_forces_to_entity(entity)
        # Move entities:
        # This must be done after all forces have been applied and entity velocities are updated for this frame
        update_cells: list[Tuple[int, int, GameEntity]] = []
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                for i in range(len(self.grid_space[row][col].entities) - 1, -1, -1):
                    e = self.grid_space[row][col].entities[i]
                    e.update_position(self.world_width, self.world_height, dt)
                    # Check if we are in a new grid cell. If we are, move the entity to the other grid cell's list
                    new_r = int(e.position.y / self.cell_size)
                    new_c = int(e.position.x / self.cell_size)
                    if new_r != row or new_c != col:
                        del self.grid_space[row][col].entities[i]
                        # Track which entities moved grid cells
                        update_cells.append((new_r, new_c, e))
        # Update grid cells with entities that moved into new cells:
        # This must be done after all entities have moved otherwise we run the risk of processing an entity's position update twice
        for cell_entity in update_cells:
            self.grid_space[cell_entity[0]][cell_entity[1]].entities.append(
                cell_entity[2]
            )
        # Move playeraaaa
        self.player.move_player(key_presses, dt)

    def apply_forces_to_entity(self, entity: GameEntity) -> None:
        """
        Finds this entity's relevant neighbors and applies forces using only the list of relevant neighbors
        """
        # Relevant neighbors are any entities in the 'cell_range' grid squares surrounding the current entity's grid square
        cell_range: int = entity.cell_interaction_range
        neighbors: list[GameEntity] = []
        r: int = int(entity.position.y / self.cell_size)
        c: int = int(entity.position.x / self.cell_size)
        for dr in range(-cell_range, cell_range + 1):
            for dc in range(-cell_range, cell_range + 1):
                grid_r: int = r + dr
                grid_r = (grid_r + self.grid_height) % self.grid_height
                grid_c: int = c + dc
                grid_c = (grid_c + self.grid_width) % self.grid_width
                neighbors.extend(self.grid_space[grid_r][grid_c].entities)
        entity.apply_forces(neighbors)

    def add_game_entity(self, entity: GameEntity) -> None:
        self.grid_space[int(entity.position.y / self.cell_size)][
            int(entity.position.x / self.cell_size)
        ].entities.append(entity)

    def get_grid_cells_in_range(
        self, x_range: Tuple[float, float], y_range: Tuple[float, float]
    ) -> list[GridCell]:
        left: int = int(x_range[0] / self.cell_size)
        right: int = int(x_range[1] / self.cell_size)
        bottom: int = int(y_range[0] / self.cell_size)
        top: int = int(y_range[1] / self.cell_size)
        cells: list[GridCell] = []
        for r in range(bottom, top + 1):
            for c in range(left, right + 1):
                cells.append(self.grid_space[r][c])
        return cells

    def get_grid_cells_in_camera_range(self) -> list[GridCell]:
        return self.get_grid_cells_in_range(
            (
                self.player.position.x - self.player.camera_w_adjust,
                self.player.position.x + self.player.camera_w_adjust,
            ),
            (
                self.player.position.y - self.player.camera_h_adjust,
                self.player.position.y + self.player.camera_h_adjust,
            ),
        )

    def get_entities_in_range(
        self, x_range: Tuple[float, float], y_range: Tuple[float, float]
    ) -> list[GameEntity]:
        """
        Finds the grid cells that are within the x, y range specified and returns all entities in those grid cells
        """
        left: int = int(x_range[0] / self.cell_size)
        right: int = int(x_range[1] / self.cell_size)
        bottom: int = int(y_range[0] / self.cell_size)
        top: int = int(y_range[1] / self.cell_size)
        entities: list[GameEntity] = []
        for r in range(bottom, top + 1):
            for c in range(left, right + 1):
                entities.extend(self.grid_space[r][c].entities)
        return entities

    def get_entities_in_camera_range(self):
        return self.get_entities_in_range(
            (
                self.player.position.x - self.player.camera_w_adjust,
                self.player.position.x + self.player.camera_w_adjust,
            ),
            (
                self.player.position.y - self.player.camera_h_adjust,
                self.player.position.y + self.player.camera_h_adjust,
            ),
        )
