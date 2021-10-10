#!/bin/bash

#SBATCH --job-name=health_sim_numbacc
#SBATCH --ntasks=2
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30123

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun, using & to run jobs at the same time
mpirun -n 1 python3 ./compile_numba.py > ./health_sim_numbacc.out 
mpirun -n 1 python3 ./health_sim_numbacc.py > ./health_sim_numbacc.out 

# Wait until all simultaneous mpiruns are done
wait