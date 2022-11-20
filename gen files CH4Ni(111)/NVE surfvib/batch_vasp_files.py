from os.path import join
from shutil import copytree


# copy files in folder
def copy_files(source, destination):
    copytree(source, destination, dirs_exist_ok=True)
    pass


source = 'source'
tebeg = [50, 100, 200, 300, 500, 700, 1000, 1400, 1650]
nt = len(tebeg)
potims, nws, nodes = [5]*nt, [800]*nt, [6]*nt
dest = 'batch'


def do_something():
    with open(join(source, 'INCAR'), 'r') as ff:
        incar = ff.readlines()

    with open(join(source, 'submit_vasp.sh'), 'r') as ff:
        vasp = ff.readlines()

    for i, t in enumerate(tebeg):
        newf = join(dest, f'{t}K')
        copy_files(source, newf)
        # mod sbatch
        vasp[4] = f'#SBATCH --nodes={nodes[i]} \n'
        vasp[5] = f'#SBATCH --ntasks={nodes[i]*16} \n'
        with open(join(newf, 'submit_vasp.sh'), 'w') as ff:
            for line in vasp:
                ff.write(line)

        # mod incar
        incar[17] = f' NSW = {nws[i]}\n'
        incar[19] = f' POTIM = {potims[i]}\n'
        incar[23] = f' TEBEG = {t}\n'
        with open(join(newf, 'INCAR'), 'w') as ff:
            for line in incar:
                ff.write(line)
        pass
