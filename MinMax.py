import math


def minmax(node, depth, alfa, beta, evaluation, end_game, root_player_id, is_max=True, is_alfa_beta=True):
    """
    (* Initial call *)
    minmax(root, depth, −inf, +inf, evaluation, end_game, True)
    :param root_player_id: starting player id
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
    if depth == 0 or end_game(node) == True:
        return evaluation(node)

    if is_max:
        value = -math.inf
        for child in node.children:
            value = max(value, minmax(child, depth - 1, alfa, beta, evaluation, end_game, root_player_id, root_player_id == child.player_id, is_alfa_beta))
            if is_alfa_beta:
                alfa = max(alfa, value)
                if alfa >= beta:
                    break
        return value

    else:
        value = math.inf
        for child in node.children:
            value = min(value, minmax(child, depth - 1, alfa, beta, evaluation, end_game, root_player_id, root_player_id == child.player_id, is_alfa_beta))
            if is_alfa_beta:
                beta = min(beta, value)
                if alfa >= beta:
                    break
        return value
