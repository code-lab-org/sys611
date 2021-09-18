"""
SYS-611: Example inventory model in SimPy.

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
# simulation duration (days)
SIM_DURATION = 100
# threshold inventory level to trigger an order (Q)
ORDER_THRESHOLD = 10
# inventory level to order up to (S)
ORDER_UP_TO = 30

#%% SECTION TO DEFINE SIMULATION

product_price = 100.00 # dollars per product
product_cost = 50.00 # dollars per product
holding_cost = 2.00 # dollars per product per day
arrival_rate = 5 # customers per day
demand_lb = 1 # products per customer
demand_ub = 4 # products per customer
delivery_delay = 2 # days

def warehouse_run(env, order_threshold, order_up_to):
    """ Process to run this simulation. 
    
    Args:
        env (simpy.Environment): the simulation environment
        order_threshold (int): the threshold inventory level to place order
        order_up_to (int): the target inventory level
    """
    # define global variables for inter-process communication
    # note: this is a bad practice; however, is OK in this small script
    global inventory, balance, num_ordered
    
    # initialize the customer counter
    i = 0
    # initialize the state variables
    inventory = order_up_to
    balance = 0
    num_ordered = 0
    
    # enter infinite loop
    while True:
        # wait for the next arrival
        interarrival = np.random.exponential(1./arrival_rate)
        yield env.timeout(interarrival)
        # subtract holding costs
        balance -= holding_cost*inventory*interarrival
        # increment a counter
        i += 1
        customer = 'Cust {}'.format(i)
        # generate demand
        demand = np.random.randint(demand_lb, demand_ub+1) 
        if NUM_RUNS <= 1:
            print('{} demands {} at t={:.2f}'.format(customer, demand, env.now))
        # handle demands
        if inventory > demand:
            num_sold = demand
        else:
            num_sold = inventory
        balance += product_price*num_sold
        inventory -= num_sold
        if num_sold > 0:
            if NUM_RUNS <= 1:
                print('{} buys {} at t={:.2f} ({} remaining)'.format(
                        customer, demand, env.now, inventory))
        # check for order
        if inventory < order_threshold and num_ordered == 0:
            quantity = order_up_to - inventory
            env.process(handle_order(env, quantity))
    
def handle_order(env, quantity):
    """ Process to place an order.
    
    Args:
        env (simpy.Environment): the simulation environment
        quantity (int): the order quantity
    """
    # define global variables to allow inter-process communication
    # note: this is a bad practice; however, is OK in this small script
    global inventory, balance, num_ordered
    
    if NUM_RUNS <= 1:
        print('order {} at t={}'.format(quantity, env.now))
    num_ordered = quantity
    balance -= product_cost*quantity
    
    # wait for the delivery to arrive
    yield env.timeout(delivery_delay)
    
    if NUM_RUNS <= 1:
        print('delivery of {} at t={:.2f}'.format(quantity, env.now))
    inventory += quantity
    num_ordered = 0

def observe(env):
    """ Process to observe the warehouse inventory during a simulation.
    
    Args:
        env (simpy.Environment): the simulation environment
        warehouse (Warehouse): the warehouse
    """
    while True:
        # record the observation time and queue length
        obs_time.append(env.now)
        inventory_level.append(inventory)
        # wait for the next minute
        yield env.timeout(0.1)

#%% SECTION TO RUN ANALYSIS

# array to store outputs
BALANCE = []

for i in range(NUM_RUNS):
    # set the random number seed
    np.random.seed(i)
    
    # arrays to record data
    obs_time = []
    inventory_level = []
    
    # create the simpy environment
    env = simpy.Environment()
    # add the warehouse run process
    env.process(warehouse_run(env, ORDER_THRESHOLD, ORDER_UP_TO))
    # add the observation process
    env.process(observe(env))
    # run the simulation
    env.run(until=SIM_DURATION)
    # record the final observed net revenue
    BALANCE.append(balance)
    
    if NUM_RUNS <= 1:
        print('Final balance: {:.2f}'.format(balance))
        
        # plot the inventory over time
        plt.figure()
        plt.step(obs_time, inventory_level, where='post')
        plt.xlabel('Time (day)')
        plt.ylabel('Inventory Level')

# print final results to console
print('Net revenue balance for N={:} runs with Q={:} and S={:}:'.format(
        NUM_RUNS, ORDER_THRESHOLD, ORDER_UP_TO))
print('\n'.join('{:.2f}'.format(i) for i in BALANCE))

#%% SECTION TO WRITE RESULTS TO CSV FILE

import csv

with open('inventory.csv', 'w') as output:
    writer = csv.writer(output)
    for sample in BALANCE:
        writer.writerow([sample])
