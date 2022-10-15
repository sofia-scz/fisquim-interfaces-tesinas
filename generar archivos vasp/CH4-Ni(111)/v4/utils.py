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
    folders = [f.name for f in os.scandir(source_path) if f.is_dir()]
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
# h1, h2, h3, h4, c = range(n0, nf)


# load CH4 positions array from poscar
def load_pos_array(poscar):
    poscar_copy = poscar.copy()
    coords = np.array([np.fromstring(line, sep='\t', count=3)
                      for line in poscar_copy[n0: nf]])
    return coords


# translation & rotation of array
def mod_array(array, r, M):
    result = pass_array(array).copy()

    # rotation
    if M is not None:
        # assert M is rotation matrix
        assert abs(np.linalg.det(M)-1) < 1e-14, ('rotation matrix has non 1 de'
                                                 'terminant')
        # perform the rotation
        Hs, C = pass_array(array[:-1]).copy(), pass_array(array[-1]).copy()
        Hs -= C
        Hs = M.dot(Hs.transpose()).transpose() + C
        result[:-1] = Hs

    # translation
    if r is not None:
        result += r

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
def edit_line(line, vector):
    x, y, z = vector
    x, y, z = format_value(x), format_value(y), format_value(z)
    return '  '+x+'   '+y+'   '+z+'    T T T\n'


def mod_poscar(old_poscar, r=None, M=None):
    # compute new coords
    old_coords = load_pos_array(old_poscar)
    new_coords = mod_array(old_coords, r, M)

    # edit old poscar
    new_poscar = old_poscar.copy()
    for i in range(n0, nf):
        new_poscar[i] = edit_line(new_poscar[i], new_coords[i-n0])
    return new_poscar


##############################################################################
#                simmetry tests
##############################################################################
a, h = 7.54318932715/6, 6.53259358287/3

# data for testing simmetries
x0, y0, z0 = 1.25718, 2.17739, 6.1155
z1, z2 = 4.0834, 2.0332
ni00 = (x0, y0, z0)
ni01 = (x0+2*a, y0, z0)
ni02 = (x0+a, y0+h, z0)
ni03 = (x0+3*a, y0+h, z0)
ni10 = (x0+a, y0+h/3, z1)
ni20 = (x0+2*a, y0+2*h/3, z2)
ni_atoms = np.array([ni00, ni01, ni02, ni03, ni10, ni20])


# compute distances
def compute_nih_distances(h_coords):
    h_array = h_coords.astype('float32')
    sorted_h_coords = h_array[np.lexsort(h_array.transpose()[::-1])]
    d = []
    for h_atom in sorted_h_coords:
        for ni_atom in ni_atoms:
            d.append(np.linalg.norm(ni_atom - h_atom))
    d = np.array(d, dtype='float32')
    d.sort()
    return d
