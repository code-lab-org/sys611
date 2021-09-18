# -*- coding: utf-8 -*-
"""
SYS-611: Example Conditional Exponential Distribution

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np
# import the matplotlib.pyplot package and refer to it as `plt`
import matplotlib.pyplot as plt
# import the scipy.stats package and refer to it as `stats`
import scipy.stats as stats

_lambda = 1.0 # average event rate (things per time)

# define number of samples and use built-in process generator
num_samples = 1000
samples = np.random.exponential(scale=1/_lambda, size=num_samples)

# create plot
fig, ax1 = plt.subplots()
# plot histogram of samples
plt.hist(samples, color='r')
# create a second plotting axis
ax2 = ax1.twinx()
ax2.set_ylim([0,_lambda])
# plot the PDF of the generating distribution up to the 99.99th percentile point
t = np.linspace(0,stats.expon.ppf(0.9999, scale=1/_lambda))
ax2.plot(t, stats.expon.pdf(t, scale=1/_lambda), '--k', label='PDF $f(t)$')
# add title and labels
plt.title('Samples of $t\sim{{exponential}}(\lambda={:.1f})$'.format(_lambda))
ax1.set_xlabel('Time ($t$)')
ax1.set_ylabel('Observed Sample Relative Frequency')
plt.legend(loc='best')

#%%

# define the cutoff time for conditional samples
cutoff_time = 2.0

# create plot
fig, ax1 = plt.subplots()
# plot histogram of samples after cutoff time
plt.hist(samples[samples > cutoff_time], color='r')
# create a second plotting axis
ax2 = ax1.twinx()
ax2.set_ylim([0,_lambda])
# plot the PDF of the generating distribution up to the 99.99th percentile point
t = np.linspace(0,stats.expon.ppf(0.9999, scale=1/_lambda))
ax2.plot(t+cutoff_time, stats.expon.pdf(t, scale=1/_lambda), '--k', label='PDF $f(t-{:.1f})$'.format(cutoff_time))
# add title and labels
plt.title('Samples of $t>{:.1f}$'.format(cutoff_time))
ax1.set_xlabel('Time ($t$)')
ax1.set_ylabel('Observed Sample Relative Frequency')
plt.legend(loc='best')