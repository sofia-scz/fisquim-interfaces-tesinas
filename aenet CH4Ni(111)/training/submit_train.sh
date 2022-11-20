#!/bin/bash
#SBATCH --partition=ib16
#SBATCH --exclude=c9,c15,c12,c16
#SBATCH --job-name=anet_tra          # Job name
#SBATCH --nodes=8                    # Number of nodes to be used
#SBATCH --ntasks=128                 # Total number of cores
#SBATCH --tasks-per-node=16          # Use 16 cores per node
#SBATCH --time=23:59:50              # Time limit hrs:min:sec
#SBATCH --output=parallel_%j.log     # Standard output and error log
pwd; hostname; date

echo " "
echo "Calling aenet:"
echo " "

module load aenet/2.0.4-intel-2021b

EXE=train.x-2.0.4-ifort_intelmpi

mpirun -n $SLURM_NTASKS $EXE train.in > train.out

## Generar los archivos con la energia DFT y NN
cat energies.train.* > energies.train
cat energies.test.* > energies.test
rm energies.t*.*
sed -i '/Ref/d' energies.train
sed -i '/Ref/d' energies.test

## Generar archivo con datos de convergencia
if [ -f "convergence.dat" ]; then
    grep "<" train.out >> convergence.dat
else
    grep "<" train.out > convergence.dat
fi

## Mover los archivos con las redes a una carpeta NNs
if [ ! -d "NNs" ]; then
    mkdir NNs
fi
cp *.ann   NNs
mv *.ann-?0000 NNs
rm *.ann-* NNs


# -------- NO NEED TO MODIFY THIS SECTION -------------------------------------
echo "END_TIME (success)   = `date +'%y-%m-%d %H:%M:%S %s'`"
END_TIME=`date +%s`
echo "RUN_TIME (hours)     = "`echo "$START_TIME $END_TIME" | awk '{printf("%.4f",($2-$1)/60.0/60.0)}'`

exit 0

