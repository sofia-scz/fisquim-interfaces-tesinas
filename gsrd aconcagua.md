# GSRD en Aconcagua

Descargar la carpeta `gsrd-aconcagua`

## Compilado

1. Extraer el tar 'gsrd' en home. Deberían quedar los directorios 'gsrd/gsrd-2.1.2'.
2. En 'gsrd-2.1.2' mover, renombrar o eliminar los 'Makefile_*' existentes, y traer el 'Makefile_mpiifort' que estaba en la descarga.
3. Correr la sentencia `module load intel/2021b` y luego `make -f Makefile_mpiifort`.

El programa debería haber sido compilado. En home crear un directorio 'Software/bin' y mover 'gsrd.x' dentro. 

## Uso

Mover los contenidos de 'gsrd-2.1.2/Sample_imput/ANN' al directorio donde se desea trabajar, y a este mismo directorio agregar el 'submit_gsrd.sh'
que estaba en la descarga.

Correr 'submit_gsrd.sh' con SBATCH.
