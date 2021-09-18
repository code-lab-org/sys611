# -*- coding: utf-8 -*-
"""
SYS-611 Continuous Time Models.

@author: Paul T. Grogan, pgrogan@stevens.edu
"""

# import the python3 behavior for importing, division, and printing in python2
from __future__ import absolute_import, division, print_function

# import the numpy package and refer to it as `np`
# see http://docs.scipy.org/doc/numpy/reference/ for documentation
import numpy as np

# import the matplotlib pyplot package and refer to it as `plt`
# see http://matplotlib.org/api/pyplot_api.html for documentation
import matplotlib.pyplot as plt

# import the scipy integrate package and refer to it as `integrate`
import scipy.integrate as integrate

#%% Euler integration example

def x(t): 
  return t

delta_t = 0.5
num_steps = int(5.0/delta_t)
q = np.zeros(num_steps + 1)
t = np.zeros(num_steps + 1)

q[0] = 5.0
t[0] = 0.0
for i in range(num_steps):
  q[i+1] = q[i] + delta_t*x(t[i])
  t[i+1] = t[i] + delta_t

plt.figure()
plt.plot(t, 5+t**2/2., '-k', label='Analytic Solution')
plt.step(t, q, '-r', where='post', label='Euler $\Delta t={:}$'.format(delta_t))
plt.xlabel('Time ($t$)')
plt.ylabel('Water Volume ($q$)')
plt.legend(loc='best')

#%% numerical integration example

# define the times to integrate over
t = np.linspace(0.0, 5.0)

# note: odeint requires a callable function dq/dt = f(q, t)
def dq_dt(q, t):
  return t

q = integrate.odeint(dq_dt, 5.0, t)

# create a plot to show various results
plt.figure()
plt.plot(t, 5+t**2/2., '-k', label='Analytic Solution')
plt.step(t, q, '-r', where='post', label='scipy.odeint')
plt.xlabel('Time, minutes ($t$)')
plt.ylabel('Water Volume, cubic meters ($q$)')
plt.legend(loc='best')