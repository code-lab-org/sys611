# -*- coding: utf-8 -*-
"""
SYS-611: Dice Fighters Example

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy library and refer to it as `np`
import numpy as np

# define the round_number state variable, initialize to 0
round_number = 0
# define the red_size state variable, initialize to 20
red_size = 20
# define the blue_size state variable, initialize to 10
blue_size = 10
# define the red_chance_hit state variable, initialize to 1/6 
red_chance_hit = 1/6
# define the blue_chance_hit state variable, initialize to 3/6 
blue_chance_hit = 3/6

# define the generate_red_hits function
def generate_red_hits():
    # roll random (0,1) numbers for each dice
    attacks = np.random.rand(red_size)
    # count the number of rolls which are lower than red_chance_hit
    num_hits = sum(attacks < red_chance_hit)
    # return the number of hits
    return num_hits

# define the generate_blue_hits function
def generate_blue_hits():
    # roll random (0,1) numbers for each dice
    attacks = np.random.rand(blue_size)
    # count the number of rolls which are lower than the blue_chance_hit
    num_hits = sum(attacks < blue_chance_hit)
    # return the number of hits
    return num_hits

# define the red_suffer_losses function with an argument for the number of opponent hits
def red_suffer_losses(opponent_hits):
    # (note: red_size must be declared as a global variable to update!)
    global red_size
    # update the red_size based on the number of opponent hits
    red_size -= opponent_hits

# define the blue_suffer_losses function with an argument for number of opponent hits
def blue_suffer_losses(opponent_hits):
    # (note: blue_size must be declared as a global variable to update!)
    global blue_size
    # update the blue_size based on number of opponent hits
    blue_size -= opponent_hits

# define the is_complete function
def is_complete():
    # return True if either red_size or blue_size is less than or equal to zero
    return (red_size <= 0 or blue_size <= 0)

# define the next_round state change function
def next_round():
    # (note: round_number must be declared as a global variable to update!)
    global round_number
    # advance the round_number
    round_number += 1

# main execution loop: continue while the game is not complete
while not is_complete():
    # generate the number of red hits
    red_hits = generate_red_hits()
    # generate the number of blue hits
    blue_hits = generate_blue_hits()
    # red team suffers losses of blue hits
    red_suffer_losses(blue_hits)
    # blue team suffers losses of red hits
    blue_suffer_losses(red_hits)
    # advance to the next round
    next_round()
    # print out the current state for debugging
    print("Round {}: {} Red, {} Blue".format(
            round_number, 
            red_size,
            blue_size
        ))

# after main loop exists, check who won (whichever team still has fighters!)
if red_size > 0:
	print("Red Wins")
elif blue_size > 0:
	print("Blue Wins")
else:
	print("Tie - Mutual Destruction!")
