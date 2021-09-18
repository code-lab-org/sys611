# -*- coding: utf-8 -*-
"""
SYS-611: Example Markov Process Generator

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np
# import the matplotlib.pyplot package and refer to it as `plt`
import matplotlib.pyplot as plt

# define the state transition function
def next_state(q):
    r = np.random.rand()
    # if it is a clear day
    if q == 0:
        if r < 186/250:
            # another clear day
            return 0
        elif r < (186+47)/250:
            # a rainy day next
            return 1
        else:
            # a snowy day next
            return 2
    # if it is a rainy day
    elif q == 1:
        if r < 47/89:
            # a clear day next
            return 0
        elif r < (47+40)/89:
            # another rainy day
            return 1
        else:
            # a snowy day next
            return 2
    # if it is a snowy day
    else:
        if r < 16/25:
            # a clear day next
            return 0
        elif r < (16+3)/25:
            # a rainy day next
            return 1
        else:
            # another snowy day
            return 2

# define the number of samples and create a state trajectory
num_samples = 100
np.random.seed(0)
q = np.zeros(num_samples)
# perform all the state transitions
for t in range(num_samples - 1):
    q[t+1] = next_state(q[t])

# create a plot of the state trajectory
plt.figure()
plt.step(range(num_samples), q, '-r')
plt.xlabel('Time ($t$)')
plt.ylabel('State ($q$)')

# estimate the stationary distribution from the samples
pi = np.zeros(3)
for i in range(3):
    pi[i] = np.sum(q==i)/num_samples

print('estimated stationary distribution (solved using simulation):')
print(' P(q=0) = {:.3f} (clear day)'.format(pi[0]))
print(' P(q=1) = {:.3f} (rainy day)'.format(pi[1]))
print(' P(q=2) = {:.3f} (snowy day)'.format(pi[2]))

#%% steady-state analysis

# formal state transition matrix
P = [[186/250, 47/250, 17/250], 
     [47/89, 40/89, 2/89],
     [16/25, 3/25, 6/25]]

# compute the eigenvalues and eigenvectors of the transpose of P
w,v = np.linalg.eig(np.transpose(P))

# the stationary distribution is the normalized eigenvector 
# corresponding to the eigenvalue of 1
pi_exact = v[:,0]/np.sum(v[:,0])

print('exact stationary distribution (solved using eigenvectors):')
print(' P(q=0) = {:.3f} (clear day)'.format(pi_exact[0]))
print(' P(q=1) = {:.3f} (rainy day)'.format(pi_exact[1]))
print(' P(q=2) = {:.3f} (snowy day)'.format(pi_exact[2]))