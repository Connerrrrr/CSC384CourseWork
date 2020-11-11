"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

cache = {}


def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


# Method to compute utility value of terminal state
def compute_utility(board, color):
    score = get_score(board)
    if color == 1:
        return score[0] - score[1]
    else:
        return score[1] - score[0]


# Better heuristic value of board
def compute_heuristic(board, color):  # not implemented, optional
    # IMPLEMENT
    return 0  # change this!


# TODO: Comments needed
def ordered_moves(board, moves, color, current_player):
    '''This is for ordering possible moves'''
    dic = dict()
    result = []
    for move in moves:
        (column, row) = move
        new_board = play_move(board, current_player, column, row)
        successor_utility = compute_utility(new_board, color)
        if successor_utility in dic and dic[successor_utility] != [move]:
            dic[successor_utility].append(move)
        else:
            dic[successor_utility] = [move]
    ordered_utility = sorted(list(dic.keys()), reverse=True)
    for utility in ordered_utility:
        result += dic[utility]
    return result


############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching=0):
    # Get the opponent
    if color == 1:
        opponent = 2
    else:
        opponent = 1
    # Check cache
    if caching and board in cache:
        return cache[board]
    best_move = None
    possible_moves = get_possible_moves(board, opponent)
    if len(possible_moves) == 0 or limit == 0:
        # fixed utility in the end
        return None, compute_utility(board, color)

    minUtility = float('inf')
    for move in possible_moves:
        # Get the new board
        (column, row) = move
        new_board = play_move(board, opponent, column, row)

        # Compute utility
        _, utility = minimax_max_node(new_board, color, limit - 1, caching)
        # Cache then new board
        if caching:
            cache[new_board] = (move, utility)
        if utility < minUtility:
            best_move = move
            minUtility = utility
    return best_move, minUtility


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    # Check cache
    if caching and board in cache:
        return cache[board]
    best_move = None
    possible_moves = get_possible_moves(board, color)

    if len(possible_moves) == 0 or limit == 0:
        # fixed utility in the end
        return None, compute_utility(board, color)

    maxUtility = -float('inf')
    for move in possible_moves:
        # Get the new board
        (column, row) = move
        new_board = play_move(board, color, column, row)

        # Compute utility
        _, utility = minimax_min_node(new_board, color, limit - 1, caching)
        # Cache then new board
        if caching:
            cache[new_board] = (move, utility)
        if utility > maxUtility:
            best_move = move
            maxUtility = utility
    return best_move, maxUtility


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """
    # IMPLEMENT
    cache.clear()
    best_move, best_utility = minimax_max_node(board, color, limit, caching)
    return best_move


############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # Get the opponent
    if color == 1:
        opponent = 2
    else:
        opponent = 1
    # Check cache
    if caching and board in cache:
        return cache[board]
    best_move = None
    possible_moves = get_possible_moves(board, opponent)
    if len(possible_moves) == 0 or limit == 0:
        # fixed utility in the end
        return None, compute_utility(board, color)

    minUtility = float('inf')
    for move in possible_moves:
        # Get the new board
        (column, row) = move
        new_board = play_move(board, opponent, column, row)

        # Compute utility
        _, utility = alphabeta_max_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        # Cache then new board
        if caching:
            cache[new_board] = (move, utility)
        if utility < minUtility:
            best_move = move
            minUtility = utility
        # Conducting alpha-beta pruning
        beta = min(beta, utility)
        if beta <= alpha:
            break
    return best_move, minUtility


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # Check cache
    if caching and board in cache:
        return cache[board]
    best_move = None
    possible_moves = get_possible_moves(board, color)

    if len(possible_moves) == 0 or limit == 0:
        # fixed utility in the end
        return None, compute_utility(board, color)

    maxUtility = -float('inf')
    if ordering:
        possible_moves = ordered_moves(board, possible_moves, color, color)
    for move in possible_moves:
        # Get the new board
        (column, row) = move
        new_board = play_move(board, color, column, row)

        # Compute utility
        _, utility = alphabeta_min_node(new_board, color, alpha, beta, limit - 1, caching, ordering)
        # Cache then new board
        if caching:
            cache[new_board] = (move, utility)
        if utility > maxUtility:
            best_move = move
            maxUtility = utility
        # Conducting alpha-beta pruning
        alpha = max(alpha, utility)
        if beta <= alpha:
            break
    return best_move, maxUtility


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    # IMPLEMENT
    cache.clear()
    best_move, best_utility  = alphabeta_max_node(board, color, -float('inf'), float('inf'), limit, caching, ordering)
    return best_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI")  # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0])  # Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if minimax == 1:
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if caching == 1:
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if ordering == 1:
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if limit == -1:
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if minimax == 1 and ordering == 1: eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            board = eval(input())  # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if minimax == 1:  # run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
