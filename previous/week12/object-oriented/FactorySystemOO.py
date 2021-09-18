"""
SYS-611: Example factory model in SimPy (object-oriented).

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
# simulation duration (hours)
SIM_DURATION = 5*8*52
# number of spares to purchase (S)
NUM_SPARES = 20
# number of repairers to hire (R)
NUM_REPAIRERS = 5

#%% SECTION TO DEFINE SIMULATION

class Factory(object):
    """ Defines a factory simulation. """
    def __init__(self, env, num_repairers, num_spares):
        """ Initializes this factory.
        
        Args:
            env (simpy.Environment): the simulation environment
            num_repairers (int): the number of repairers to hire
            num_spares (int): the number of spares to purchase
        """
        self.repairers = simpy.Resource(env, capacity=num_repairers) 
        self.spares = simpy.Container(env, init=num_spares, capacity=num_spares)
        self.env = env
        self.cost = 0
        self.daily_cost = 3.75*8*num_repairers + 30*num_spares
    
    def run(self):
        """ Process to run this simulation. """
        # launch the 50 machine processes
        for i in range(50):
            self.env.process(factory.operate_machine(i+1))
        # update the daily costs each day
        while True:
            self.cost += self.daily_cost
            yield self.env.timeout(8.0)
    
    def operate_machine(self, machine):
        """ Process to operate a machine.
        
        Args:
            machine (int): the machine number
        """
        while True:
            # wait until the machine breaks
            yield self.env.timeout(np.random.uniform(132,182))
            time_broken = self.env.now
            if NUM_RUNS <= 1:
                print('machine {} broke at {:.2f} ({} spares available)'.format(
                        machine, time_broken, self.spares.level))
            # launch the repair process
            self.env.process(self.repair_machine())
            # wait for a spare to become available
            yield self.spares.get(1)
            time_replaced = self.env.now
            if NUM_RUNS <= 1:
                print('machine {} replaced at {:.2f}'.format(machine, time_replaced))
            # update the cost for being out of service
            self.cost += 20*(time_replaced-time_broken)
              
    def repair_machine(self):
        """ Process to repair a machine. """
        with self.repairers.request() as request:
            # wait for a repairer to become available
            yield request
            # perform the repair
            yield self.env.timeout(np.random.uniform(4,10))
            # put the machine back in the spares pool
            yield self.spares.put(1)
            if NUM_RUNS <= 1:
                print('repair complete at {:.2f} ({} spares available)'.format(
                        self.env.now, self.spares.level))

# arrays to record data
obs_time = []
obs_cost = []
obs_spares = []

def observe(env, factory):
    """ Process to observe the factory during a simulation.
    
    Args:
        env (simpy.Environment): the simulation environment
        factory (Factory): the factory
    """
    while True:
        obs_time.append(env.now)
        obs_cost.append(factory.cost)
        obs_spares.append(factory.spares.level)
        yield env.timeout(1.0)

#%% SECTION TO RUN ANALYSIS

# array to store outputs
COST = []

for i in range(NUM_RUNS):
    # set the random number seed
    np.random.seed(i)
    
    # create the simpy environment
    env = simpy.Environment()
    # create the factory
    factory = Factory(env, NUM_REPAIRERS, NUM_SPARES)
    # add the factory run process
    env.process(factory.run())
    # add the observation process
    env.process(observe(env, factory))
    # run simulation
    env.run(until=SIM_DURATION)
    # record the final observed cost
    COST.append(obs_cost[-1])
    
    if NUM_RUNS <= 1:
        # output the total cost
        print('Total cost: {:.2f}'.format(factory.cost))
        
        # plot the number of spares available
        plt.figure()
        plt.step(obs_time, obs_spares, where='post')
        plt.xlabel('Time (hour)')
        plt.ylabel('Number Spares Available')
        
        # plot the total cost accumulation
        plt.figure()
        plt.step(obs_time, obs_cost, where='post')
        plt.xlabel('Time (hour)')
        plt.ylabel('Total Cost')

    # print final results to console
    print('Factory costs for N={:} runs with R={:} repairers and S={:} spares:'.format(
            NUM_RUNS, NUM_REPAIRERS, NUM_SPARES))
    print('\n'.join('{:.2f}'.format(i) for i in COST))

#%% SECTION TO WRITE RESULTS TO CSV FILE

import csv

with open('factory.csv', 'w') as output:
    writer = csv.writer(output)
    for sample in COST:
        writer.writerow([sample])