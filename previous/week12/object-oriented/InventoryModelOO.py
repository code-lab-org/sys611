"""
SYS-611: Example inventory model in SimPy (object-oriented).

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
ORDER_UP_TO = 20

#%% SECTION TO DEFINE SIMULATION

class Warehouse(object):
    """ Defines a warehouse simulation. """
    def __init__(self, env, order_threshold, order_up_to):
        """ Initializes this warehouse.
        
        Args:
            env (simpy.Environment): the simulation environment
            order_threshold (int): the threshold inventory level to place order
            order_up_to (int): the target inventory level
        """
        self.product_price = 100.00 # dollars per product
        self.product_cost = 50.00 # dollars per product
        self.holding_cost = 2.00 # dollars per product per day
        self.arrival_rate = 5 # customers per day
        self.demand_lb = 1 # products per customer
        self.demand_ub = 4 # products per customer
        self.order_threshold = order_threshold # products
        self.order_up_to = order_up_to # products
        self.delivery_delay = 2 # days
        
        self.env = env
        self.inventory = order_up_to
        self.num_ordered = 0
        self.balance = 0
    
    def run(self):
        """ Process to run this simulation. """
        # initialize the customer counter
        i = 0
        # enter infinite loop
        while True:
            # wait for the next arrival
            inter_arrival = np.random.exponential(1./self.arrival_rate)
            yield self.env.timeout(inter_arrival)
            # subtract holding costs
            self.balance -= self.holding_cost*self.inventory*inter_arrival
            # increment a counter
            i += 1
            customer = 'Cust {}'.format(i)
            # generate demand
            demand = np.random.randint(self.demand_lb, self.demand_ub+1) 
            if NUM_RUNS <= 1:
                print('{} demands {} at t={:.2f}'.format(customer, demand, env.now))
            # handle demands
            if self.inventory > demand:
                num_sold = demand
            else:
                num_sold = self.inventory
            self.balance += self.product_price*num_sold
            self.inventory -= num_sold
            if num_sold > 0:
                if NUM_RUNS <= 1:
                    print('{} buys {} at t={:.2f} ({} remaining)'.format(
                            customer, demand, env.now, self.inventory))
            # check for order
            if self.inventory < self.order_threshold and self.num_ordered == 0:
                quantity = self.order_up_to - self.inventory
                self.env.process(self.handle_order(quantity))
    
    def handle_order(self, quantity):
        """ Process to place an order.
        
        Args:
            quantity (int): the order quantity
        """
        if NUM_RUNS <= 1:
            print('order {} at t={}'.format(quantity, env.now))
        self.num_ordered = quantity
        self.balance -= self.product_cost*quantity
        
        # wait for the delivery to arrive
        yield self.env.timeout(self.delivery_delay)
        
        if NUM_RUNS <= 1:
            print('delivery of {} at t={:.2f}'.format(quantity, env.now))
        self.inventory += quantity
        self.num_ordered = 0

def observe(env, warehouse):
    """ Process to observe the warehouse inventory during a simulation.
    
    Args:
        env (simpy.Environment): the simulation environment
        warehouse (Warehouse): the warehouse
    """
    while True:
        # record the observation time and queue length
        obs_time.append(env.now)
        inventory_level.append(warehouse.inventory)
        # wait for the next minute
        yield env.timeout(0.1)
#%% SECTION TO RUN ANALYSIS

# array to store outputs
BALANCE = []

for i in range(NUM_RUNS):
    # arrays to record data
    queue_wait = []
    total_wait = []
    obs_time = []
    inventory_level = []
    
    # set the initial seed
    np.random.seed(i)
    
    # create the simpy environment
    env = simpy.Environment()
    # create the warehouse
    warehouse = Warehouse(env, ORDER_THRESHOLD, ORDER_UP_TO)
    # add the warehouse run process
    env.process(warehouse.run())
    # add the observation process
    env.process(observe(env, warehouse))
    # run the simulation
    env.run(until=SIM_DURATION)
    # record the final observed net revenue
    BALANCE.append(warehouse.balance)
    
    if NUM_RUNS <= 1:
        print('Final balance: {:.2f}'.format(warehouse.balance))
        
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