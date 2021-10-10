from mpi4py import MPI
import numpy as np
import scipy.stats as sts
from life_loop import loop_lifetimes
import time


def sim_lifetimes_mpi():

    # Get rank of process and overall size of communicator:
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    t0 = time.time()

    # Set model parameters
    rho = 0.5
    mu = 3.0
    sigma = 1.0
    z_0 = mu

    # Set simulation parameters, draw all idiosyncratic random shocks,
    # and create empty containers
    # Evenly distribute number of simulation runs across processes
    S = int(1000 / size) # Set the number of lives to simulate
    T = int(4160) # Set the number of periods for each simulation

    np.random.seed(rank)

    eps_mat = sts.norm.rvs(loc=0, scale=sigma, size=(T, S))
    z_mat = np.zeros((T, S))

    z_mat = loop_lifetimes(S, T, z_0, rho, mu, eps_mat, z_mat)

    time_elapsed = time.time() - t0
  
    print(rank, size, S, time_elapsed)

    return

def main():
    sim_lifetimes_mpi()

if __name__ == '__main__':
    main()