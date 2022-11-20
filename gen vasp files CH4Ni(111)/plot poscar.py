import ase.io
from ase.visualize import view

atoms = ase.io.read('POSCAR', format='vasp')
view(atoms)
