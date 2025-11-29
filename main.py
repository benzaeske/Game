from controller.controller import GameController, ControllerOptions
from model.entities.boid import FlockingParameters, FishFactory, FishTypes

world_width = 6400.0
world_height = 6400.0
cell_size = 128.0
background_color = (0, 0, 0)

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size, background_color)
)

# Boid options
num_agents = 1000
agent_size = 32.0
agent_speed = 200.0
max_acceleration = 1.0

# Flocking parameters
cohere_dist = 128.0
avoid_dist = 48.0
cohere_k = 1.0
avoid_k = 1.8
align_k = 1.0
target_mouse = False
target_k = 1.0

red_school = FishFactory(
    FishTypes.RED,
    FlockingParameters(
        cohere_dist,
        avoid_dist,
        cohere_k,
        avoid_k,
        align_k,
        target_mouse=target_mouse,
        target_k=target_k,
    ),
    agent_size,
    agent_size,
    agent_speed,
    max_acceleration,
    (0.0, game_controller.model.world_width),
    (0.0, game_controller.model.world_height),
)

for x in range(0, num_agents):
    game_controller.add_game_entity(red_school.create_random_boid())

game_controller.start_game()
