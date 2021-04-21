from typing import List

from Player import Player


class Stone:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return str(self.color)


class Hole:
    def __init__(self, number, stones, player):
        self.stones: List[Stone] = stones
        self.number: int = number
        self.player: Player = player

    def add_stone(self, stone):
        self.stones.append(stone)

    def __str__(self):
        return str([str(stone) for stone in self.stones])


class Mancala(Hole):
    def __init__(self, stones, player):
        super().__init__(7, stones, player)

    def points(self):
        return len(self.stones)

    def __str__(self):
        return f"[[ {str([str(stone) for stone in self.stones])} ]]"