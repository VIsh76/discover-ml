#!/bin/sh

#SBATCH --account g0613
##SBATCH --qos=debug
#SBATCH --job-name=ml-physics
#SBATCH --output=ml-physics.o%j
#SBATCH --ntasks-per-node=40
#SBATCH --nodes=4
#SBATCH --time=08:00:00

python3.6 main.py

salloc --account g0613 ---partition=gpu_a100 --constraint=rome -job-name=test_ml_gpu --qos=debug --time=00:30:00

