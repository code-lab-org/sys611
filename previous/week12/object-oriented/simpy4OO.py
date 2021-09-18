"""
Example 4 for SimPy (object-oriented)

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the simpy package 
# see https://simpy.readthedocs.io/en/latest/api_reference for documentation
import simpy

class Car(object):
    """ Car object for a SimPy discrete event simulation."""
    def __init__(self, env, name):
        """ Initializes this car and launches the execute process.
        
        Args: 
            env (simpy.Environment): the SimPy environment
            name (str): this car's name
        """
        self.env = env
        self.name = name
        
    def park(self, duration):
        """ Enters the parking state.
        
        Args: 
            duration (float): the time in the parking state (hours)
        """
        print('{} start parking @ {}'.format(self.name, self.env.now))
        yield self.env.timeout(duration)
        
    def drive(self, duration):
        """ Enters the driving state.
        
        Args: 
            duration (float): the time in the driving state (hours)
        """
        print('{} start driving @ {}'.format(self.name, self.env.now))
        yield self.env.timeout(duration)
        
    def run(self, lot, parking_duration, driving_duration):
        """ Runs this car's process.
        
        Args:
            lot (simpy.Resource): the shared parking lot
            parking_duration (float): the time in the parking state (hours)
            driving_duration (float): the time in the driving state (hours)
        """
        while True:
            with lot.request() as request:
                print('{} waiting for parking @ {}'.format(self.name, self.env.now))
                yield request # wait for access to resource
                print('{} got parking @ {}'.format(self.name, self.env.now))
                yield self.env.process(self.park(parking_duration))
            yield self.env.process(self.drive(driving_duration))

# create the simpy simulation environment
env = simpy.Environment()
single_lot = simpy.Resource(env, capacity=1)
# create two new car objects
env.process(Car(env, 'A').run(single_lot, 5.0, 2.0))
env.process(Car(env, 'B').run(single_lot, 3.0, 3.0))
# run the simulation for 15.0 minutes
env.run(until=15.0)