"""
Tic Tac Toe Player

Original code by the amazing faculty of CS 50's intro to AI with Python.
Other stuff is stuff by KS

June, 2020.

"""

import util
import math

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
    count = 0
    for item in board:
        for i in range(len(item)):
            if item[i] == X:
                count += 1
            elif item[i] == O:
                count -= 1
            else:
                continue
    if count == 0:
        return (X)
    if count != 0:
        return (O)

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = []
    for i in range (len(board)):
        for j in range (3):
            if board[i][j] is EMPTY:
                actions.append((i, j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    mark = player(board)
    newboard = []
    for row in board:
        list = []
        for item in row:
            list.append(item)
        newboard.append(list)
    i = action [0]
    j = action [1]
    if newboard[i][j] is not EMPTY:
        raise Exception ('Action not valid.')
    else:
        newboard[i][j] = mark
    return newboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #check if X wins by row.
    for i in range (3):
        if board[i][0] == X and board[i][1] == X and board[i][2] == X:
            return X
    #check for X win by column
    for j in range (3):
        if board [0][j] == X and board [1][j] == X and board [2][j] == X:
            return X
    #check for win by diaganol
    if board [0][0] == X and board [1][1] == X and board [2][2] == X:
        return X
    if board [0][2] == X and board [1][1] == X and board [2][0] == X:
        return X

    #check if O wins by row.
    for i in range (3):
        if board[i][0] == O and board[i][1] == O and board[i][2] == O:
            return O
    #check for O win by column
    for j in range (3):
        if board [0][j] == O and board [1][j] == O and board [2][j] == O:
            return O
    #check for win by diaganol
    if board [0][0] == O and board [1][1] == O and board [2][2] == O:
        return O
    if board [0][2] == O and board [1][1] == O and board [2][0] == O:
        return O

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    terminal = winner(board)
    if terminal == None:
        return False
    else:
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    utility = winner (board)

    if utility == X:
        return 1
    if utility == O:
        return -1
    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def maxi(board):
        #print ('Max called.')
        if terminal(board):
            # print (board)
            # print (utility(board))
            return utility(board)
        v = -100
        moves = actions(board)
        for move in moves:
            v = max(v, mini(result(board, move)))
        print (f'V = {v}')
        return v

    def mini(board):
        # print ('Min called.')
        if terminal(board):
            # print (board)
            # print(utility(board))
            return utility(board)
        v = 100
        moves = actions(board)
        for move in moves:
            v = max(v, maxi(result(board, move)))
        # print(f'V = {v}')
        return v

    if player(board) == X:
        maxi (board)

    if player(board) == O:
        mini (board)

