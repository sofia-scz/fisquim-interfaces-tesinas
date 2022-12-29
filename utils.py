import os
from shutil import copytree
import numpy as np


##############################################################################
#               aux
##############################################################################

# pass array as float array
def pass_array(array):
    return np.asarray(array, dtype='float64')


##############################################################################
#               files handling
##############################################################################

# copy files in folder
def copy_files(source, destination):
    copytree(source, destination, dirs_exist_ok=True)
    pass


# load default poscars
# top with vasp files for 1h 2h 3h approaches
def load_poscars(source_path):
    folders = [f.name for f in os.scandir(source_path) if (f.is_dir() and f.name != 'vasp_files')]
    datadict = {}
    for folder in folders:
        with open(os.path.join(source_path, folder, 'POSCAR'),
                  'r') as source_poscar:
            lines = source_poscar.readlines()
            datadict[folder] = lines
    return datadict


##############################################################################
#               mod poscar
##############################################################################

# CH4 lines
n0, nf = 45, 50


# load CH4 positions array from poscar
def load_pos_array(poscar):
    poscar_copy = poscar.copy()
    coords = np.array([np.fromstring(line, sep='\t', count=3)
                      for line in poscar_copy[n0: nf]])
    return coords


# translation & CH bond stretching
def mod_array(array, h, b):
    result = pass_array(array).copy()

    # height
    if h is not None:
        result += (0, 0, h)

    # stretch CH bond
    if b is not None:
        i, a = b
        if i > 0 and i < 5:
            hpos, cpos = result[i-1], result[-1]
            v0 = (hpos - cpos)/np.linalg.norm(hpos - cpos)
            result[i-1] += v0*a
        elif i == 0:
            pass
        else:
            print(i)
            raise Exception('error trying to stretch C-H bonds.')

    return result


# format value
def format_value(x):
    out = f'{x:14.20f}'
    while out[0] == ' ':
        out = out[1:]
    while len(out) < 13:
        out += '0'
    while len(out) > 13:
        out = out[:-1]
    return out


# edit line string
def edit_line(vector):
    x, y, z = vector
    x, y, z = format_value(x), format_value(y), format_value(z)
    return '  '+x+'   '+y+'   '+z+'    T T T\n'


def mod_poscar(old_poscar, h=None, b=None, ni=None):
    # compute new coords
    old_coords = load_pos_array(old_poscar)
    new_coords = mod_array(old_coords, h, b)

    # edit old poscar
    new_poscar = old_poscar.copy()

    # CH4 lines
    for i in range(n0, nf):
        new_poscar[i] = edit_line(new_coords[i-n0])

    # Ni lines
    if ni:
        nid_vec = np.array([2.51442, 4.35509, 6.11523]) + (0, 0, ni)
        new_poscar[n0-1] = edit_line(nid_vec)

    return new_poscar
