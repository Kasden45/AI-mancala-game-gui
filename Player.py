class Player:
    def __init__(self, player_id=0, name=""):
        self.id = player_id
        self.points = 0
        self.name = name
        self.type = "Human"  # AI
        self.AI_mode = "minmax"
        self.computing_time = 0

    def __str__(self):
        return f"Id: {self.id} -- Name: {self.name} -- Points: {self.points} {self.AI_mode if self.type == 'AI' else ''}"
