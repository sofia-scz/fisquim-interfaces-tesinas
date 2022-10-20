#!/bin/bash
#SBATCH --partition=ib16
#SBATCH --job-name=CH4Ni111          # Job name
#SBATCH --nodes=2                    # Number of nodes to be used
#SBATCH --ntasks=32                  # Total number of cores
#SBATCH --tasks-per-node=16          # Use 16 cores per node
#SBATCH --time=02:00:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo "Running VASP on $SLURM_CPUS_ON_NODE CPU cores"

##module use /opt/software/apps/modules/all
####module load VASP/5.4.4-18Apr17-p01-intel-2021b    # version estandard de vasp
module load VASP/5.4.4-SRP-intel-2021b                # version de vasp compilado con la funcional SRP de Leiden

EXE=vasp_std

#mpirun -n $SLURM_CPUS_ON_NODE $EXE
mpirun -n $SLURM_NTASKS $EXE

date

