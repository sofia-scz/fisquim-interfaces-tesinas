import os
import numpy as np
import ase.io
from utils import copy_files, load_poscars, mod_poscar

##############################################################################
#               load & set up configs
##############################################################################

root = '.'

# load source files
source_path = os.path.join(root, 'source')
poscars_dict = load_poscars(source_path)  # folders

# destination folder
dest_path = os.path.join(root, 'batch')

# heights
hcm = .3
heights = {'CMref': .0,
           'CMup': hcm,
           'CMdown': -hcm, }

# bonds
c, p1, p2 = -.2, .2, .3
bonds = {'Beq': (0, 0),
         'Bcomp1': (1, c),
         'Bcomp2': (2, c),
         'Bcomp3': (3, c),
         'Bcomp4': (4, c),
         'Bpull1': (1, p1),
         'Bpull2': (2, p1),
         'Bpull3': (3, p1),
         'Bpull4': (4, p1),
         'BPULL1': (1, p2),
         'BPULL2': (2, p2),
         'BPULL3': (3, p2),
         'BPULL4': (4, p2),
         }

# nidis
hni = .1
nidis = {'NIeq': 0,
         'NIup': hni,
         'NIdown': -hni,
         'NIDOWN': -2*hni, }


##############################################################################
#               CH4/Ni config class
##############################################################################

class Config:
    def __init__(self, s_key, height_key, bond_key, nidis_key):
        # store keys
        self.s_key = s_key

        # label config
        self.label = s_key + '_' + height_key + '_' + bond_key + '_' + nidis_key

        # store old data
        self.old_poscar = poscars_dict[s_key].copy()

        # create new data
        self.new_poscar = mod_poscar(self.old_poscar,
                                     h=heights[height_key],
                                     b=bonds[bond_key],
                                     ni=nidis[nidis_key])

        # create new dir
        self.path = os.path.join(dest_path, self.label)

        # ase atoms
        self.load_ase_atoms()

        # cart coordinates
        self.coords = self.ase_atoms.positions.copy()
        self.ch4_coords = self.coords[-5:].copy()

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

    def makefolder(self):
        # copy all vasp files
        source = os.path.join(source_path, 'vasp_files')
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


# batch
def make_configs_batch():
    for s_key in poscars_dict:
        for h_key in heights:
            for b_key in bonds:
                for ni_key in nidis:
                    new_config = Config(s_key, h_key, b_key, ni_key)
                    new_config.makefolder()
    pass
