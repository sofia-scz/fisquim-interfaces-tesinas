import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import AutoMinorLocator

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#e8e', '#95c', '#38e', '#3bb', '#395', '#dc2', '#fa3',
          '#e63', '#c33', '#865']


def file_to_array(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        lines = [float(line[76:87]) for line in lines]
    return np.array(lines)


files = ['greps/mode'+str(i) for i in range(1, 10)]

fig, ax = plt.subplots(1, 1, dpi=150, figsize=(7, 5))
for i, f in enumerate(files):
    arr = file_to_array(f)
    ax.plot(np.arange(len(arr))*.1, file_to_array(f), color=colors[i],
            label='mode '+str(i+1), lw=1.4)

ax.legend(loc='upper right', fontsize=8)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.tick_params(which='major', width=.8, length=4)
ax.tick_params(which='minor', width=.6, length=3)
ax.grid(color='grey', linestyle='-', linewidth=.25)
ax.set_ylabel(r'Energia cinetica [eV]')
ax.set_xlabel('Tiempo [fs]')

fig.tight_layout(pad=.4)
plt.show()
