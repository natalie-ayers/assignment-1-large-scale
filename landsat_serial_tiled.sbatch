#!/bin/bash

#SBATCH --job-name=landsat_serial_tiled
#SBATCH --ntasks=2
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30123

# Load Python and MPI modules
module load cuda
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun
for i in {10,20}
do
    mpirun -n 1 python3 ./landsat_serial_tiled.py $i > ./landsat_serial_tiled.out 
done
