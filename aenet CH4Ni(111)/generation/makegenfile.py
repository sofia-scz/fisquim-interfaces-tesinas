import os
from datetime import date

xsf_files = [f.path for f in os.scandir('xsf-files') if not f.is_dir()]
xsf_files.sort()
count = len(xsf_files)

text = f"""OUTPUT    CH4Ni_{date.today().strftime("%d-%m-%Y")}.train

TYPES
3
Ni     0.0000000000     !  eV
H      0.0000000000     !  eV
C      0.0000000000     !  eV

SETUPS
Ni     fingerprint/Ni.stp
H      fingerprint/H.stp
C      fingerprint/C.stp

FILES
{count}
"""

with open('generate.in', 'w') as outfile:
    outfile.write(text)
    for ff in xsf_files:
        outfile.write(ff+'\n')

