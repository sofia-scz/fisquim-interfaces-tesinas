import os
import numpy as np
import ase.io
from ase.visualize import view
from utils import (copy_files, load_poscars, mod_poscar, a, h,
                   compute_nih_distances)

##############################################################################
#               load & set up configs
##############################################################################

root = '..'

# load source files
source_path = os.path.join(root, 'vasp_source_top')
poscars_dict = load_poscars(source_path)  # folders 1h, 2h, 3h

# destination folder
dest_path = os.path.join(root, 'vasp_batch_dirs')

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
#               CH4/Ni config class
##############################################################################

class Config:
    def __init__(self, h_key, site_key, rot_key):
        # store keys
        self.h_key = h_key
        self.site_key = site_key
        self.rot_key = rot_key

        # label config
        self.label = h_key + '_' + site_key + '_' + rot_key

        # store old data
        self.old_poscar = poscars_dict[h_key].copy()

        # create new data
        self.new_poscar = mod_poscar(self.old_poscar,
                                     r=translations[site_key],
                                     M=rotations[rot_key])

        # create new dir
        self.path = os.path.join(dest_path, self.label)

        # ase atoms
        self.load_ase_atoms()

        # cart coordinates
        self.coords = self.ase_atoms.positions.copy()
        self.ch4_coords = self.coords[-5:].copy()

        # simmetry array
        self.setup_simmetry_array()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of __init__ method

    def load_ase_atoms(self):
        temp_dir = os.path.join(root, 'aux')
        with open(temp_dir, 'w') as poscar_auxfile:
            for line in self.new_poscar:
                poscar_auxfile.write(line)
        self.ase_atoms = ase.io.read(temp_dir, format='vasp')
        os.remove(temp_dir)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of ase atoms method

    def setup_simmetry_array(self):
        array = self.ch4_coords[:-1].copy()
        self.simmetry_array = compute_nih_distances(array)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~
        #       end of simmetry array method

    def makefolder(self):
        # copy all vasp files
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


def test_new_config(new_config, configlist):
    arr1 = new_config.simmetry_array
    for old_config in configlist:
        arr2 = old_config.simmetry_array
        if np.allclose(arr1, arr2, atol=err):
            return False
    return True


# batch
def make_configs_batch():
    batch = []
    for h_key in poscars_dict:
        step = []
        for t_key in translations:
            for r_key in rotations:
                new_config = Config(h_key, t_key, r_key)
                if test_new_config(new_config, step):
                    step.append(new_config)
        batch += step
    return batch
