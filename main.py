from controller.controller import GameController, ControllerOptions
from model.entities.boid import BoidFactory, FlockingParameters

world_width = 10000
world_height = 10000
cell_size = 100.0
background_color = (0, 0, 0)

game_controller = GameController(
    ControllerOptions(world_width, world_height, cell_size, background_color)
)

# Boid options
num_agents = 2000
agent_size = 11.0
agent_speed = 300.0
max_acceleration = 1.0
entity_color = (255, 255, 255)

# Flocking parameters
cohere_dist = 100.0
avoid_dist = 33.0
cohere_k = 1.0
avoid_k = 1.8
align_k = 1.0
target_mouse = False
target_k = 1.0

boid_factory = BoidFactory(
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
    entity_color,
)

for x in range(0, num_agents):
    game_controller.add_game_entity(boid_factory.create_random_boid())

game_controller.start_game()
