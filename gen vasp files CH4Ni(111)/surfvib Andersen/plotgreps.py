from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
import numpy as np
from os import listdir
from os.path import join, isfile

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
plt.rc('legend', fontsize=10)
plt.rc('legend', title_fontsize=10)
colors = ['#e8e', '#95c', '#38e', '#3bb', '#395', '#dc2', '#fa3',
          '#e63', '#c33', '#865']


def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


mydir = 'greps'
files = [f for f in listdir(mydir) if isfile(join(mydir, f))]

arrays = {}
for f in files:
    with open(join(mydir, f), 'r') as rfile:
        lines = rfile.readlines()
        values = []
        for line in lines:
            values.append([float(x) for x in line.split() if is_float(x)])
        array = np.array(values)
        arrays[f] = array


nfiles = len(files)
keys = sorted(arrays.keys(), key=lambda s: float(s[:-1]))

fig, axes = plt.subplots(
    nfiles, 2, dpi=150, figsize=(12, 3*nfiles), sharex=True)
for i, key in enumerate(keys):
    # left
    axis = axes[i]
    a = arrays[key]
    x = a[:, 0]*5
    ax = axis[0]
    ax.plot(x, a[:, 2] - a[0, 2], label=r'$\Delta$E total', c='#395')
    ax.legend(loc='upper left')

    # right
    ax = axis[1]
    ax2 = ax.twinx()
    ax.plot(x, a[:, 2] - a[0, 2], label=r'$\Delta$E total', c='#395')
    ax.plot(x, a[:, 3] - a[0, 3], label=r'$\Delta$E pot', c='#38e')
    ax.plot(x, a[:, 5] - a[0, 5], label=r'$\Delta$E k', c='#95c')
    ax2.plot(x, a[:, 1], label='Temperatura', c='#c33')

    ax.legend(loc='upper left')
    ax2.legend(title=f'TEBEG$={key}$\n'r'$\left< T \right>=$'f'${round(np.mean(a[:, 1]), 2)}K$',
               loc='upper right')

    for ax in axis:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', width=.8, length=4)
        ax.tick_params(which='minor', width=.6, length=3)
        ax.grid(color='grey', linestyle='-', linewidth=.25)
fig.supxlabel('Tiempo [fs]')
fig.supylabel(r'Energia [eV]')
fig.text(1.01, .43, r'Temperatura [K]', rotation=-90)
fig.tight_layout(pad=.8)
plt.show()
plt.show()
