import math
import copy

X = "X"
O = "O"

EMPTY = None

def initial_start():
    return[[EMPTY, EMPTY, EMPTY],
           [EMPTY, EMPTY, EMPTY],
           [EMPTY, EMPTY, EMPTY]]

def player(board):
    count_x = 0
    count_o = 0
    for i in board:
        for j in i:
            if j == "X":
                count_x += 1
            elif j == "O":
                count_o += 1
    if count_x == count_o:
        return "X"
    else:
        return "O"

def actions(board):
    moves_available = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves_available.add((i,j))
    return moves_available

def result(board, action):
    if action not in actions(board):
        raise ValueError("Action Impossible")
    row, col = action
    current_player = player(board)
    new_board = [row[:] for row in board]
    new_board[row][col] = current_player

    return new_board

def winner(board):
    for player in [X, O]:
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return player
            if all(board[j][i] == player for j in range(3)):
                return player
        if all(board[i][i] == player for i in range(3)):
            return player
        if all(board[i][2 - i] == player for i in range(3)):
            return player
    return None

def terminal(board):
    return winner(board) is not None or all(board[i][j] != EMPTY for i in range(3) for j in range(3))

def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def min_value(board):
    if terminal(board):
        return utility(board), None

    f = float("inf")
    optimal_action = None
    for action in actions(board):
        max_val, _ = max_value(result(board, action))
        if max_val < f:
            f = max_val
            optimal_action = action
    return f, optimal_action

def max_value(board):
    if terminal(board):
        return utility(board), None

    f = float("-inf")
    optimal_action = None
    for action in actions(board):
        min_val, _ = min_value(result(board, action))
        if min_val > f:
            f = min_val
            optimal_action = action

    return f, optimal_action

def minimax(board):
    if terminal(board):
        return None
    if player(board) == X:
        value, action = max_value(board)
    else:
        value, action = min_value(board)

    return action