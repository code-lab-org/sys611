"""
Example: Cafe Java Arrival Time Distribution and Process Generator.

This example develops a continuous process generator for arrival times 
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

# import the scipy stats package and refer to it as `stats`
# see http://docs.scipy.org/doc/scipy-0.14.0/reference/stats.html for docs
import scipy.stats as stats

_lambda = 1/2 # customers per minute

# define a linear space between 0 and 10
plot_x = np.linspace(0,10)
# define PDF and CDF functions from derived formulas
pdf = _lambda*np.exp(-_lambda*plot_x)
cdf = 1-np.exp(-_lambda*plot_x)

# create a new figure for a PDF plot
plt.figure()
# plot the PDF using a blue line (-b)
plt.plot(plot_x, pdf, '-b')
# plot the PDF using the built-in function using a dashed black line (--k)
plt.plot(plot_x, stats.expon.pdf(plot_x, scale=1./_lambda), '--k')
plt.xlabel('Inter-arrival Time x (minutes)')
plt.ylabel('f(x)')
plt.title('PDF for Cafe Java Inter-arrival Time')

# create a new figure for a CDF plot
plt.figure()
# plot the CDF using a blue line (-b)
plt.plot(plot_x, cdf, '-b')
# plot the CDF using the built-in function using a dashed black line (--k)
plt.plot(plot_x, stats.expon.cdf(plot_x, scale=1./_lambda), '--k')
plt.xlabel('Inter-arrival Time x (minutes)')
plt.ylabel('F(x)')
plt.title('CDF for Cafe Java Inter-arrival Time')

# define a function to compute arrival times using inverse transform method
def generate_arrival_ivt():
    """Generates an arrival time following the inverse transform method.
    
    Returns:
        arrival (float): the time until the next arrival    
    """
    r = np.random.rand()
    return -np.log(1-r)/_lambda
    """
    note: the code above could be replaced with the built-in process generator:
    
    return np.random.exponential(1/_lambda)
    """

# define number of samples
num_samples = 1000

# fill the samples arrays with samples from the generators
samples_ivt = [generate_arrival_ivt() for i in range(num_samples)]

# create a new figure to display a histogram of results
plt.figure()
# plot a histogram of samples, using bins between 0 and 10
plt.hist(samples_ivt, bins=range(10), color='blue', label='IVT Samples')
# overlay a plot of the theoretical number of samples computed from PDF
plt.plot(plot_x, stats.expon.pdf(plot_x, scale=1./_lambda)*num_samples,
         '-k', label='Theoretical')
plt.xlabel('Inter-arrival Time Bin (minutes)')
plt.ylabel('Count')
plt.title('Histogram for Inter-arrival Time Samples (n={})'.format(num_samples))
plt.legend()