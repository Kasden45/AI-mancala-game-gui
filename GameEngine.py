import math
import pprint
import random
from copy import copy
from typing import List, Tuple

import MinMax
from GameNode import GameNode,make_decision_tree, pprint_tree, mancala_function, is_finished
from Player import Player
from Components import Stone, Hole, Mancala
from itertools import cycle

# COLORS = ["blue", "red", "yellow", "green", "white", "black"]
COLORS = ["b", "r", "y", "g", "w", "bl"]


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

        stones = copy(hole.stones)
        hole.stones.clear()
        while len(stones) != 0:
            stone = stones[0]
            stones.remove(stone)
            hole = self.get_next_hole(hole)
            was_empty = len(hole.stones) == 0
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
        hole.stones.clear()
        opposite_hole.stones.clear()

    def set_turn(self, player_id=None):
        if player_id is None:
            return random.choice(list(self.players.keys()))
        else:
            return player_id

    def get_players(self, how_many=2):
        player1 = Player(0)
        player2 = Player(1)
        if how_many == 2:
            print("1st player!")
            name1 = input("Please type your name: ")
            player1.name = name1
            print(f"Hi, {name1}!")
            type1 = input(f"Are you a human, {name1}?: 'YES'/'NO' ->")
            player1.type = "Human" if type1 == "YES" else "AI"
            if player1.type == "AI":
                player1.name += " (AI)"

            print("2nd player!")
            name2 = input("Please type your name: ")
            player2.name = name2
            print(f"Hi, {name2}!")
            type2 = input(f"Are you a human, {name2}?: 'YES'/'NO' ->")
            player2.type = "Human" if type2 == "YES" else "AI"
            if player2.type == "AI":
                player2.name += " (AI)"
        print("Players created!")
        return player1, player2

    def get_opposite_hole(self, hole):
        return self.holes[14 - self.global_hole_number(hole)]

    def get_player_move(self):
        player_on_turn = self.players[self.turn]
        print(f"{player_on_turn.name}'s move!")
        hole = int(input("I pick hole number:"))
        if hole in range(2 * (self.holes_in_row + 1)):
            return hole
        else:
            return 0

    def calculate_result(self):
        print("Leaderboard")
        for player_id, player in self.players.items():
            player.points = len(self.get_mancala(player_id).stones)
            print(player)

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
        elif mode == "numbers":  # 23
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
            print("", end=" -> ")
            for hole_num, hole in sorted(
                    [(hole_num, hole) for (hole_num, hole) in self.holes.items() if hole_num in range(1, 8)],
                    key=lambda h: h[0], reverse=False):
                print("{}".format(f"({hole.count()})"), end=" -> ")
            print()
            print("", end="    ")
            for hole_num in range(1, 7):
                print(" {} ".format(hole_num), end="    ")
            print(" M ".format(), end="    ")
            print()
            print("\n{:^52}\n".format(f"{self.players[0].name}: {self.get_points(0)}"))

    def finish_game(self):
        for player_id, player in self.players.items():
            mancala = self.get_mancala(player_id)
            for hole in self.holes.values():
                if hole.player.id == player_id and not isinstance(hole, Mancala):
                    mancala.stones.extend(hole.stones)
                    hole.stones.clear()

            player.points = len(mancala.stones)

    def is_finished(self):
        return len([True for hole in self.holes.values() if
                    hole.player.id == self.turn and not isinstance(hole, Mancala) and len(hole.stones) > 0]) == 0

    def start_game(self):
        players = self.get_players(2)
        self.initialize_game(players)
        self.set_turn(0)
        next_best_move = 0
        DEPTH = 4
        # Game itself
        while not self.is_finished():
            self.print_game_state("numbers")

            self.calculate_result()

            move_done = False
            hole_number = next_best_move
            while not move_done:
                if self.players[self.turn].type == "Human":
                    hole_number = self.get_player_move()
                    print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")
                    while hole_number == 0:
                        print("Enter correct number!")
                        hole_number = self.get_player_move()

                    move_done = self.move(self.turn, hole_number)
                    if not move_done:
                        print("Illegal move!")
                elif self.players[self.turn].type == "AI":
                    if hole_number != 0:
                        move_done = self.move(self.turn, hole_number)
                        print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")
                    else:
                        print("Random AI move")
                        hole_number = random.choice(list(self.get_possible_moves(self.turn)))
                        move_done = self.move(self.turn, hole_number)
                        print(f"{self.players[self.turn].name} picked hole no.{hole_number}!")

            print("MOVE DONE")
            if not self.additional_move:
                self.change_turn()
            self.additional_move = False

            root = GameNode(self, hole_number, self.turn)
            make_decision_tree(root, DEPTH)

            MinMax.minmax(root, DEPTH, -math.inf, math.inf, mancala_function, is_finished, root.player_id)
            if len(root.children) > 0:
                for child in root.children:
                    print("v:", child.number, child.value)
                next_best_move = max(root.children, key=lambda n: n.value).number
                #next_best_move = sorted(root.children, key=lambda n: n.value, reverse=True)[0].number
                print("Next best move:", next_best_move)
            #pprint_tree(root)

        # Game finished
        self.finish_game()
        self.print_game_state()
        self.calculate_result()
        print("All moves:")
        pprint.pprint(self.moves_table)