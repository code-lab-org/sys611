"""
SYS-611 Inventory Model

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
import numpy as np
# import the matplotlib.pyplot package and refer to it as `plt`
import matplotlib.pyplot as plt

# define simulation parameters
product_price = 100.00 # dollars per item
product_cost = 50.00 # dollars per item
holding_cost = 2.00 # dollars per item per day
arrival_rate = 5 # customers per day
demand_lb = 1 # items per customer
demand_ub = 4 # items per customer
order_trigger = 15 # items
order_target = 20 # items
delivery_delay = 2 # days

def generate_interarrival():
    # generates a customer inter-arrival time
    return np.random.exponential(scale=1./arrival_rate)
    
def generate_demand():
    # generates a customer demand
    return np.random.randint(demand_lb, demand_ub+1)

# initialize simulation variables
t = 0.0
inventory = order_target
num_ordered = 0
cost_orders = 0.0
cost_holding = 0.0
revenue = 0.0
t_customer = generate_interarrival()
t_delivery = float('inf')

# initialize data lists for plotting
plot_t = []
plot_P = []

def print_state():
    """Prints this simulation state."""
    print('Time = {:.2f}'.format(t))
    print('Inventory on Hand = {:d}'.format(inventory))
    print('Amount on Order = {:d}'.format(num_ordered))
    print('Event list = C: {:.1f}, D: {:.1f}'.format(
            t_customer, t_delivery))
    print('Order Costs = {:.2f}'.format(cost_orders))
    print('Holding Costs = {:.2f}'.format(cost_holding))
    print('Revenue = {:.2f}'.format(revenue))
    print('')
    
# print the simulation state
print_state()

# iterate over the first 14.0 days
while t < 14.0:
    # compute the holding costs for current inventory since last time
    cost_holding += holding_cost*inventory*(min(t_customer, t_delivery) - t)
    # update the simulation time
    t = min(t_customer, t_delivery)
    
    # check if this is a customer event (the tie-breaker if same time)
    if t == t_customer:
        # generate the customer demand
        demand = generate_demand()
        
        # check if inventory exceeds demands - can meet all demand
        if inventory > demand:
            # update revenue and inventory levels after sale
            revenue += product_price*demand
            inventory -= demand
        # otherwise can only meet partial demand
        else:
            # update revenue and inventory levels after sale
            revenue += product_price*inventory
            inventory = 0
        
        # check if inventory falls below order trigger and no order in progress
        if inventory < order_trigger and num_ordered == 0:
            # place an order, update costs and delivery event time
            num_ordered = order_target - inventory
            cost_orders += product_cost*num_ordered
            t_delivery = t + delivery_delay
        
        # generate the next customer arrival
        t_customer += generate_interarrival()
    # check if this is a delivery event
    else:
        # add the ordered products to the inventory        
        inventory += num_ordered
        
        # reset the number ordered and delivery time
        num_ordered = 0
        t_delivery = float('inf')
    
    # print the simulation state for first 2.0 days
    if t < 2.0:
        print_state()
    
    # append data for plotting
    plot_t.append(t)
    plot_P.append(revenue-cost_orders-cost_holding)
    
plt.figure()
plt.plot(plot_t, plot_P, '-r')
plt.xlabel('Time ($t$)')
plt.ylabel('Profit')