"""
Example 4 for SimPy.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

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
    
def car_run(env, name, lot, parking_duration, driving_duration):
    """ Generator which alternates between parking and driving. 
    
    Args:
        env (simpy.Environment) - the simulation environment
        name (str) - the car name
        lot (simpy.Resource): the shared parking lot
        parking_duration (float) - the parking duration (hours)
        driving_duration (float) - the driving duration (hours)
    """
    while True:
        with lot.request() as request:
            print('{} waiting for parking @ {}'.format(name, env.now))
            yield request # wait for access to resource
            print('{} got parking @ {}'.format(name, env.now))
            yield env.process(car_park(env, name, parking_duration))
        yield env.process(car_drive(env, name, driving_duration))

# create the simpy simulation environment
env = simpy.Environment()
single_lot = simpy.Resource(env, capacity=1)
# create two new car objects
env.process(car_run(env, 'A', single_lot, 5.0, 2.0))
env.process(car_run(env, 'B', single_lot, 3.0, 3.0))
# run the simulation for 15.0 minutes
env.run(until=15.0)