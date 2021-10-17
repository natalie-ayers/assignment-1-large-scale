#!/bin/bash

#SBATCH --job-name=mpi_rho_tests_numbacc
#SBATCH --ntasks=2
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30123

# Load Python and MPI modules
module load cuda
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun, using & to run jobs at the same time
mpirun -n 1 python3 ./compile_numba_rho_loop.py > ./mpi_rho_tests_numbacc.out 
mpirun -n 1 python3 ./mpi_rho_tests_numbacc.py > ./mpi_rho_tests_numbacc.out 

# Wait until all simultaneous mpiruns are done
wait