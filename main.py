import random

from pygame import Vector2

from controller.controller import GameController, ControllerOptions
from model.entities.fish import SchoolingParameters, FishFactory, FishTypes

world_width = 6400.0
world_height = 6400.0
cell_size = 128.0
background_color = (0, 0, 0)

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size, background_color)
)


def get_red_school_with_random_target(school_id: int):
    return FishFactory(
        FishTypes.RED,
        SchoolingParameters(
            128.0,
            48.0,
            1.0,
            1.8,
            1.0,
            school_id,
            Vector2(
                random.randint(int(cell_size), int(world_width - cell_size)),
                random.randint(int(cell_size), int(world_height - cell_size)),
            ),
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


# Fishy
red_school_count: int = 10
red_count: int = 50
for x in range(red_school_count):
    school: FishFactory = get_red_school_with_random_target(x)
    for _ in range(red_count):
        game_controller.add_game_entity(school.create_random_boid())

green_school_1 = FishFactory(
    FishTypes.GREEN,
    SchoolingParameters(
        256.0,
        96.0,
        1.0,
        1.8,
        1.0,
        red_school_count + 1,
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
    SchoolingParameters(
        128.0,
        48.0,
        1.0,
        1.8,
        1.0,
        red_school_count + 2,
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


green_count: int = 300
for x in range(green_count):
    game_controller.add_game_entity(green_school_1.create_random_boid())

yellow_count: int = 300
for x in range(yellow_count):
    game_controller.add_game_entity(yellow_school_1.create_random_boid())

game_controller.start_game()
