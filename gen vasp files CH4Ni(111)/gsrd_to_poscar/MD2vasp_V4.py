#!/usr/bin/env python3
import os
import argparse
import numpy as np
from ase.io import read, write
from shutil import copytree


# copy files in folder
def copy_files(source, destination):
    copytree(source, destination, dirs_exist_ok=True)
    pass


###################################################################################################
parser = argparse.ArgumentParser(description='''This script finds all the GSRD output files
                                 contained in folder, and writes VASP files suitable for
                                 recalculating with DFT''',
                                 allow_abbrev=True)

# Set the arguments we want to implement
parser.add_argument("--dir", help="directory for the GSRD output files (def: current directory")
parser.add_argument("--extra", help="directory for extra source files other than the POSCAR, eg: "
                    "POTCAR (def: None")
parser.add_argument("--dest", help="destination directory (def: files_for_DFT")


# Apply the arguments so they can be used
args = parser.parse_args()

#
cwd = os.getcwd()
if args.dir:
    print(args.dir)
    base_dir = os.path.join(cwd, args.dir)
    print(f"Searching from {base_dir} directory")
else:
    base_dir = cwd
    print(f"Searching from current directory: {base_dir}")

if args.extra:
    print(args.extra)
    extras = os.path.join(cwd, args.extra)
    print(f"Copying extras from {extras} directory")
else:
    extras = None

if args.dest:
    print(args.dest)
    dest = os.path.join(cwd, args.dest)
    print(f"Saving everything to {dest} directory")
else:
    dest = os.path.join(cwd, "files_for_DFT")

try:
    os.makedirs(dest)
except OSError:
    print(f"Creation of the directory {dest} failed")

###################################################################################################
dft_cell = [[7.5431893271500003,  0.0000000000000000,   0.0000000000000000],
            [-3.7715946635700002, 6.5325935828699997,   0.0000000000000000],
            [0.0000000000000000,  0.0000000000000000,  22.1152300000000000]]

###################################################################################################

E_ref = np.loadtxt(os.path.join(base_dir, 'refstructureFF_eneroptim.out'), usecols=1)[-1]

conf_files = ['config_probl.xyz', 'config_stick.xyz',
              'config_sticklate.xyz', 'config_stickearly.xyz', 'config_stickpat.xyz']
traj_files = ['traj_probl.out', 'traj_stick.out',
              'traj_sticklate.out', 'traj_stickearly.out', 'traj_stickpat.out']

numfiles = 1
for t_file, c_file in zip(traj_files, conf_files):

    #########################################################################################
    # Es estos if se deben poner las condiciones que debe cumplir la trayectoria
    # para ser seleccionada.
    #
    # El parametro usecols debe coincidir con la columna que tiene la energia
    # potencial en el archivo traj_XXXXX.out (recordar que en python los indices empiezan en
    # cero, asi que para columna 5 -> usecols=4)
    #
    # cond es la condicion que se debe cumplir para ser seleccionada, por ejemplo que v>2.0 eV
    #
    # Los archivos que no tienen un bloque especifico, se seleccionana todas las confs.
    # por ejemplo, de traj_probl.out se seleccionan todas para calcular por DFT
    #
    if (t_file == 'traj_admol.out'):
        try:
            atoms = read(os.path.join(base_dir, c_file), index=':', format='xyz')
            v, vint = np.loadtxt(os.path.join(base_dir, t_file), usecols=(4, 5), unpack=True)
        except OSError:
            continue
#        cond = np.logical_or( v > 2.0, vint < -0.5 )
        cond = np.full(len(atoms), True, dtype=bool)

    elif (t_file in ['traj_stick.out', 'traj_sticklate.out', 'traj_stickearly.out', 'traj_stickpat.out']):
        try:
            atoms = read(os.path.join(base_dir, c_file), index=':', format='xyz')
            v = np.loadtxt(os.path.join(base_dir, t_file), usecols=6)
        except OSError:
            continue
#        cond = v > 2.0
        cond = np.full(len(atoms), True, dtype=bool)

    elif (t_file == 'traj_refl.out'):
        try:
            atoms = read(os.path.join(base_dir, c_file), index=':', format='xyz')
            v = np.loadtxt(os.path.join(base_dir, t_file), usecols=4)
        except OSError:
            continue
#        cond = v > 2.0
        cond = np.full(len(atoms), True, dtype=bool)
    else:
        try:
            atoms = read(os.path.join(base_dir, c_file), index=':', format='xyz')
        except OSError:
            continue
        v = np.loadtxt(os.path.join(base_dir, t_file), usecols=5)
        cond = np.full(len(atoms), True, dtype=bool)
    print('{}: {}'.format(t_file, cond))

    #########################################################################################

    # Aca se escriben los POSCAR correspondientes
    for ind in np.arange(len(atoms)):
        if cond[ind]:
            atoms[ind].set_cell(dft_cell)
            atoms[ind].translate([0.0, 0.0, -atoms[ind][0].z])
            output_dir = os.path.join(dest, f"conf{numfiles}")
            try:
                os.makedirs(output_dir)
            except OSError:
                print(f"Creation of the directory {output_dir} failed")
            poscar_file = os.path.join(output_dir, "POSCAR")

            if (v.size > 1):
                label = f'# ann energy = {v[ind]+E_ref} eV'
            else:
                label = f'# ann energy = {v+E_ref} eV'
            write(poscar_file, atoms[ind], label=label, format='vasp', vasp5=True)

            # copy extra files
            if extras:
                copy_files(extras, output_dir)

            numfiles += 1
