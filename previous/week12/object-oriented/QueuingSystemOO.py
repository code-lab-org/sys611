"""
SYS-611: Example queuing model in SimPy (object-oriented).

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

class CafeJava(object):
    """ Defines a cafe simulation. """
    def __init__(self, env, num_servers, _lambda, _mu):
        """ Initializes this cafe.

        Args:
            env (simpy.Environment): the simulation environment
            num_servers (int): the number of servers
            _lambda (float): the average inter-arrival rate (customers/minute)
            _mu (float): the average service rate (customers/minute)
        """
        self.env = env
        self.servers = simpy.Resource(env, num_servers)
        self._mu = _mu
        self._lambda = _lambda
        self.queue_wait = []
        self.total_wait = []

    def handle_customer(self, customer):
        """ Process to handle a customer.

        Args:
            customer (str): the name of the customer
        """
        with self.servers.request() as request:
            arrival_time = env.now
            if NUM_RUNS <= 1:
                print('{} enters cafe at t={:.2f}'.format(customer, arrival_time))
            # wait for the request to be fulfilled
            yield request
            service_time = env.now
            self.queue_wait.append(service_time - arrival_time)
            if NUM_RUNS <= 1:
                print('{} gets service at t={:.2f}'.format(customer, service_time))
            # wait for the service to complete
            yield self.env.timeout(np.random.exponential(1/self._mu))
            depart_time = env.now
            self.total_wait.append(depart_time - arrival_time)
            if NUM_RUNS <= 1:
                print('{} departs cafe at t={:.2f}'.format(customer, depart_time))

    def run(self):
        """ Process to run this cafe simulation."""
        # initialize the customer counter
        i = 0
        # enter infinite loop
        while True:
            # wait for the next arrival
            yield env.timeout(np.random.exponential(1/self._lambda))
            # increment a counter
            i += 1
            # launch the customer process
            env.process(self.handle_customer('Cust {}'.format(i)))

def observe_queue(env, cafe, obs_time, queue_length):
    """ Process to observe the queue length during a simulation.

    Args:
        env (simpy.Environment): the simulation environment
        cafe (CafeJava): the cafe to observe
        obs_time (list): the observation times
        queue_length (list): the observed queue length
    """
    while True:
        # record the observation time and queue length
        obs_time.append(env.now)
        queue_length.append(len(cafe.servers.queue))
        # wait for the next minute
        yield env.timeout(1.0)

#%% SECTION TO RUN ANALYSIS

# array to store outputs
AVERAGE_WAIT = []

for i in range(NUM_RUNS):
    # arrays to record data
    obs_time = []
    queue_length = []

    # set the initial seed
    np.random.seed(i)

    # create the simpy environment
    env = simpy.Environment()
    cafe = CafeJava(env, 1, 3, 4)
    # add the cafe process
    env.process(cafe.run())
    # add the observation process
    env.process(observe_queue(env, cafe, obs_time, queue_length))
    # run the simulation
    env.run(until=SIM_DURATION)
    # record the final average waiting time
    AVERAGE_WAIT.append(np.mean(cafe.total_wait))

    if NUM_RUNS <= 1:
        # create a plot showing the queue length at each time
        plt.figure()
        plt.step(obs_time, queue_length, where='post')
        plt.xlabel('Simulation Time (min)')
        plt.ylabel('Queue Length')

        # create a plot showing the histogram of waiting time
        plt.figure()
        plt.hist(cafe.total_wait)
        plt.xlabel('Total Waiting Time (min)')
        plt.ylabel('Number of Customers')

        # create a plot showing the average queue length at each time
        plt.figure()
        plt.plot(obs_time, np.divide(np.cumsum(queue_length).astype('float'),
                                     1+np.arange(len(queue_length))))
        plt.xlabel('Simulation Time (min)')
        plt.ylabel('Average Queue Length')

        # create a plot showing the average wait time (queue and total) at each time
        plt.figure()
        plt.plot(1+np.arange(len(cafe.queue_wait)),
                 [np.mean(cafe.queue_wait[0:i]) for i in range(len(cafe.queue_wait))],
                  label='Wait in Queue')
        plt.plot(1+np.arange(len(cafe.total_wait)),
                 [np.mean(cafe.total_wait[0:i]) for i in range(len(cafe.total_wait))],
                  label='Total Wait')
        plt.xlabel('Customer')
        plt.ylabel('Average Wait (min)')
        plt.legend(loc='best')

# print final results to console
print('Average waiting time for N={:} runs:'.format(NUM_RUNS))
print('\n'.join('{:.2f}'.format(i) for i in AVERAGE_WAIT))
