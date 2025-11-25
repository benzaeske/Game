from controller.controller import GameController
from model.entities.boid import BoidFactory, FlockingParameters

game_controller = GameController()

num_agents = 300
agent_size = 11.0
agent_speed = 100.0
max_force = 0.4

cohere_dist = 66.0
avoid_dist = 22.0
cohere_k = 1.0
avoid_k = 1.8
align_k = 1.0

flocking_settings = FlockingParameters(
    cohere_dist, avoid_dist, cohere_k, avoid_k, align_k
)
boid_factory = BoidFactory(
    flocking_settings,
    agent_size,
    agent_size,
    agent_speed,
    max_force,
    (0.0, game_controller.view.screen_width),
    (0.0, game_controller.view.screen_height),
)

for x in range(0, num_agents):
    game_controller.add_game_entity(boid_factory.create_random_boid())

game_controller.start_game()
