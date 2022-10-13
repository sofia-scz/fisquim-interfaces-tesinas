import os
import numpy as np
import ase.io
from ase.visualize import view as ase_view
from dscribe.descriptors import ACSF
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

# behler simmetry function descriptor
acsf = ACSF(
    species=["Ni", "H", "C"],
    rcut=6.5,
    g2_params=[[1, 1], [1, 2], [1, 3]],
    g4_params=[[1, 1, 1], [1, 2, 1], [1, 1, -1], [1, 2, -1]],
)


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

        # load ase atoms
        aux_poscarfile_path = os.path.join(source_path, self.h_key, 'aux')
        with open(aux_poscarfile_path, 'w') as poscar_auxfile:
            for line in self.new_poscar:
                poscar_auxfile.write(line)
        self.ase_atoms = ase.io.read(aux_poscarfile_path, format='vasp')
        os.remove(aux_poscarfile_path)

        # dscribe - dscribe methods
        self.behler_descriptor = acsf.create(self.ase_atoms)

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
err = 1e-8


# test fingerprints
def test_fingerprint(new_poscar, poslist):
    # get behler array
    arr1 = new_poscar.behler_descriptor.copy()
    for poscar in poslist:
        arr2 = poscar.behler_descriptor.copy()
        if np.allclose(arr1, arr2, atol=err):
            return False
    return True


# start poscars batch
def make_poscar_batch():
    batch = []
    for h_key in poscars_dict:
        for t_key in translations:
            for r_key in rotations:
                new_poscar = Poscar(h_key, t_key, r_key)
                if test_fingerprint(new_poscar, batch):
                    batch.append(new_poscar)
    return batch
