"""
Example 2 for SimPy.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the simpy package 
# see https://simpy.readthedocs.io/en/latest/api_reference for documentation
import simpy

def car_run(env, car, parking_duration, driving_duration):
    """ Generator which alternates between parking and driving. 
    
    Args:
        env (simpy.Environment) - the simulation environment
        car (str) - the car name
        parking_duration (float) - the parking duration (hours)
        driving_duration (float) - the driving duration (hours)
    """
    while True:
        print('{} start parking @ {}'.format(car, env.now))
        # wait for parking to finish
        yield env.timeout(parking_duration)
        
        print('{} start driving @ {}'.format(car, env.now))
        # wait for driving to finish
        yield env.timeout(driving_duration)

# create the simpy simulation environment
env = simpy.Environment()
# add two new car processes to the environment
env.process(car_run(env, 'A', 5.0, 2.0))
env.process(car_run(env, 'B', 3.0, 3.0))
# run the simulation for 15.0 minutes
env.run(until=15.0)