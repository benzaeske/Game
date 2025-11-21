from controller.controller import Game
from model.shapes import Square

game = Game()

square = Square(50, (0, 102, 0))
square.set_position(game.WIDTH / 2, game.HEIGHT / 2)
game.add_entity(square)

game.run()
