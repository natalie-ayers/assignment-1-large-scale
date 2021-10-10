import numpy as np
import scipy.stats as sts
import time
from life_loop import loop_lifetimes

t0 = time.time()

# Set model parameters
rho = 0.5
mu = 3.0
sigma = 1.0
z_0 = mu

# Set simulation parameters, draw all idiosyncratic random shocks,
# and create empty containers
S = 1000 # Set the number of lives to simulate
T = int(4160) # Set the number of periods for each simulation
np.random.seed(25)
eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
z_mat = np.zeros((T, S))

z_mat = loop_lifetimes(S, T, z_0, rho, mu, eps_mat, z_mat)

time_elapsed = time.time() - t0

print("Simulated %d Lifecycles: %f seconds with numba pre-compilation" \
                % (S, time_elapsed))