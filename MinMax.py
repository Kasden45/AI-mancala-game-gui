import math


def minmax(node, depth, alfa, beta, evaluation, end_game, maxing_player_id, is_max=True, is_alfa_beta=True):
    print("player: ", maxing_player_id, "alfabeta? ", is_alfa_beta)
    """
    (* Initial call *)
    minmax(root, depth, −inf, +inf, evaluation, end_game, True)
    :param maxing_player_id: starting player id
    :param node: current node (root at the beginning)
    :param depth: remaining depth
    :param alfa: alfa value
    :param beta: beta value
    :param evaluation: evaluation function with game as argument
    :param end_game: function answering if the game is finished in given state
    :param is_max: flag -> True: maximize, False: minimize
    :param is_alfa_beta:
    :return:
    """
    if depth == 0 or end_game(node) == True or len(node.children) == 0:
        node.value = evaluation(node, maxing_player_id)
        return node.value

    if is_max:
        value = -math.inf
        max_value = -math.inf
        for child in node.children:
            value = max(value, minmax(child, depth - 1 if node.game_state.turn != child.game_state.turn else depth, alfa, beta, evaluation, end_game, maxing_player_id, maxing_player_id == child.player_id, is_alfa_beta))
            max_value = max(max_value, value)
            if is_alfa_beta:
                alfa = max(alfa, value)
                if alfa >= beta:
                    break
        node.value = max_value
        return value

    else:
        value = math.inf
        min_value = math.inf
        for child in node.children:
            value = min(value, minmax(child, depth - 1 if node.game_state.turn != child.game_state.turn else depth, alfa, beta, evaluation, end_game, maxing_player_id, maxing_player_id == child.player_id, is_alfa_beta))
            min_value = min(min_value, value)
            if is_alfa_beta:
                beta = min(beta, value)
                if alfa >= beta:
                    break
        node.value = min_value
        return value
