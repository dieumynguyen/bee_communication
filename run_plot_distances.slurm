#!/bin/bash
#SBATCH -p short
#SBATCH --job-name=plot_distances  # Job name
#SBATCH --mail-type=ALL             # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=ding1018@colorado.edu
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --mem=500gb                # Memory limit
#SBATCH --time=24:00:00             # Time limit hrs:min:sec
#SBATCH --output=/Users/ding1018/bee_communication_project/eofiles_plot_distances/slurm_test_%j.out     # Standard output and error log
#SBATCH --error=/Users/ding1018/bee_communication_project/eofiles_plot_distances/slurm_test_%j.err	   # %j inserts job number

pwd; hostname; date

module load python/3.6.3

python /Users/ding1018/bee_communication_project/plot_distances.py

date
