from GameNode import heuristic_stones_far_from_mancala, heuristic_steal, heuristic_most_points, heuristic_points_diff


class Player:
    def __init__(self, player_id=0, name=""):
        self.id = player_id
        self.points = 0
        self.name = name
        self.type = "Human"  # AI
        self.AI_mode = "minmax"
        self.computing_time = 0
        self.heuristic = None
        self.stolen_stones = 0
    def __str__(self):
        return f"Id: {self.id} -- Name: {self.name} -- Points: {self.points} {self.AI_mode if self.type == 'AI' else ''}"

    def heuristic_name(self):
        if self.heuristic == heuristic_points_diff:
            return "Points diff"
        elif self.heuristic == heuristic_steal:
            return "Steal"
        elif self.heuristic == heuristic_stones_far_from_mancala:
            return "Far from mancala"
        elif self.heuristic == heuristic_most_points:
            return "Most points"
        else:
            return None
