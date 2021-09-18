# -*- coding: utf-8 -*-
"""
SYS-611: Tic-Tac-Toe Example

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the pandas library and refer to it as `pd`
import pandas as pd

# define the game state as a list of lists with 3x3 grid cells
# initialize the cells to a blank space character
state = [
    [" "," "," "],
    [" "," "," "],
    [" "," "," "]
]

# define a function to check if a mark is valid
def is_valid(row, col):
    # check if the row/column is empty
    return state[row][col] == " "

# define a function to mark an 'x' at a row and column
def mark_x(row, col):
    # check if this is a valid move
    if is_valid(row, col):
        # if valid, update the state accordingly
        state[row][col] = "x"

# define a function to mark an 'o' at a row and column
def mark_o(row, col):
    # check if this is a valid move
    if is_valid(row, col):
        # if valid, update the state accordingly
        state[row][col] = "o"

# define a function to print out the grid to the console
def show_grid():
    # use the pandas dataframe to help format the matrix
    print(pd.DataFrame(state))

# define a function to clear out the game state
def reset_game():
    # iterate over values in 0, 1, 2
    for i in range(3):
        # iterate over values in 0, 1, 2
        for j in range(3):
            # empty this state location at (i,j)
            state[i][j] = " "
    
def get_winner():
    pass # replace this line for HW-01

def is_tie():
    pass # replace this line for HW-01

#%% example game sequence

mark_x(1, 1)
show_grid()

mark_o(0, 2)
show_grid()

mark_x(0, 0)
show_grid()

mark_o(2, 2)
show_grid()

reset_game()
show_grid()