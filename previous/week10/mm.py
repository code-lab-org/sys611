# -*- coding: utf-8 -*-
"""
SYS-611: M&M Jar Model

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

# import the scipy stats package and refer to it as `stats`
# see http://docs.scipy.org/doc/scipy/reference/stats.html for documentation
import scipy.stats as stats

NUM_RUNS = 10000
NUM_OPPONENTS = 50

#%% Monte Carlo simulation for number of M&Ms

# set the random number generator seed
np.random.seed(0)

# define a process generator for number of M&Ms in the jar
def generate_N(size=1):
    # sample the jar volume
    V = np.random.triangular(1890*.98, 1890, 1890*1.02, size)
    # sample the packing factor
    mu = np.random.triangular(0.55*0.8, 0.55, 0.55*1.2, size)
    # sample the average M&M diameter
    d = np.random.triangular(1.4*0.9, 1.4, 1.4*1.1, size)
    # sample the average M&M thickness
    t = np.random.triangular(0.6*0.9, 0.6, 0.6*1.1, size)
    # sample and return the derived number of M&Ms in the jar
    N = 6*V*mu/(np.pi*d**2*t)
    return N.astype(int)

# generate NUM_RUNS samples
N = generate_N(NUM_RUNS)

# create a histogram to visualize results
plt.figure()
plt.hist(N,color='r')
plt.xlabel('Number of M&Ms in Jar')
plt.ylabel('Frequency')

# print descriptive statistics
print('N_bar = {:.0f}'.format(np.mean(N)))
print('5th percentile = {:.0f}'.format(np.percentile(N,5)))
print('95th percentile = {:.0f}'.format(np.percentile(N,95)))

#%% Monte Carlo simulation for probability of winning (simple)

# define the space of alternatives
x = np.arange(0,2500,5)
# define the outcomes (number of wins)
w = np.zeros(np.size(x))

# iterate over each run
for run in range(NUM_RUNS):
    # set the random number generator seed
    np.random.seed(run)
    # generate a true number of M&Ms
    N_star = generate_N()
    # sample the opponents' guesses from a triangular distribution
    y = np.random.triangular(500, 1600, 2500, NUM_OPPONENTS)
    
    if np.sum(y[y<=N_star]) > 0:
        # if at least one opponent has a winning choice
        # a winning alternative must be <= the true number of M&Ms
        # and >= the best opponent's guess
        winners = np.logical_and(x<=N_star, x>=np.max(y[y<=N_star]))
    else:
        # otherwise a winning alternative must be <= the true number of M&Ms
        winners = x<=N_star
    
    # if any alternative is a winner, record the outcomes
    if np.any(winners):
        w[winners] += 1

# plot a distribution of the probability of an alternative winning
plt.figure()
plt.plot(x,w/NUM_RUNS,'-r')
plt.xlabel('Guess of Number of M&Ms in Jar')
plt.ylabel('Probability of Winning')