from controller.controller import GameController
from model.entities.boid import BoidFactory, FlockingParameters

game_controller = GameController()

num_agents = 300
agent_size = 11.0
agent_speed = 200.0
max_acceleration = 1.5

# Flocking settings
cohere_dist = 66.0
avoid_dist = 33.0
cohere_k = 1.0
avoid_k = 2.0
align_k = 1.0
target_mouse = True
target_k = 1.5

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
    (0.0, game_controller.view.screen_width),
    (0.0, game_controller.view.screen_height),
)

for x in range(0, num_agents):
    game_controller.add_game_entity(boid_factory.create_random_boid())

game_controller.start_game()
