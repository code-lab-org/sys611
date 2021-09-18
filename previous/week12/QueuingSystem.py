"""
SYS-611: Example queuing model in SimPy.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the simpy package
# see https://simpy.readthedocs.io/en/latest/api_reference for documentation
import simpy

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

#%% SECTION TO CONFIGURE SIMULATION

# number of simulation runs to perform
NUM_RUNS = 1
# simulation duration (minutes)
SIM_DURATION = 100

#%% SECTION TO DEFINE SIMULATION

def cafe_run(env, servers, _lambda, _mu):
    """ Process for simulating a cafe.

    Args:
        env (simpy.Environment): the simulation environment
        servers (simpy.Resource): the servers resource
        _lambda (float): the average inter-arrival rate (customers/minute)
        _mu (float): the average service rate (customers/minute)
    """
    # initialize the customer counter
    i = 0
    # enter infinite loop
    while True:
        # wait for the next arrival
        yield env.timeout(np.random.exponential(1/_lambda))
        # increment a counter
        i += 1
        # launch the customer process
        env.process(handle_customer(env, 'Cust {}'.format(i), servers, _mu))

def handle_customer(env, customer, servers, _mu):
    """ Process for simulating a customer.

    Args:
        env (simpy.Environment): the simulation environment
        customer (str): the customer name
        servers (simpy.Resource): the servers resource
        _mu (float): the average service rate (customer/minute)
    """
    with servers.request() as request:
        arrival_time = env.now
        if NUM_RUNS <= 1:
            print('{} enters cafe at t={:.2f}'.format(customer, arrival_time))
        # wait for the request to be fulfilled
        yield request
        service_time = env.now
        queue_wait.append(service_time - arrival_time)
        if NUM_RUNS <= 1:
            print('{} gets service at t={:.2f}'.format(customer, service_time))
        # wait for the service to complete
        yield env.timeout(np.random.exponential(1/_mu))
        depart_time = env.now
        if NUM_RUNS <= 1:
            print('{} departs cafe at t={:.2f}'.format(customer, depart_time))
        total_wait.append(depart_time - arrival_time)

def observe(env, servers):
    """ Process to observe the queue length during a simulation.

    Args:
        env (simpy.Environment): the simulation environment
        servers (simpy.Resource): the servers resource
    """
    while True:
        # record the observation time and queue length
        obs_time.append(env.now)
        queue_length.append(len(servers.queue))
        # wait for the next minute
        yield env.timeout(1.0)

#%% SECTION TO RUN ANALYSIS

# array to store outputs
AVERAGE_WAIT = []

for i in range(NUM_RUNS):
    # arrays to record data
    queue_wait = []
    total_wait = []
    obs_time = []
    queue_length = []

    # set the initial seed
    np.random.seed(i)

    # create the simpy environment
    env = simpy.Environment()
    # create the servers resource
    servers = simpy.Resource(env, capacity=1)
    # add the cafe process
    env.process(cafe_run(env, servers, 3.0, 4.0))
    # add the observation process
    env.process(observe(env, servers))
    # run the simulation
    env.run(until=SIM_DURATION)
    # record the final average waiting time
    AVERAGE_WAIT.append(np.mean(total_wait))

    if NUM_RUNS <= 1:
        # create a plot showing the queue length at each time
        plt.figure()
        plt.step(obs_time, queue_length, where='post')
        plt.xlabel('Simulation Time (min)')
        plt.ylabel('Queue Length')

        # create a plot showing the histogram of waiting time
        plt.figure()
        plt.hist(total_wait)
        plt.xlabel('Total Waiting Time (min)')
        plt.ylabel('Number of Customers')

        # create a plot showing the average queue length at each time
        plt.figure()
        plt.plot(obs_time, np.cumsum(queue_length)/np.arange(1,1+len(queue_length)))
        plt.xlabel('Simulation Time (min)')
        plt.ylabel('Average Queue Length')

        # create a plot showing the average wait time (queue and total) at each time
        plt.figure()
        plt.plot(1+np.arange(len(queue_wait)), np.cumsum(queue_wait)/np.arange(1,1+len(queue_wait)), label='Wait in Queue')
        plt.plot(1+np.arange(len(total_wait)), np.cumsum(total_wait)/np.arange(1,1+len(total_wait)), label='Total Wait')
        plt.xlabel('Customer')
        plt.ylabel('Average Wait (min)')
        plt.legend(loc='best')

# print final results to console
print('Average waiting time for N={:} runs:'.format(NUM_RUNS))
print('\n'.join('{:.2f}'.format(i) for i in AVERAGE_WAIT))
