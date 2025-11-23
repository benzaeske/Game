from controller.game import Game

game = Game()
game.add_square_group(1, (0, 200, 0), 33, 100, 5)
game.run()
