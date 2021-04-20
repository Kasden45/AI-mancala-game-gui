class Stone:
    def __init__(self, color):
        self.color = color


class Hole:
    def __init__(self, number, stones, player):
        self.stones = stones
        self.number = number
        self.player = player


class Mancala(Hole):
    def __init__(self, stones, player):
        super().__init__(0, stones, player)

    def points(self):
        return len(self.stones)