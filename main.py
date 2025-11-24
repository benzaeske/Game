from controller.controller import GameController
from model.model import RandomSquareAgent

game_controller = GameController()

num_agents = 33
agent_size = 33
agent_speed = 33.0
for x in range(0, num_agents):
    game_controller.add_game_entity(
        RandomSquareAgent(
            agent_size,
            agent_speed,
            game_controller.view.screen_width,
            game_controller.view.screen_height,
        )
    )

game_controller.start_game()
