from pygame import Vector2

from controller.controller import GameController, ControllerOptions
from model.entities.boid import FlockingParameters, FishFactory, FishTypes

world_width = 6400.0
world_height = 6400.0
cell_size = 128.0
background_color = (0, 0, 0)

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size, background_color)
)

red_school_1 = FishFactory(
    FishTypes.RED,
    FlockingParameters(
        128.0,
        48.0,
        1.0,
        1.8,
        1.0,
        1,
        Vector2(world_width / 2, world_height / 2),
        1.0,
    ),
    32.0,
    32.0,
    200.0,
    1.0,
    (0.0, game_controller.model.world_width),
    (0.0, game_controller.model.world_height),
    1,
)

green_school_1 = FishFactory(
    FishTypes.GREEN,
    FlockingParameters(
        256.0,
        96.0,
        1.0,
        1.8,
        1.0,
        2,
        None,
        1.0,
    ),
    48.0,
    48.0,
    150.0,
    1.0,
    (0.0, game_controller.model.world_width),
    (0.0, game_controller.model.world_height),
    2,
)

yellow_school_1 = FishFactory(
    FishTypes.YELLOW,
    FlockingParameters(
        128.0,
        48.0,
        1.0,
        1.8,
        1.0,
        3,
        None,
        1.0,
    ),
    32.0,
    32.0,
    300.0,
    1.5,
    (0.0, game_controller.model.world_width),
    (0.0, game_controller.model.world_height),
    1,
)

# Fishy
red_count: int = 200
yellow_count: int = 500
green_count: int = 300

for x in range(red_count):
    game_controller.add_game_entity(red_school_1.create_random_boid())
for x in range(green_count):
    game_controller.add_game_entity(green_school_1.create_random_boid())
for x in range(yellow_count):
    game_controller.add_game_entity(yellow_school_1.create_random_boid())

game_controller.start_game()
