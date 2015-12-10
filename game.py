from engine import Game, Writer

if __name__ == '__main__':
    game = Game()

    while not game.over:
        game.step()
        game.test_achievements()

    Writer.print_game_over()
    input()

    game.save_and_quit()
