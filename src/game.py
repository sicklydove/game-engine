from engine import Game
import writer
from example_game import states, achievements

if __name__ == '__main__':
    game = Game(states, achievements)
    writer.init(200)

    while not game.over:
        game.step()
        game.test_achievements()

    writer.print_game_over()
    input()

    game.save_and_quit()
