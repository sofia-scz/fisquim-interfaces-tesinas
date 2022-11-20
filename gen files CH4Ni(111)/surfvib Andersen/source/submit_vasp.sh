#!/bin/bash
#SBATCH --partition=ib16
#SBATCH --exclude=c12,c16
#SBATCH --job-name=svib_and          # Job name
#SBATCH --nodes=6                    # Number of nodes to be used
#SBATCH --ntasks=96                  # Total number of cores
#SBATCH --tasks-per-node=16          # Use 16 cores per node
#SBATCH --time=23:59:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo "Running VASP on $SLURM_CPUS_ON_NODE CPU cores"

module load VASP/5.4.4-SRP-intel-2021b                # version de vasp compilado con la funcional SRP de Leiden

EXE=vasp_std

mpirun -n $SLURM_NTASKS $EXE

rm CHG* D* E* IB* PC* R* va* W* X*

date

