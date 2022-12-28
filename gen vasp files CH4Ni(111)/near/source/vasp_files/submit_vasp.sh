#!/bin/bash
#SBATCH --partition=ib16
#SBATCH --job-name=CH4Ni             # Job name
#SBATCH --exclude=c[1-4],c9,c12,c15,c16,c25,c26
#SBATCH --nodes=2                    # Number of nodes to be used
#SBATCH --ntasks=32                  # Total number of cores
#SBATCH --tasks-per-node=16          # Use 16 cores per node
#SBATCH --time=01:00:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo "Running VASP on $SLURM_CPUS_ON_NODE CPU cores"

module load VASP/5.4.4-SRP-intel-2021b                # version de vasp compilado con la funcional SRP de Leiden

EXE=vasp_std

mpirun -n $SLURM_NTASKS $EXE

rm C* D* E* I* R* v* W* X* P* OS*

date

