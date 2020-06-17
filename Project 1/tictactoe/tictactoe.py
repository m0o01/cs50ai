"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x, o = 0, 0
    # Count each time player has played
    for row in board:
        for tile in row:
            if tile == X:
                x += 1
            elif tile == O:
                o += 1
    # Player X starts first
    if x == o:
        return X
    else:
        return O    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            # Add the action if the tile was vacant
            if(board[i][j] == EMPTY):
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Copy new board
    new_board = copy.deepcopy(board)
    # Check current turn
    turn = player(board)
    # Get coords from action
    row, column = action[0], action[1]
    # Only apply the action is the tile was empty
    if new_board[row][column] == EMPTY:
        new_board[row][column] = turn
    else:
        raise Exception("Tile is already taken.")
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        # Check players alternately
        for player in [X, O]:
            # Check for horizontal match
            if board[i][0] == player and board[i][1] == player and board[i][2] == player:
                return player
            # Check for vertical match
            if board[0][i] == player and board[1][i] == player and board[2][i] == player:
                return player
    
    for i in [X, O]:
        # Check for diagonal match
        if board[0][0] == i and board[1][1] == i and board[2][2] == i:
            return i 
        # Check for reverse diagonal match
        if board[0][2] == i and board[1][1] == i and board[2][0] == i:
            return i

    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there's a winner, the game is terminal
    if winner(board):
        return True
    for i in range(3):
        for j in range(3):
            # If there's an empty tile, the game in progress
            if board[i][j] == EMPTY:
                return False
    # No winners
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Check for winner
    winner_player = winner(board)

    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0
    
def max_value(state):
    if terminal(state):
        return utility(state)
    value = -1
    for action in actions(state):
        value = max(value, min_value(result(state, action)))
    return value

def min_value(state):
    if terminal(state):
        return utility(state)
    value = 1
    for action in actions(state):
        value = min(value, max_value(result(state, action)))
    return value

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    desired_outcome = 1

    current_player = player(board)

    if current_player == O:
        desired_outcome = -1

    opponent_actions = []

    for action in actions(board):
        if desired_outcome == 1:
            value = min_value(result(board, action))
            opponent_actions.append((value, action))
        else:
            value = max_value(result(board, action))
            opponent_actions.append((value, action))

    if desired_outcome == 1:
        return max(opponent_actions)[1]
    else:
        return min(opponent_actions)[1]