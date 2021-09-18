"""
SYS-611 Cafe Discrete Event Simulation.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
import numpy as np
# import the matplotlib.pyplot package and refer to it as `plt`
import matplotlib.pyplot as plt
    
# define process generator for x
def generate_x():
    # define the arrival rate
    _lambda = 1/1.5
    return -np.log(1-np.random.rand())/_lambda

# define process generator for y
def generate_y():
    # define the service rate
    _mu = 1/0.75
    return -np.log(1-np.random.rand())/_mu 

# define process generator for balk
def generate_b(N):
    r = np.random.rand()
    if N > 5 and r < 0.5:
        return True
    else:
        return False

# initialize variables
t = 0
t_A = generate_x()
t_D = np.inf
N = 0
N_A = 0
N_B = 0
N_D = 0
W = 0

# initialize data lists for plotting
plot_t = []
plot_N = []
plot_B = []

print('{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}'.format(
        'i', 't', 't_A', 't_D', 'N', 'N_A', 'N_D', 'N_B', 'W'))
print('{:10.2f}{:10.2f}{:10.2f}{:10.0f}{:10.0f}{:10.0f}{:10.0f}{:10.2f}'.format(
        t, t_A, t_D, N, N_A, N_D, N_B, W))

# loop until simulation ends
while t_A < np.inf or t_D < np.inf:
    # update the total waiting time
    W += N*(min(t_A,t_D)-t)
    # update the simulation time
    t = min(t_A,t_D)
    
    if t_A <= t_D:
        if generate_b(N):
            N_B += 1
        else:
            # this is an arrival - increment the state variable
            N += 1
            # record an arrival
            N_A += 1
            if N <= 1:
                # schedule the departure
                t_D = t + generate_y()
        # schedule another arrival as long as < 1000 minutes
        t_A = t + generate_x() if t < 1000 else np.inf
    else:
        # this is a departure - decrement the state variable
        N -= 1
        # record a departure
        N_D += 1
        # schedule the next departure if there are more in the system
        t_D = t + generate_y() if N > 0 else np.inf
    
    # append data for plotting
    plot_t.append(t)
    plot_N.append(N)
    plot_B.append(N_B)

    print('{:10.2f}{:10.2f}{:10.2f}{:10.0f}{:10.0f}{:10.0f}{:10.0f}{:10.2f}'.format(
            t, t_A, t_D, N, N_A, N_D, N_B, W))
print('W_bar = {:.2f}'.format(W/N_A))

plt.figure()
plt.plot(plot_t, plot_N, '-r', label="$N$")
plt.plot(plot_t, plot_B, '-b', label="$N_B$")
plt.xlabel('Time ($t$)')
plt.ylabel('Number Customers')
plt.legend(loc='best')