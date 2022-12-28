#!/bin/bash
#SBATCH --partition=eth20
#SBATCH --job-name=GSRD              # Job name
#SBATCH --nodes=1                    # Run all processes on a single node
#SBATCH --ntasks=20                  # Run a single task
#SBATCH --tasks-per-node=20          # Use 20 cores per node
#SBATCH --time=24:00:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo "Running GSRD on $SLURM_NTASKS cores"

module load intel/2021b                         # version de intel
module load aenet/2.0.4-intel-2021b             # version de aenet

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/software/apps/software/aenet/2.0.4/lib/

EXE=$HOME/Software/bin/gsrd.x

mpirun -n $SLURM_NTASKS $EXE

