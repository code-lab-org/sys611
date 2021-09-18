# -*- coding: utf-8 -*-
"""
SYS-611 Queuing Markov Model Example

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it is `np`
import numpy as np
# import the matplotlib pyplot package and refer to it is `plt`
import matplotlib.pyplot as plt

_lambda = 1/1.5 # arrival rate, 1.5 minutes per customer or 2/3 customer per minute
_mu = 1/0.75 # service rate, 0.75 minutes per customer or 4/3 customer per minute

# define process generator for inter-arrival duration
def gen_t_arrival():
    r = np.random.rand()
    return -np.log(1-r)/_lambda
    # note: could also use
    # return np.random.exponential(scale=1/_lambda)

# define process generator for service duration
def gen_t_service():
    r = np.random.rand()
    return -np.log(1-r)/_mu
    # note: could also use
    # return np.random.exponential(scale=1/_mu)
    
# define the number of events
NUM_EVENTS = 1000
# create lists to store variables of interest
t = np.zeros(NUM_EVENTS+1) # time
q = np.zeros(NUM_EVENTS+1) # number of customers in system
t_arrival = np.zeros(NUM_EVENTS) # sampled inter-arrival durations
t_service = np.zeros(NUM_EVENTS) # sampled service durations
delta_t = np.zeros(NUM_EVENTS) # duration of each event

# initialize time and state variables
t[0] = 0
q[0] = 0

for i in range(NUM_EVENTS):
    # generate samples for inter-arrival and service durations
    t_arrival[i] = gen_t_arrival()
    t_service[i] = gen_t_service()
    # process state transitions / updates for q and t
    if q[i] == 0 or t_arrival[i] < t_service[i]:
        # if no customers in queue or arrival happens before service
        # event is an arrival
        delta_t[i] = t_arrival[i]
        q[i+1] = q[i] + 1
    else:
        # otherwise event is a service
        delta_t[i] = t_service[i]
        q[i+1] = q[i] - 1
    t[i+1] = t[i] + delta_t[i]

print('{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}'.format(
        'i', 't(i)', 'q(i)', 't_arrival', 't_service', 'delta_t', 'q(i+1)'))
for i in range(NUM_EVENTS):
    print('{:10.0f}{:10.2f}{:10.0f}{:10.2f}{:10.2f}{:10.2f}{:10.0f}'.format(
            i, t[i], q[i], t_arrival[i], t_service[i], delta_t[i], q[i+1]))
    
plt.figure()
plt.xlabel('Time, $t$')
plt.ylabel('Customers in System, $q$')
plt.step(t,q,'-r',where='post')