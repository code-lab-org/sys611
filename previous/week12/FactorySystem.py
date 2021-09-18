"""
SYS-611: Example factory model in SimPy.

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
NUM_REPAIRERS = 3

#%% SECTION TO DEFINE SIMULATION
    
def factory_run(env, repairers, spares):
    """ Process to run this simulation. 
        
    Args:
        env (simpy.Environment): the simulation environment
        repairers (simpy.Resource): the repairers resource
        spares (simpy.Container): the spares container
    """
    # define global variables for inter-process communication
    # note: this is a bad practice; however, is OK in this small script
    global cost
    cost = 0
    
    # launch the 50 machine processes
    for i in range(50):
        env.process(operate_machine(env, i+1, repairers, spares))
    # update the daily costs each day
    while True:
        cost += 3.75*8*repairers.capacity + 30*spares.capacity
        yield env.timeout(8.0)
    
def operate_machine(env, machine, repairers, spares):
    """ Process to operate a machine.
    
    Args:
        env (simpy.Environment): the simulation environment
        machine (int): the machine number
        repairers (simpy.Resource): the repairers resource
        spares (simpy.Container): the spares container
    """
    # define global variables for inter-process communication
    # note: this is a bad practice; however, is OK in this small script
    global cost
    
    while True:
        # wait until the machine breaks
        yield env.timeout(np.random.uniform(132,182))
        time_broken = env.now
        if NUM_RUNS <= 1:
            print('machine {} broke at {:.2f} ({} spares available)'.format(
                    machine, time_broken, spares.level))
        # launch the repair process
        env.process(repair_machine(env, repairers, spares))
        # wait for a spare to become available
        yield spares.get(1)
        time_replaced = env.now
        if NUM_RUNS <= 1:
            print('machine {} replaced at {:.2f}'.format(machine, time_replaced))
        # update the cost for being out of service
        cost += 20*(time_replaced-time_broken)
          
def repair_machine(env, repairers, spares):
    """ Process to repair a machine. 

    Args:
        env (simpy.Environment): the simulation environment
        repairers (simpy.Resource): the repairers resource
        spares (simpy.Container): the spares container    
    """
    with repairers.request() as request:
        # wait for a repairer to become available
        yield request
        # perform the repair
        yield env.timeout(np.random.uniform(4,10))
        # put the machine back in the spares pool
        yield spares.put(1)
        if NUM_RUNS <= 1:
            print('repair complete at {:.2f} ({} spares available)'.format(
                    env.now, spares.level))

def observe(env, spares):
    """ Process to observe the factory during a simulation.
    
    Args:
        env (simpy.Environment): the simulation environment
        factory (Factory): the factory
    """
    while True:
        obs_time.append(env.now)
        obs_cost.append(cost)
        obs_spares.append(spares.level)
        yield env.timeout(1.0)

#%% SECTION TO RUN ANALYSIS
        
# array to store outputs
COST = []

for i in range(NUM_RUNS):
    # arrays to record data
    obs_time = []
    obs_cost = []
    obs_spares = []
    
    # set the random number seed
    np.random.seed(i)
    
    # create the simpy environment
    env = simpy.Environment()
    # create the resources
    repairers = simpy.Resource(env, capacity=NUM_REPAIRERS) 
    spares = simpy.Container(env, init=NUM_SPARES, capacity=NUM_SPARES)
    # add the factory run process
    env.process(factory_run(env, repairers, spares))
    # add the observation process
    env.process(observe(env, spares))
    # run simulation
    env.run(until=SIM_DURATION)
    # record the final observed cost
    COST.append(obs_cost[-1])
    
    if NUM_RUNS <= 1:
        # output the total cost
        print('Total cost: {:.2f}'.format(obs_cost[-1]))
        
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