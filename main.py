from controller.game import Game

game = Game()
game.add_square_group(5, (0, 200, 0), 33, 10, 2)
game.run()
