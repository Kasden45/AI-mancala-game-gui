from copy import deepcopy

from Components import Mancala
from MinMax import minmax
import pickle


class GameNode:
    def __init__(self, game, number, player_id):
        self.number = number
        self.player_id = player_id
        self.game_state = game
        self.children = []  # number : node
        self.value = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def players_turn(self, player_id):
        return self.player_id == player_id


def is_finished(game_node):
    game = game_node.game_state
    return len([True for hole in game.holes.values() if
                hole.player.id == game.turn and not isinstance(hole, Mancala) and len(hole.stones) > 0]) == 0


def mancala_function(node: GameNode, player_id):
    game = node.game_state
    #print("From ",player_id)
    #game.print_game_state()
    score = game.get_points(player_id) - game.get_points(game.get_opponent_id(player_id))
    #print("Score", score)
    return score


def pprint_tree(node, file=None, _prefix="", _last=True):
    print(_prefix, "`- " if _last else "|- ", f"{node.number}:{node.value} -> next:{node.player_id} ", sep="", file=file)
    _prefix += "   " if _last else "|  "
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        _last = i == (child_count - 1)
        pprint_tree(child, file, _prefix, _last)


def make_decision_tree(node: GameNode, depth):
    if depth == 0:
        return
    #print("Number", node.number, "Depth:", depth, "Turn:", node.game_state.turn)
    for choice in node.game_state.get_possible_moves(node.player_id):
        new_game_state = pickle.loads(pickle.dumps(node.game_state))
        # deepcopy(node.game_state)
        new_game_state.move(node.player_id, choice)
        if not new_game_state.additional_move:
            new_game_state.change_turn()
        new_game_state.additional_move = False
        child = GameNode(new_game_state, choice, new_game_state.turn)
        node.add_child(child)
        make_decision_tree(child, depth - 1 if node.game_state.turn != new_game_state.turn else depth)
