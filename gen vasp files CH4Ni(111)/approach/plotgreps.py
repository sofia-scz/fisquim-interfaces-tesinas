from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
import numpy as np
from os import listdir
from os.path import join, isfile

fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1.5)
plt.rc('lines', markersize=3)
plt.rc('legend', title_fontsize=12)
plt.rc('legend', fontsize=10)
plt.rc('lines', marker='o')
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


sites = ['top', 'bridge', 'hcp', 'fcc']
clors = ['#395', '#38e', '#c33']
fig, axes = plt.subplots(2, 2, dpi=100, figsize=(12, 9), sharex=True, sharey=True)
dom = (14.1152 - 6.1154) - np.arange(31)*.2
E0 = -89.51997675

for i, ax in enumerate(axes.flatten()):
    site = sites[i]
    for j in np.arange(1, 4):
        key = f'{j}h_{site}_0'
        ax.plot(dom, arrays[key][:, 4]-E0, color=clors[j-1], label=f'{j}h', alpha=.9)
    ax.legend(title=site, loc='upper right')
    ax.set_ylim(-.5, 2)

for ax in axes.flatten():
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.tick_params(which='major', width=.8, length=4)
    ax.tick_params(which='minor', width=.6, length=3)
    ax.grid(color='grey', linestyle='-', linewidth=.25)

fig.supxlabel(r'Distancia centro de masa $CH_4$ - layer 1 sup Ni $\left[\AA\right]$')
fig.supylabel(r'Energia [eV]')
fig.tight_layout(pad=.8, h_pad=0)
plt.show()
