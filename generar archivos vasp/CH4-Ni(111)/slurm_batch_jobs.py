import os

filename = 'submit_jobs.sh'
with open(filename, 'w') as ff:
    ff.write('#!/bin/bash\n')
    subfolders = [f.path for f in os.scandir('.') if f.is_dir()]
    for sf in subfolders:
        ff.write(f'(cd {sf} && sbatch submit_vasp.sh)\n')
