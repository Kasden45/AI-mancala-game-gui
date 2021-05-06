import cProfile
import pstats

import GameEngine
from itertools import cycle
from GameEngine import Game


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':


    # profile = cProfile.Profile()
    # profile.runcall(lambda: game.start_game())
    # ps = pstats.Stats(profile)
    # ps.print_stats()

    for level in range(4, 5):
        for mode in ["minmax", "alfabeta"]:
            for i in range(1, 7):
                game = Game()
                game.start_game(first_move=i, testing=True, ai_depth_level=level, mode=mode)

