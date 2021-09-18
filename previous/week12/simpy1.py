"""
Example 1 for SimPy.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the simpy package 
# see https://simpy.readthedocs.io/en/latest/api_reference for documentation
import simpy

def car_run(env):
    """ Generator which alternates between parking and driving. 
    
    Args:
        env (simpy.Environment) - the simulation environment
    """
    while True:
        print('start parking @ {}'.format(env.now))
        # wait for 5.0 hours (while parking)
        yield env.timeout(5.0)
        
        print('start driving @ {}'.format(env.now))
        # wait for 2.0 hours (while driving)
        yield env.timeout(2.0)

# create the simpy simulation environment
env = simpy.Environment()
# add a new car process to the environment
env.process(car_run(env))
# run the simulation for 15.0 minutes
env.run(until=15.0)