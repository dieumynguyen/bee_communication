#!/bin/bash
#SBATCH -p short
#SBATCH --job-name=distbwworkers  # Job name
#SBATCH --mail-type=FAIL             # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=ding1018@colorado.edu
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --mem=500gb                # Memory limit
#SBATCH --time=24:00:00             # Time limit hrs:min:sec
#SBATCH --output=/scratch/Users/ding1018/eofiles_bw_workers/slurm_test_%j.out     # Standard output an$
#SBATCH --error=/scratch/Users/ding1018/eofiles_bw_workers/slurm_test_%j.err     # %j inserts job numb$

pwd; hostname; date

module load python/3.6.3

python /scratch/Users/ding1018/get_distance_bw_workers.py

date
