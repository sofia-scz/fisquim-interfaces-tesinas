import os
from v4.utils import copy_files, exc_states_load_poscar, mod_poscar, \
    exc_states_load_modes

modes_dict = exc_states_load_modes('')
old_poscar_dict = exc_states_load_poscar('')
dest_path = 'batch_vasp_dirs'

##############################################################################
#               config class
##############################################################################


class Config:
    def __init__(self, newposcar, label):
        self.newposcar = newposcar
        self.label = label

        # create new dir
        self.path = os.path.join(dest_path, self.label)

    def makefolder(self):


def batch_exc_states():
    for mode_key in modes_dict:
