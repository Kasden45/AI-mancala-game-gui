from typing import List

import Player
from Components import Stone, Hole, Mancala
from itertools import cycle

COLORS = ["blue", "red", "yellow", "green", "white", "black"]

class Game:
    def __init__(self):
        self.turn = 0
        self.holes = None # cyclic
        self.stones = []
        self.number_of_stones = 4
        self.holes_in_row = 6
        self.players = {}

    def initialize_game(self, players : List[Player]):
        self.players[players[0].id] = players[0]
        self.players[players[1].id] = players[1]

        holes = []
        for player in self.players.values():
            for hole_number in range(self.holes_in_row):
                stones = []
                for stone_number in range(self.number_of_stones):
                    stones.append(Stone(COLORS[stone_number])) # Stones have colors assigned
                holes.append(Hole(hole_number, stones, player.id))
            holes.append(Mancala([],player.id)) # Mancala is empty
        self.holes = cycle(holes)

    def move(self, player, hole):
        pass

    def get_opposite_hole(self, player, hole):
        pass

def start_game():
