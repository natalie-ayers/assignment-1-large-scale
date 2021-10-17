#!/bin/bash

#SBATCH --job-name=landsat_serial
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30123

# Load Python and MPI modules
module load cuda
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun
mpirun -n 1 python3 ./landsat_serial.py > ./landsat_serial.out 
