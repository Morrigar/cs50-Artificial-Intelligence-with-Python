
X = "X"
O = "O"
EMPTY = None

boardwon1 = [[X,X,X],
            [O,X,EMPTY],
            [O,O,EMPTY]]

boardwon2 = [[X,X,EMPTY],
            [O,X,EMPTY],
            [O,O,X]]

tboard1 = [[X,O,X],
            [EMPTY,O,EMPTY],
            [O,EMPTY,X]]

tboard2 = [[X, EMPTY ,X ],
           [EMPTY, O, EMPTY],
           [EMPTY, EMPTY, EMPTY]]

def pboard(board):
    for item in board:
        print (item)

