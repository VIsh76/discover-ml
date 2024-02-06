#!/bin/sh

#SBATCH --account g0613
##SBATCH --qos=debug
#SBATCH --job-name=ml-physics
#SBATCH --output=ml-physics.o%j
#SBATCH --ntasks-per-node=40
#SBATCH --nodes=4
#SBATCH --time=08:00:00

python3.6 main_phys.py > run_phys_20240126.log
