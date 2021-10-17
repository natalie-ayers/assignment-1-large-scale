from mpi4py import MPI
import numpy as np
import scipy.stats as sts
from rho_loop import loop_rho_vals
import time


def test_rho_effects():

    # Get rank of process and overall size of communicator:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    t0 = time.time()

    # Set model parameters
    rho_arr = np.linspace(-0.95, 0.95, num=200)
    mu = 3.0
    sigma = 1.0
    z_0 = mu

    # Set simulation parameters, draw all idiosyncratic random shocks,
    # and create empty containers
    # Evenly distribute number of simulation runs across processes
    rho_rank = rho_arr[rank:rank+20]
    S = int(1000) # Set the number of lives to simulate
    T = int(4160) # Set the number of periods for each simulation

    np.random.seed(0)

    eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
    z_mat = np.zeros((T, S))
    rho_mat = np.zeros((len(rho_rank),2))

    rho_mat = loop_rho_vals(S, T, z_0, rho_rank, mu, eps_mat, z_mat, rho_mat)

    time_elapsed = time.time() - t0
    
    print('rank, size, num_lives (S), time_elapsed, rho_mat')
    print(rank, size, S, time_elapsed, rho_mat)
