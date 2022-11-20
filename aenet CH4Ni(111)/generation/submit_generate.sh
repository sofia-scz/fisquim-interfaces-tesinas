#!/bin/bash
#SBATCH --partition=eth20
#SBATCH --job-name=anet_gen          # Job name
#SBATCH --nodes=1                    # Number of nodes to be used
#SBATCH --ntasks=20                  # Total number of cores
#SBATCH --tasks-per-node=20          # Use 16 cores per node
#SBATCH --time=08:00:00              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo " "
echo "Calling aenet:"
echo " "

module load aenet/2.0.4-intel-2021b

EXE=generate.x-2.0.4-ifort_intelmpi

mpirun -n $SLURM_NTASKS $EXE generate.in > generate.out

# -------- NO NEED TO MODIFY THIS SECTION -------------------------------------
echo "END_TIME (success)   = `date +'%y-%m-%d %H:%M:%S %s'`"
END_TIME=`date +%s`
echo "RUN_TIME (hours)     = "`echo "$START_TIME $END_TIME" | awk '{printf("%.4f",($2-$1)/60.0/60.0)}'`

exit 0

