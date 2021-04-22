import cProfile
import pstats

import GameEngine
from itertools import cycle
from GameEngine import Game


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    game = Game()

    # profile = cProfile.Profile()
    # profile.runcall(lambda: game.start_game())
    # ps = pstats.Stats(profile)
    # ps.print_stats()

    game.start_game()

