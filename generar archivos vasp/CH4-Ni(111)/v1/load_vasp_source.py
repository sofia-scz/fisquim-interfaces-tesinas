import os
from shutil import copytree


# load default poscars
# top with vasp files for 1h 2h 3h approaches
def load_poscars(source_path):
    folders = [f.name for f in os.scandir(source_path) if f.is_dir()]
    data = {}
    for folder in folders:
        with open(os.path.join(source_path, folder, 'POSCAR'),
                  'r') as source_poscar:
            lines = source_poscar.readlines()
            data[folder] = lines
    return data


# copy all other files
def copy_files(source, destination):
    copytree(source, destination, dirs_exist_ok=True)
    pass
