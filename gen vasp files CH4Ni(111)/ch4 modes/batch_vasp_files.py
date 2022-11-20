import os
import ase.io
from utils import copy_files, load_poscars, mod_poscar

##############################################################################
#               load & set up configs
##############################################################################

root = '.'

# load source files
source_path = os.path.join(root, 'source')
poscars_dict = load_poscars(source_path)  # folders mode1, .., mode9

# destination folder
dest_path = os.path.join(root, 'batch')

# translations
translation = (0, 2, -5)


##############################################################################
#               CH4/Ni config class
##############################################################################

class Config:
    def __init__(self, mode):
        # store keys
        self.mode = mode

        # label config
        self.label = mode

        # store old data
        self.old_poscar = poscars_dict[mode].copy()

        # create new data
        self.new_poscar = mod_poscar(self.old_poscar,
                                     r=translation,)

        # create new dir
        self.path = os.path.join(dest_path, self.label)

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
        source = os.path.join(source_path, 'vaspconfig')
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
    batch = []
    for mode in poscars_dict:
        new_config = Config(mode)
        batch.append(new_config)
    return batch


# do
def do_something():
    batch = make_configs_batch()
    for b in batch:
        b.makefolder()
    pass
