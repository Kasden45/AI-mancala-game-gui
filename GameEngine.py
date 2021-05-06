import math
import pprint
import random
from copy import copy
from typing import List, Tuple
import time

import MinMax
from GameNode import GameNode,make_decision_tree, pprint_tree, mancala_function, is_finished
from Player import Player
from Components import Stone, Hole, Mancala
from itertools import cycle

COLORS = ["blue", "red", "yellow", "green", "white", "black"]
#COLORS = ["b", "r", "y", "g", "w", "bl"]


class Game:
    def __init__(self):
        self.turn = 0
        self.players = {}

        self.number_of_stones = 4
        self.holes_in_row = 6

        self.holes = {}  # cyclic
        self.stones = []

        self.additional_move = False
        self.total_holes = 14
        self.moves_table = []  # (id, move)

    def get_possible_moves(self, player_id):  # Should be used in move(), can check instance instead of number
        return list([hole.number for _, hole in self.holes.items() if hole.player.id == player_id and len(hole.stones) > 0 and hole.number != 7])

    def get_mancala(self, player_id):
        for hole in self.holes.values():
            if isinstance(hole, Mancala) and hole.player.id == player_id:
                return hole

    def get_next_hole(self, hole):
        next_number = self.global_hole_number(hole) + 1
        if next_number > self.total_holes:
            next_number = 1
        next_hole = self.holes[next_number]
        if isinstance(next_hole, Mancala) and next_hole.player.id != self.turn:
            return self.get_next_hole(next_hole)
        else:
            return next_hole

    def change_turn(self):
        for player_id in self.players.keys():
            if player_id != self.turn:
                self.turn = player_id
                return

    def global_hole_number(self, hole):
        hole_number = hole.number
        player_id = hole.player.id
        return hole_number + (self.holes_in_row + 1) * player_id

    def initialize_game(self, players: Tuple[Player, Player]):
        self.players[players[0].id] = players[0]  # 0
        self.players[players[1].id] = players[1]  # 1
        # Initialize players, holes and stones
        for player in self.players.values():
            for hole_number in range(1, self.holes_in_row + 1):
                stones = []
                for stone_number in range(self.number_of_stones):
                    stone = Stone(COLORS[stone_number])
                    self.stones.append(stone)
                    stones.append(stone)  # Stones have colors assigned
                hole = Hole(hole_number, stones, player)
                self.holes[self.global_hole_number(hole)] = hole
            self.holes[self.holes_in_row + 1 + (self.holes_in_row + 1) * player.id] = Mancala([], player)
        self.total_holes = 2 * (self.holes_in_row + 1)

    def get_opponent_id(self, player_id):
        return [k for k in self.players.keys() if k != player_id][0]

    def get_points(self, player_id):
        return len(self.get_mancala(player_id).stones)

    def move(self, player_id, hole_number):
        hole = None
        for some_hole in self.holes.values():
            if some_hole.number == hole_number and some_hole.player.id == player_id:
                hole = some_hole
                break

        if hole is None or len(hole.stones) == 0:
            return False

        self.moves_table.append({"P": player_id, "H": hole_number})
        # Take stones
        stones = copy(hole.stones)
        hole.stones.clear()
        while len(stones) != 0:
            stone = stones[0]
            stones.remove(stone)
            hole = self.get_next_hole(hole)
            was_empty = len(hole.stones) == 0  # Check if hole was empty before adding stone
            hole.add_stone(stone)
            if len(stones) == 0:  # Last stone placed
                if was_empty and hole.player.id == player_id and not isinstance(hole, Mancala):  # Steal opportunity
                    opposite_hole = self.get_opposite_hole(hole)
                    if len(opposite_hole.stones) > 0:  # Steal
                        self.steal_stones(hole, opposite_hole, player_id)
                elif hole == self.get_mancala(player_id):
                    self.additional_move = True
        return True

    def steal_stones(self, hole, opposite_hole, player_id):
        mancala = self.get_mancala(player_id)
        mancala.stones.extend(hole.stones)
        mancala.stones.extend(opposite_hole.stones)
        for stone in opposite_hole.stones:
            stone.moved = True
        hole.stones.clear()
        opposite_hole.stones.clear()

    def set_turn(self, player_id=None):
        if player_id is None:
            return random.choice(list(self.players.keys()))
        else:
            return player_id

    def get_players(self, how_many=2, first_bot="minmax", second_bot="minmax", testing=False):
        player1 = Player(0)
        player2 = Player(1)
        if how_many == 2:
            if not testing:
                print("1st player!")
                name1 = input("Please type your name: ")
                player1.name = name1
                print(f"Hi, {name1}!")
                type1 = input(f"Are you a human, {name1}?: 'YES'/'NO' ->")
                player1.type = "Human" if type1 == "YES" else "AI"
                if player1.type == "AI":
                    player1.name += " (AI)"
                    player2.AI_mode = first_bot
                    player1.AI_mode = first_bot

                print("2nd player!")
                name2 = input("Please type your name: ")
                player2.name = name2
                print(f"Hi, {name2}!")
                type2 = input(f"Are you a human, {name2}?: 'YES'/'NO' ->")
                player2.type = "Human" if type2 == "YES" else "AI"
                if player2.type == "AI":
                    player2.name += " (AI)"
                    player2.AI_mode = second_bot
                    player1.AI_mode = second_bot
            if testing:
                player1.name = "First"
                player1.type = "AI"
                player1.AI_mode = first_bot
                player1.name += " (AI)"

                player2.name = "Second"
                player2.type = "AI"
                player2.AI_mode = second_bot
                player2.name += " (AI)"
                print("TESTING")

        print("Players created!")
        return player1, player2

    def get_opposite_hole(self, hole):
        return self.holes[14 - self.global_hole_number(hole)]  # Opposite hole to steal from

    def get_player_move(self):
        player_on_turn = self.players[self.turn]
        print(f"{player_on_turn.name}'s move!")
        hole = int(input("I pick hole number:"))
        if hole in self.get_possible_moves(self.turn):  # Check if move is possible
            return hole
        else:
            return 0

    def get_hole(self, number, player_id):
        for hole in self.holes.values():
            if hole.player.id == player_id and hole.number == number:
                return hole

    def calculate_result(self):
        print("Leaderboard")
        string_result = {}
        for player_id, player in self.players.items():
            player.points = len(self.get_mancala(player_id).stones)
        for i, player in enumerate(sorted(self.players.values(), key=lambda p: p.points, reverse=True)):
            string_result[i+1] = f"{i+1}. {str(player)}"
            print(f"{i+1}.", str(player))
        return string_result

    def print_game_state(self, mode="colors"):
        if mode == "colors":
            for hole_num, hole in sorted(
                    [(hole_num, hole) for (hole_num, hole) in self.holes.items() if hole_num in range(8, 15)],
                    key=lambda h: h[0], reverse=True):
                print(f"{hole_num}: {hole}", end=" -- ")
            print()
            for hole_num, hole in sorted(
                    [(hole_num, hole) for (hole_num, hole) in self.holes.items() if hole_num in range(1, 8)],
                    key=lambda h: h[0], reverse=False):
                print(f"{hole_num}: {hole}", end=" -- ")
        elif mode == "numbers":
            print("\n{:^52}\n".format(f"{self.players[1].name}: {self.get_points(1)}"))
            print("", end="    ")
            print(" M ".format(), end="    ")
            for hole_num in range(6, 0, -1):
                print(" {} ".format(hole_num), end="    ")

            print()
            print("", end=" <- ")
            for hole_num, hole in sorted(
                    [(hole_num, hole) for (hole_num, hole) in self.holes.items() if hole_num in range(8, 15)],
                    key=lambda h: h[0], reverse=True):
                print("{}".format(f"({hole.count()})"), end=" <- ")
            print()
            print("", end="        -> ")
            for hole_num, hole in sorted(
                    [(hole_num, hole) for (hole_num, hole) in self.holes.items() if hole_num in range(1, 8)],
                    key=lambda h: h[0], reverse=False):
                print("{}".format(f"({hole.count()})"), end=" -> ")
            print()
            print("", end="           ")
            for hole_num in range(1, 7):
                print(" {} ".format(hole_num), end="    ")
            print(" M ".format(), end="    ")
            print()
            print("\n{:^52}\n".format(f"{self.players[0].name}: {self.get_points(0)}"))

    def finish_game(self):
        # Place all stones from holes to Mancalas
        for player_id, player in self.players.items():
            mancala = self.get_mancala(player_id)
            for hole in self.holes.values():
                if hole.player.id == player_id and not isinstance(hole, Mancala):
                    for stone in hole.stones:
                        stone.moved = True
                    mancala.stones.extend(hole.stones)
                    hole.stones.clear()

            player.points = len(mancala.stones)

    def is_finished(self):
        return len([True for hole in self.holes.values() if
                    hole.player.id == self.turn and not isinstance(hole, Mancala) and len(hole.stones) > 0]) == 0

    def start_game(self, testing=False, first_move=0, ai_depth_level=2, mode=None):
        if mode is None:
            first_bot_mode = "minmax"
            second_bot_mode = "minmax"
        else:
            first_bot_mode = mode
            second_bot_mode = mode
        if testing:
            players = self.get_players(2, first_bot=first_bot_mode, second_bot=second_bot_mode, testing=testing)
        else:
            players = self.get_players(2)
        self.initialize_game(players)
        self.set_turn(0)
        next_best_move = first_move  # If 0 then first move is random if done by AI
        ai_depth = ai_depth_level
        next_best_node = None
        # Game start

        while not self.is_finished():
            # Print board
            self.print_game_state("numbers")
            # Print leaderboard
            self.calculate_result()

            hole_number = next_best_move
            # Human's move
            if self.players[self.turn].type == "Human":
                hole_number = self.get_player_move()
                while hole_number == 0:
                    print("Enter correct number!")
                    hole_number = self.get_player_move()

                print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")

                self.move(self.turn, hole_number)
            # AI's move
            elif self.players[self.turn].type == "AI":
                if hole_number != 0:
                    self.move(self.turn, hole_number)
                    if not testing:
                        print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")
                else:  # If first move then random
                    if not testing:
                        print("Random AI move")
                    hole_number = random.choice(list(self.get_possible_moves(self.turn)))
                    self.move(self.turn, hole_number)
                    if not testing:
                        print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")

            if not self.additional_move:
                self.change_turn()
            self.additional_move = False
            # # Beginning of computing
            # start_time = time.perf_counter()
            #  Create decision tree
            if next_best_node is None:
                root = GameNode(self, hole_number, self.turn)
            else:
                root = next_best_node
            make_decision_tree(root, ai_depth)
            # Beginning of computing alg only
            start_time = time.perf_counter()
            # Compute node values
            MinMax.minmax(root, ai_depth, -math.inf, math.inf, mancala_function, is_finished, root.player_id,
                          is_alfa_beta=True if self.players[self.turn].AI_mode == "alfabeta" else False)  # True
            if len(root.children) > 0:
                if not testing:
                    print("Next move options:")
                    for child in root.children:  # Print options
                        print("Hole:", child.number, child.value)
                # next_best_node = max(root.children, key=lambda n: n.value).number
                # next_best_move = next_best_node.number
                next_best_move = max(root.children, key=lambda n: n.value).number
                if not testing:
                    print("Next best move:", next_best_move)
            # End of computing
            end_time = time.perf_counter()
            self.players[self.turn].computing_time += (end_time - start_time)
            print("Time:", (end_time - start_time))
            #pprint_tree(root)

        # Game finished
        self.finish_game()
        # Print board
        self.print_game_state("numbers")
        # Print leaderboard
        results = self.calculate_result()
        if not testing:
            print("\nAnd the winner is . . .", end=" ")
            if self.players[0].points == self.players[1].points:
                print("nobody. It's a draw!\n")
            else:
                winner = max(self.players.values(), key=lambda p: p.points)
                print("{} with {} points! Congrats!\n".format(winner.name, winner.points))
            print("All moves:")
            # Print all moves
            pprint.pprint(self.moves_table)
        if testing:
            with open(f"Results/test_{ai_depth_level}_{first_bot_mode}_{second_bot_mode}.txt", "a") as f:
                f.write(f"First move: {first_move} Depth: {ai_depth_level}\n{self.players[0]} vs {self.players[1]}\n")
                f.write(f"First (0) time = {self.players[0].computing_time * 1000}ms\n"
                        f"Second (1) time = {self.players[1].computing_time * 1000}ms")
                f.write("\n")
                f.write(f"First (0) moves = {len([move for move in self.moves_table if move['P'] == 0])}\n"
                        f"Second (1) moves = {len([move for move in self.moves_table if move['P'] == 1])}")
                # f.write("\n")
                # f.write(pprint.pformat(self.moves_table))
                f.write("\n")
                f.write(pprint.pformat(results))
                f.write("\n")
                f.write("\n")
                f.write("\n")
