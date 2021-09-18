"""
Example 3 for SimPy.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the simpy package 
# see https://simpy.readthedocs.io/en/latest/api_reference for documentation
import simpy

def car_park(env, name, duration):
    """ Generator which parks a car for a duration. 
    
    Args:
        env (simpy.Environment) - the simulation environment
        name (str) - the car name
        duration (float) - the parking duration (hours)
    """
    print('{} start parking @ {}'.format(name, env.now))
    yield env.timeout(duration)
    
def car_drive(env, name, duration):
    """ Generator which drives a car for a duration. 
    
    Args:
        env (simpy.Environment) - the simulation environment
        name (str) - the car name
        duration (float) - the driving duration (hours)
    """
    print('{} start driving @ {}'.format(name, env.now))
    yield env.timeout(duration)

def car_run(env, name, parking_duration, driving_duration):
    """ Generator which alternates between parking and driving. 
    
    Args:
        env (simpy.Environment) - the simulation environment
        car (str) - the car name
        parking_duration (float) - the parking duration (hours)
        driving_duration (float) - the driving duration (hours)
    """
    while True:
        # wait for parking to finish
        yield env.process(car_park(env, name, parking_duration))
        # wait for driving to finish
        yield env.process(car_drive(env, name, driving_duration))

# create the simpy simulation environment
env = simpy.Environment()
# create two new car objects
env.process(car_run(env, 'A', 5.0, 2.0))
env.process(car_run(env, 'B', 3.0, 3.0))
# run the simulation for 15.0 minutes
env.run(until=15.0)