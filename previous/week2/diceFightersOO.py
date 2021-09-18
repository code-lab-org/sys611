# -*- coding: utf-8 -*-
"""
SYS-611: Object-oriented Dice Fighters Example

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy library and refer to it as `np`
import numpy as np

# define a class to model each team
class Team:
    # define an initialization function
    def __init__(self, size, chance_hit):
        self.size = size
        self.chance_hit = chance_hit
    # define the generate_hits function
    def generate_hits(self):
        # roll random (0,1) numbers for each dice
        attacks = np.random.rand(self.size)
        # count the number of rolls which are lower than chance_hit
        num_hits = sum(attacks < self.chance_hit)
        # return the number of hits
        return num_hits
    # define the suffer_losses function with an argument for the number of opponent hits
    def suffer_losses(self, opponent_hits):
        # update the red_size based on the number of opponent hits
        self.size -= opponent_hits

# define the round_number state variable, initialize to 0
round_number = 0
# define the red Team with size 20 and hit chance 1/6
red = Team(20, 1/6)
# define the blue team with size 10 and hit chance 3/6
blue = Team(10, 3/6)

# define the is_complete function
def is_complete():
    # return True if either red_size or blue_size is less than or equal to zero
    return (red.size <= 0 or blue.size <= 0)

# define the next_round state change function
def next_round():
    # (note: round_number must be declared as a global variable to update!)
    global round_number
    # advance the round_number
    round_number += 1

# main execution loop: continue while the game is not complete
while not is_complete():
    # generate the number of red hits
    red_hits = red.generate_hits()
    # generate the number of blue hits
    blue_hits = blue.generate_hits()
    # red team suffers losses of blue hits
    red.suffer_losses(blue_hits)
    # blue team suffers losses of red hits
    blue.suffer_losses(red_hits)
    # advance to the next round
    next_round()
    # print out the current state for debugging
    print("Round {}: {} Red, {} Blue".format(
            round_number, 
            red.size,
            blue.size
        ))

# after main loop exists, check who won (whichever team still has fighters!)
if red.size > 0:
	print("Red Wins")
elif blue.size > 0:
	print("Blue Wins")
else:
	print("Tie - Mutual Destruction!")
