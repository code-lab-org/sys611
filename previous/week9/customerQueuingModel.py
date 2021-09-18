"""
SYS 611: Customer-based Queuing Simulation.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np
    
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

# set random number seed
np.random.seed(0)

# define the number of customers and create arrays to store results
num_customers = 1000
x = [generate_x() for i in range(num_customers)]
y = [generate_y() for i in range(num_customers)]
t_enter = np.zeros(num_customers)
q_length = np.zeros(num_customers)
t_served = np.zeros(num_customers)
q_wait = np.zeros(num_customers)
t_exit = np.zeros(num_customers)
total_wait = np.zeros(num_customers)

# loop over each  customer
for i in range(num_customers):
    # entry time is appended to the previous entry time
    # or equal to arrival time for first customer
    t_enter[i] = t_enter[i-1] + x[i] if i > 0 else x[i]
    # queue length is the number of customers who have not yet exited
    # or zero for the first customer
    q_length[i] = np.sum(t_exit[0:i] > t_enter[i]) if i > 0 else 0
    # time served is the exit time of previous customer if in queue
    # or entry time if no queue
    t_served[i] = t_exit[i-1] if q_length[i] > 0 else t_enter[i]
    # waiting time in queue is service time minus entry time
    q_wait[i] = t_served[i]-t_enter[i]
    # exit time is time served plus service time
    t_exit[i] = t_served[i] + y[i]
    # total wait is exit time minus entry time
    total_wait[i] = t_exit[i] - t_enter[i]

print('{:>4s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}{:>10s}'.format(
        'i', 't_enter', 'L_q', 't_served', 'W_q', 't_exit', 'W'))
for i in range(num_customers):
    print('{:4d}{:10.2f}{:10.0f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}'.format(
            i+1, t_enter[i], q_length[i], t_served[i], 
            q_wait[i], t_exit[i], total_wait[i]))
print('L_q_bar = {:.2f}'.format(np.mean(q_length)))
print('W_q_bar = {:.2f}'.format(np.mean(q_wait)))
print('W_bar = {:.2f}'.format(np.mean(total_wait)))