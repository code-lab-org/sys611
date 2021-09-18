"""
Example: Cafe Java Demand Distribution and Process Generator.

This example develops a discrete process generator for coffee demand data
observed in Cafe Java.

@author: Paul T. Grogan <pgrogan@stevens.edu>
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

# create a numpy array with the demand sizes
demands = np.array([0, 1, 2, 3])
labels = ["None", "Small", "Medium", "Large"]
print("demands = {}".format(demands))

# create a numpy array with the observed frequencies
frequency = np.array([8, 10, 22, 10])

# the probability mass function is the number of demands (frequency) divided
# by the total number of demands (sub of all frequency)
pmf = frequency/np.sum(frequency)
print("pmf = {}".format(pmf))

# create a new figure for a bar plot using the demand indices, pmf values, 
# desired bar width, and color
plt.figure()
bar_width = 0.5
plt.bar(demands, pmf, bar_width, align='center', color='b')
plt.ylabel('p(x)')
plt.ylim([0,1])
plt.xlabel('Coffee Demand (x)')
plt.title('PMF for Cafe Java Demand')
plt.xticks(demands, labels)

# the cumulative distribution function is the cumulative sum of the PDF
cdf = np.cumsum(pmf)
print("cdf = {}".format(cdf))

# create a new figure for a step plot using the demand indices, cdf values,
# desired format (solid red line, -r), and option for post-steps
plt.figure()
plt.step(demands, cdf, '-r', where='post')
plt.ylabel('F(x)')
plt.ylim([0,1])
plt.xlabel('Coffee Demand (x)')
plt.title('CDF for Cafe Java Demand')
plt.xticks(demands, labels)

# define a function to generate demands following the accept-reject method
def generate_demand_arm():
    """Generates a demand following the accept-reject method.
    
    Returns:
        demand (int): the size of coffee demanded    
    """
    # create a CDF for alternatives
    alternatives = [0.25, 0.50, 0.75, 1.00]
    # store the accepted demand (-1 until accepted)
    accepted = -1
    # perform accept-reject while no demand is yet accepted
    while accepted < 0:
        # generate random U(0,1) samples
        r_1 = np.random.rand()
        r_2 = np.random.rand()
        # perform check for alternative 0
        if r_1 <= alternatives[0]:
            # check if second sample is less than PMF value
            if r_2 <= pmf[0]:
                accepted = 0
        # perform check for alternative 1
        elif r_1 <= alternatives[1]:
            # check if second sample is less than PMF value
            if r_2 <= pmf[1]:
                accepted = 1
        # perform check for alternative 2
        elif r_1 <= alternatives[2]:
            # check if second sample is less than PMF value
            if r_2 <= pmf[2]:
                accepted = 2
        # otherwise no need to check, it's the final CDF entry (alternative 3)
        else:
            # check if second sample is less than PMF value
            if r_2 <= pmf[3]:
                accepted = 3
        """
        note: the code above could be replaced with the following for 
        loop which iterates over each array index i in demands
        
        r_1 = np.random.rand()
        r_2 = np.random.rand()
        for i in range(len(demands)):
            if r_1 <= alternatives[i]:
                if r_2 <= pmf[i]:
                    accepted = i
        """
    return accepted

# define number of samples
num_samples = 1000

# fill the samples arrays with samples from the generators
samples_arm = [generate_demand_arm() for i in range(num_samples)]
    
# count the number of each demand: use a generator expression to count the
# number of samples which match each demand level i
counts_arm = np.array([sum(samples_arm==i) for i in demands])
frequency_arm = counts_arm/np.sum(counts_arm)

# create a new figure recreating the PMF bar plot
plt.figure()
bar_width = 0.3
plt.bar(demands, pmf, bar_width, align='center', color='k', label='Observed')
# also display the generated frequency (offset bars by bar_width)
plt.bar(demands+bar_width, frequency_arm, 
        bar_width, color='g', label='Generated (ARM)')
plt.ylabel('p(x)')
plt.ylim([0,1])
plt.xlabel('Coffee Demand (x)')
plt.title('Cafe Java Demand Process Generator Results (n={})'.format(num_samples))
plt.xticks(demands + bar_width, labels)
plt.legend()