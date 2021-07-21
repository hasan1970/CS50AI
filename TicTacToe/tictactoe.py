"""
Tic Tac Toe Player
"""

import math
import numpy as np
import copy #for deepcopy
import sys  #for positive and negative infinity

X = "X"
O = "O"
EMPTY = str('  ')


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
    
       
    xcount=ocount=0  
    for i in range(3):
        for j in range(3):
            if board[i][j]==X:
                xcount+=1
            elif board[i][j]==O:
                ocount+=1

    if xcount>ocount:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
   
    list1=[]
    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                list1.append((i,j))
                
    return set(list1)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    a=action[0]
    b=action[1]
    if board[a][b]!=EMPTY:
        raise Exception("INVALID")
    turn=player(board)
    NewBoard= copy.deepcopy(board)
    NewBoard[a][b]=turn
    return NewBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #Diagonal
    if (board[0][0]==board[1][1]==board[2][2]) or (board[0][2]==board[1][1]==board[2][0]) and board[1][1]!=EMPTY :
        return board[1][1]
        
    
    for i in range(3):
        if (board[i][0]==board[i][1]==board[i][2]) and board[i][0]!=EMPTY:
            return board[i][0]
        if (board[0][i]==board[1][i]==board[2][i]) and board[0][i]!=EMPTY:
            return board[0][i]

    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Variable for count of Empty spaces
    ecount=0    
    if winner(board)!=None:
        return True


    for i in range(3):
        for j in range(3):
            if board[i][j]==EMPTY:
                ecount+=1
    if ecount==0:
        return True
    else:
        return False



    
        


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    check=winner(board)
    if check==X:
        return 1
    elif check==O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    playernow=player(board)
    if playernow==X:
        return Maximum(board)[1]
    else:
        return Minimum(board)[1]
        

def Maximum(board):
    if terminal(board):
        return (utility(board), None)

    v = -sys.maxsize - 1    #getting negative infinity
    optAction = None
    for action in actions(board):
        Result1 = Minimum(result(board, action))
        if Result1[0] > v: #checking if its max
            optAction = action
            v = Result1[0]
        

        if v == 1:
            break

    return (v, optAction)


def Minimum(board):
    if terminal(board):
        return (utility(board), None)



    v = sys.maxsize #positive infinity
    optAction = None
    for action in actions(board):
        Result1 = Maximum(result(board, action))
        if Result1[0] < v: #checking if its min
           
            optAction = action
            v = Result1[0]
        

       
        if v == -1: #utiiity check
            break

    return (v, optAction)

