import cProfile
import pstats
import random

from itertools import cycle
from GameEngine import Game
from GameNode import heuristic_stones_far_from_mancala, heuristic_steal, heuristic_most_points, heuristic_points_diff


def print_hi(name):
    print(f'Hi, {name}')


def to_csv():
    res1 = "mode,first_move,depth,first_time,second_time,first_moves,second_moves,heuristic,first_points,second_points\n"
    res = "first_move,depth,heuristic_1,first_points,heuristic_2,second_points\n"
    for i in range(2, 5):
        for mode in ["minmax", "alfabeta"]:
            with open(f"Results/heuristics/result_{i}_{mode}_{mode}_heuristic.txt",
                      "r") as g:
                lines = g.readlines()
                for line in lines:
                    if line.startswith("First move:"):
                        splitted = line.split(' ')
                        first_move = splitted[2]
                        depth = splitted[4][:-1]
                        res1 += f"{mode},{first_move},{depth},"

                    if line.startswith("First (0) time"):
                        splitted = line.split(' ')
                        first_time = splitted[-1].replace("ms", "")[:-1]
                        res1 += f"{first_time},"
                    if line.startswith("Second (1) time"):
                        splitted = line.split(' ')
                        second_time = splitted[-1].replace("ms", "")[:-1]
                        res1 += f"{second_time},"
                    if line.startswith("First (0) moves"):
                        splitted = line.split(' ')
                        first_moves = splitted[-1][:-1]
                        res1 += f"{first_moves},"
                    if line.startswith("Second (1) moves"):
                        splitted = line.split(' ')
                        second_moves = splitted[-1][:-1]
                        res1 += f"{second_moves},"
                    if line.startswith("First (0) :"):
                        splitted = line.split(' ')
                        heu1 = splitted[3]
                        points = []
                        for a, word in enumerate(splitted):

                            if word.startswith('['):
                                points.append(word[1:-1])
                                index = a
                        res1 += f"{heu1}, {points[0]}, {points[1]}\n"
                print(res1)

        with open(f"Results/tournament/result_{i}_alfabeta_alfabeta_heuristic.txt",
                  "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith("First move:"):
                    splitted = line.split(' ')
                    first_move = splitted[2]
                    depth = splitted[4][:-1]
                    res += f"{first_move},{depth},"

                if line.startswith("First (0) :"):
                    splitted = line.split(' ')
                    heu1 = splitted[3]
                    points = []
                    for a, word in enumerate(splitted):

                        if word.startswith('['):
                            points.append(word[1:-1])
                            index = a
                    heu2 = splitted[index+1]
                    res += f"{heu1},{points[0]},{heu2},{points[1]}\n"
            print(res)

    with open(f"Results/heuristics/summary2.csv",
              "w") as n:
        n.write(res1)

    with open(f"Results/tournament/summary2.csv",
              "w") as m:
        m.write(res)


if __name__ == '__main__':


    # profile = cProfile.Profile()
    # profile.runcall(lambda: game.start_game())
    # ps = pstats.Stats(profile)
    # ps.print_stats()
    # to_csv()
    # for level in range(2, 5):
    #     for heuristic in [heuristic_steal, heuristic_most_points, heuristic_points_diff, heuristic_stones_far_from_mancala]:
    #         for mode in ["minmax", "alfabeta"]:
    #             for i in range(1, 7):
    #                 game = Game()
    #                 game.start_game(first_move=i, testing=True, ai_depth_level=level, mode=mode, directory="heuristics", heuristic1=heuristic, heuristic2=heuristic)

    # for level in range(2, 5):
    #     for heuristic1 in [heuristic_steal, heuristic_most_points, heuristic_points_diff,
    #                       heuristic_stones_far_from_mancala]:
    #         for heuristic2 in [heuristic_steal, heuristic_most_points, heuristic_points_diff,
    #                            heuristic_stones_far_from_mancala]:
    #             for i in range(1, 3):
    #                 first_move = random.randint(1, 6)
    #                 game = Game()
    #                 game.start_game(first_move=first_move, testing=True, ai_depth_level=level, mode="alfabeta", heuristic1=heuristic1, heuristic2=heuristic2, directory="tournament")

    game = Game()
    game.start_game(first_move=3, testing=True, ai_depth_level=3, mode="alfabeta", heuristic1=heuristic_steal, heuristic2=heuristic_steal)

