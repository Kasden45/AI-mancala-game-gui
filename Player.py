class Player:
    def __init__(self, player_id=0, name=""):
        self.id = player_id
        self.points = 0
        self.name = name
        self.type = "Human"  # AI

    def __str__(self):
        return f"Id: {self.id} -- Name: {self.name} -- Points: {self.points}"
