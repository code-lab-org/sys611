"""
SYS-611: Buffon's Needle Experiment Example.

This example performs a Monte Carlo simulation of Buffon's Needle Experiment
to estimate the probability of a needle of certain length crossing lines
on a floor with certain spacing. This probability is proportional to the
mathematical constant pi.

@author: Paul T. Grogan <pgrogan@stevens.edu>
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

# import the scipy stats package and refer to it as `stats`
# see http://docs.scipy.org/doc/scipy/reference/stats.html for documentation
import scipy.stats as stats

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# define the line width and needle length for buffon's experiment
line_width = 3.0
needle_length = 2.5

# define a process generator for the event if a needle crosses a line
def drop_needle():
    # generate distance between needle centroid and nearest line from uniform 
    # distribution between 0 and line_width/2
    d = np.random.rand()*line_width/2
    # generate acute angle between needle and line from uniform distribution
    # between 0 and pi/2 radians
    theta = np.random.rand()*np.pi/2
    
    # return True if d < needle_length/2*sin(theta)
    # otherwise return False
    if d < needle_length/2*np.sin(theta):
        return True
    else:
        return False

# set the random number generator seed to 0
np.random.seed(0)

# generate 10000 samples
samples = [drop_needle() for i in range(10000)]

# compute the lower and upper-bounds using a 95% confidence interval
confidence_level = 0.05
z_crit = stats.norm.ppf(1-confidence_level/2)

print('p = {:.3f} +/- {:.3f} (95% CI)'.format(
        np.average(samples),
        z_crit*stats.sem(samples)
    ))

# compute the exact solution, as solved by calculus
solution = 2*needle_length/(line_width*np.pi)

# compute running statistics for mean and confidence interval
mean_estimate = np.array([np.average(samples[0:i]) for i in range(len(samples))])
confidence_int = z_crit*np.array([stats.sem(samples[0:i]) for i in range(len(samples))])

# create a plot to show the mean estimate with 95% confidence interval bounds
plt.figure()
plt.plot(range(len(samples)), mean_estimate, 
         'b', label='Mean Estimate')
plt.plot(range(len(samples)), mean_estimate-confidence_int, 
         'g', label='95% CI Lower Bound')
plt.plot(range(len(samples)), mean_estimate+confidence_int, 
         'r', label='95% CI Upper Bound')
#plt.plot([0, len(samples)], [solution, solution], 
#          '-k', label='Analytical Solution')
plt.xlabel('Sample')
plt.ylabel('Estimate of $p$')
plt.legend(loc='best')

#%%

# transform the mean estimate to estimate pi using the solution form
pi_estimate = 2*needle_length/(line_width*mean_estimate)
pi_lower_bound = 2*needle_length/(line_width*(mean_estimate+confidence_int))
pi_upper_bound = 2*needle_length/(line_width*(mean_estimate-confidence_int))

print('pi = {:.3f} +/- {:.3f} (95% CI)'.format(
        pi_estimate[-1],
        pi_upper_bound[-1] - pi_estimate[-1]
    ))

# create a plot to show the pi estimate with 95% confidence interval bounds
plt.figure()
plt.plot(range(len(samples)), pi_estimate, 
         'b', label='Mean Estimate')
plt.plot(range(len(samples)), pi_lower_bound, 
         'g', label='95% CI Lower Bound')
plt.plot(range(len(samples)), pi_upper_bound, 
         'r', label='95% CI Upper Bound')
plt.plot([0, len(samples)], [np.pi, np.pi], 
         '-k', label='Analytical Solution')
plt.xlabel('Sample')
plt.ylabel('Estimate of $\pi$')
plt.legend(loc='best')