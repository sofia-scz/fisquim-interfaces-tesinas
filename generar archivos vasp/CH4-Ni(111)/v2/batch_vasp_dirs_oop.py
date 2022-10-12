import os
import numpy as np
from load_vasp_source import load_poscars, copy_files
from mod_poscar import mod_poscar, load_pos_array

##############################################################################
#               load & set up configs
##############################################################################

root = '..'

# load source files
source_path = os.path.join(root, 'vasp_source_top')
poscars_dict = load_poscars(source_path)  # folders 1h, 2h, 3h

# destination folder
dest_path = os.path.join(root, 'vasp_batch_dirs')

# grid vectors
a, h = 7.54318932715/6, 6.53259358287/3

# translations
translations = {'top': (a, h, 0),
                'bridge': (1.5*a, .5*h, 0),
                'fcc': (a, h/3, 0),
                'hcp': (2*a, 2*h/3, 0),
                'top-bridge': (1.25*a, .75*h, 0),
                'top-fcc': (a, 2*h/3, 0),
                'top-hcp': (1.5*a, 5*h/6, 0)}


# rotations
# matrix acting on COLUMN vectors
def z_rotation_matrix(theta, deg=True):
    if deg:
        aaa = theta*np.pi/180
    else:
        aaa = theta.copy()
    return np.array([(np.cos(aaa), -np.sin(aaa), 0),
                     (np.sin(aaa), np.cos(aaa), 0),
                     (0, 0, 1)])


rotations = {}
for i in range(24):
    n = 15*i
    rotations[str(n)] = z_rotation_matrix(n)


##############################################################################
#               POSCAR class
##############################################################################
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


class Poscar:
    def __init__(self, h_key, site_key, rot_key):
        # store keys
        self.h_key = h_key
        self.site_key = site_key
        self.rot_key = rot_key

        # label poscar
        self.label = h_key + '_' + site_key + '_' + rot_key

        # store old data
        self.old_poscar = poscars_dict[h_key].copy()
        self.old_coords = load_pos_array(self.old_poscar)

        # create new data
        self.new_coords, self.new_poscar = mod_poscar(self.old_poscar,
                                                      r=translations[site_key],
                                                      M=rotations[rot_key])

        # create new dir
        self.path = os.path.join(dest_path, self.label)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of __init__ method

    def H_simmetry(self):
        array = self.new_coords[:-1].copy().round(decimals=8)
        return array[np.lexsort(np.transpose(array)[::-1])]
        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of H_simmetry method

    def makefolder(self):
        # copy all files
        source = os.path.join(source_path, self.h_key)
        copy_files(source, self.path)

        # modify poscar
        with open(os.path.join(self.path, 'POSCAR'), 'w') as poscar_newfile:
            for line in self.new_poscar:
                poscar_newfile.write(line)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of makefolder method

##############################################################################
#               BATCH poscars
##############################################################################

# test repeated configs ~~~~~~~~~~~~~~~~~


# error tolerance
err = 1e-6


# test repeated CH4 positions
def test_repeated_ch4pos(new_poscar, poslist):
    # get new poscar H coords
    arr1 = new_poscar.H_simmetry()
    for poscar in poslist:
        # get saved poscars H coords
        arr2 = poscar.H_simmetry()
        if np.allclose(arr1, arr2, atol=err):
            return True
    return False


# compute distances
def compute_distances(ch4_coords):
    d = []
    for ch4_atom in ch4_coords:
        for ni_atom in ni_atoms:
            d.append(np.linalg.norm(ni_atom - ch4_atom))
    return np.array(d).round(decimals=8)


def test_repeated_ch4_ni_distances(new_poscar, poslist):
    # get new poscar H coords
    arr1 = new_poscar.H_simmetry()
    arr1 = compute_distances(arr1)
    arr1 = arr1[np.lexsort(np.transpose(arr1)[::-1])]
    for poscar in poslist:
        # get saved poscars H coords
        arr2 = poscar.H_simmetry()
        arr2 = compute_distances(arr2)
        arr2 = arr2[np.lexsort(np.transpose(arr2)[::-1])]
        if np.allclose(arr1, arr2, atol=err):
            return True
    return False


def test_new_poscar(new_poscar, poslist):
    if not test_repeated_ch4_ni_distances(new_poscar, poslist):
        return True
    return False


# start poscars batch
def make_poscar_batch():
    batch = []
    for h_key in poscars_dict:
        for t_key in translations:
            for r_key in rotations:
                new_poscar = Poscar(h_key, t_key, r_key)
                if test_new_poscar(new_poscar, batch):
                    batch.append(new_poscar)
    return batch
