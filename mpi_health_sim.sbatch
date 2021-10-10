#!/bin/bash

#SBATCH --job-name=mpi_health_sim
#SBATCH --ntasks=210
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30123

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun
for i in {1..20} 
do 
    mpirun -n $i python3 mpi_health_sim.py >> mpi_health_sim.out
done
