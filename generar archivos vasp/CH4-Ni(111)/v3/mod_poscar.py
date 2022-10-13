import numpy as np

# CH4 lines
n0, nf = 45, 50
# h1, h2, h3, h4, c = range(n0, nf)


# aux pass array as float array
def pass_array(array):
    return np.asarray(array, dtype='float64')


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
    return new_coords, new_poscar
