# -*- coding: utf-8 -*-
"""
SYS-611: Dice Fighters Monte Carlo Simulation Example

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

# import the scipy stats package and refer to it as `stats`
# see http://docs.scipy.org/doc/scipy/reference/stats.html for documentation
import scipy.stats as stats

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# define the red_chance_hit state variable, initialize to 1/6 
red_chance_hit = 1/6
# define the blue_chance_hit state variable, initialize to 3/6
blue_chance_hit = 3/6
    
# define the generate_red_hits function
def generate_red_hits():
    return np.random.binomial(red_size, red_chance_hit)

# define the generate_blue_hits function
def generate_blue_hits():
    return np.random.binomial(blue_size, blue_chance_hit)

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
    

def gen_battle():
    global round_number, red_size, blue_size
    # define the round_number state variable, initialize to 0
    round_number = 0
    # define the red_size state variable, initialize to 20
    red_size = 20
    # define the blue_size state variable, initialize to 10
    blue_size = 10
    
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
    
    # after main loop exists, check who won (whichever team still has fighters!)
    if red_size > 0:
        	return 'red'
    elif blue_size > 0:
        	return 'blue'
    else:
        	return 'tie'

# seed the random number generator for consistent results
np.random.seed(0)

# generate samples and store in a numpy array
samples = np.array([gen_battle() for i in range(10000)])

# compute the lower and upper-bounds using a 95% confidence interval
confidence_level = 0.05
z_crit = stats.norm.ppf(1-confidence_level/2)

# compute running statistics for mean and confidence interval
win_red_mean = np.array([np.average(samples[0:i]=='red') for i in range(len(samples))])
win_red_ci = z_crit*np.array([stats.sem(samples[0:i]=='red') for i in range(len(samples))])

# create a plot to show the mean estimate with 95% confidence interval bounds
plt.figure()
plt.plot(range(len(samples)), win_red_mean, 
         'b', label='Mean Estimate')
plt.plot(range(len(samples)), win_red_mean-win_red_ci, 
         'g', label='95% CI Lower Bound')
plt.plot(range(len(samples)), win_red_mean+win_red_ci, 
         'r', label='95% CI Upper Bound')
plt.xlabel('Sample')
plt.ylabel('Estimate of $P(W=red)$')
plt.legend(loc='best')

# just for fun, compute the 95% confidence interval for tie games
print('P(W=tie) = {:.3f} +/- {:.3f} (95% CI)'.format(
        np.average(samples=='tie'),
        z_crit*stats.sem(samples=='tie')
    ))