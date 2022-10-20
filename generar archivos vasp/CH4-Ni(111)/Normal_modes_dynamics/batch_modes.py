import os
from v4.utils import copy_files, exc_states_load_poscar, mod_poscar, \
    exc_states_load_modes

modes_dict = exc_states_load_modes('')
old_poscar_dict = exc_states_load_poscar('source_modes')
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
        # copy all vasp files
        copy_files('source_modes', self.path)

        # modify poscar
        with open(os.path.join(self.path, 'POSCAR'), 'w') as poscar_newfile:
            for line in self.newposcar:
                poscar_newfile.write(line)
        pass


def batch_exc_states():
    oldposcar = old_poscar_dict['source']
    for mode_key in modes_dict:
        new_config = Config(mod_poscar(oldposcar,
                                       n0=45,
                                       m=.09*modes_dict[mode_key]),
                            mode_key)
        new_config.makefolder()
    pass
