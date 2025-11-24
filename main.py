from pygame import Vector2

from controller.controller import GameController

game_controller = GameController()

for x in range(0, 25):
    for y in range(0, 25):
        game_controller.create_square_entity(
            50,
            (0, 255 - (x * 5) - (y * 5), 0),
            Vector2(x * 60 + 25.0, y * 60 + 25.0),
            Vector2(5.0, -1.0),
            25.0,
            Vector2(2.5, 0.5),
        )

game_controller.start_game()
