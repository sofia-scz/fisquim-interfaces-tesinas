import os
import argparse
from glob import glob
from ase.io import read

###################################################################################################


def write_xsf(xsfile, atoms):
    """Create an aenet compatible xsf from an atoms object.
       This function was taken from aenet package.

    Parameters
    ----------
    xsfile : string
        Filename to write xsf file to

    atoms : ase.Atoms
        an ase atoms object with an attached calculator to get energy and
        forces.

    Returns
    -------
    output : string
        The string written to the file.
    """
    energy = atoms.get_potential_energy()
    forces = atoms.get_forces()

    xsf = ['# total energy = {} eV'.format(energy), '']

    if True in atoms.pbc:
        xsf += ['CRYSTAL', 'PRIMVEC']
        for v in atoms.get_cell():
            xsf += ['{} {} {}'.format(*v)]
        xsf += ['PRIMCOORD', '{} 1'.format(len(atoms))]

    else:
        xsf += ['ATOMS']

    S = ('{atom.symbol:<3s} {atom.x: .12f} {atom.y: .12f} {atom.z: .12f}'
         ' {f[0]: .12f} {f[1]: .12f} {f[2]: .12f}')
    xsf += [S.format(atom=atom, f=forces[i]) for i, atom in enumerate(atoms)]

    output = '\n'.join(xsf)

    base, fname = os.path.split(xsfile)

    if not os.path.isdir(base):
        os.makedirs(base)

    with open(xsfile, 'w') as f:
        f.write(output)

    return output


###################################################################################################
parser = argparse.ArgumentParser(description='''This script finds all the OUTCAR files contained
                                              in tgz, and writes the energy and configuration
                                   into a configs.in file suitable for GSRD fitting''',
                                 allow_abbrev=True)

# Set the arguments we want to implement
parser.add_argument(
    "--dir", help="base directory for the resursive search of VASP output files (default: current "
    "directory")
parser.add_argument(
    "--output", help="name for the output file (default: config.out)")
parser.add_argument(
    "--first_file", help="number for the first file ###.xsf (default: 0")


# Apply the arguments so they can be used
args = parser.parse_args()

# Set the folder from which tgz files will be searched recursively
if args.dir:
    print(args.dir)
    base_dir = os.path.expanduser(args.dir)
    print("Searching from {} directory".format(base_dir))
else:
    base_dir = os.getcwd()
    print("Searching from current directory: {}".format(base_dir))

# Set the name of the output file received as argument
if args.output:
    outfile = str(args.output)
    print("Output file name set to: {}".format(outfile))
else:
    outfile = "xsf-files"
    print("Using default name for output file: {}".format(outfile))

# Set the initial number for xsf file
if args.first_file:
    numfiles = int(args.first_file)
else:
    numfiles = 0
###################################################################################################

outcar_files = [y for x in os.walk(base_dir)
                for y in glob(os.path.join(x[0], 'OUTCAR'))]
print(sorted(outcar_files))
for file in sorted(outcar_files):  # loop over the list of outcar files
    # load OUTCAR file using ASE module
    atoms = read(file, index=':', format="vasp-out")
    # write the configs.xsf files
    for count in range(len(atoms)):
        outname = os.path.join(
            outfile, "{}.xsf".format(str(numfiles).zfill(5)))
        write_xsf(outname, atoms[count])
        numfiles += 1
