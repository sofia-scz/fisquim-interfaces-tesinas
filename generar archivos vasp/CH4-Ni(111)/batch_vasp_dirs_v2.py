import os
import numpy as np
from load_vasp_source import load_poscars, copy_files
from mod_poscar import mod_poscar

# folders are 1h, 2h, 3h

#          POSCAR CH4 initial values EDITS       ~~~~~~~~~~~~~~~~~~

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


rotations = {'0': z_rotation_matrix(0),
             '15': z_rotation_matrix(15),
             '30': z_rotation_matrix(30),
             '45': z_rotation_matrix(45)}


#               CREATE NEW FOLDERS ~~~~~~~~~~~~~~~~~~~
def make_folders(source_path, ouput_path, translation_dict, rotation_dict):
    root = '.'
    # load source files
    poscars_dict = load_poscars(source_path)

    for h_key in poscars_dict:
        old_poscar = poscars_dict[h_key]
        for t_key in translations:
            for r_key in rotations:

                # def path & folder name
                new_dir_name = h_key+'_'+t_key+'_'+r_key+'deg'
                path = os.path.join(root, ouput_path, new_dir_name)

                # copy all files in source
                source = os.path.join(root, source_path, h_key)
                copy_files(source, path)

                # get new POSCAR
                new_poscar = mod_poscar(old_poscar, r=translations[t_key],
                                        M=rotations[r_key])

                # save new POSCAR
                with open(os.path.join(path, 'POSCAR'), 'w') as poscar_newfile:
                    for line in new_poscar:
                        poscar_newfile.write(line)
    pass


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rotations_2h = {'60': z_rotation_matrix(60),
                '75': z_rotation_matrix(75),
                '90': z_rotation_matrix(90),
                '105': z_rotation_matrix(105),
                '120': z_rotation_matrix(120),
                '135': z_rotation_matrix(135),
                '150': z_rotation_matrix(150),
                '165': z_rotation_matrix(165)}
