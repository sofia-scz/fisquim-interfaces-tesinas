import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,
                               FormatStrFormatter)

fm = fm.fontManager.addfont(path='Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#395', '#e63', '#38e', '#c33', '#eb2', '#865']

# data

x_points = np.array([3.77168, 6.28609, 5.0289, 2.5144, 1.25718, 0,
                     1.25723, 3.77164, 2.51442])

y_points = np.array([6.53265, 2.17745, 4.3551, 0.00002, 2.17739, 4.35506,
                    6.5326, 2.1774, 4.35509])


# plots

fig, ax = plt.subplots(1, 1, figsize=(5, 5), dpi=200)

a = 2.5144
b = 2.17739

vx, vy = b*np.cos(np.pi/6)*(2/3), b*np.sin(np.pi/6)*(2/3)
ux, uy = b*np.cos(np.pi/6), b*np.sin(np.pi/6)

# lattice grid
ax.plot([a, 2*a], [0, 2*b], lw=.5, color='gray', label='lattice grid')
ax.plot([.5*a, 1.5*a], [b, 3*b], lw=.5, color='gray')
ax.plot([0, .5*a], [2*b, 3*b], lw=.5, color='gray')

ax.plot([a, 0], [0, 2*b], lw=.5, color='gray')
ax.plot([a*1.5, .5*a], [b, 3*b], lw=.5, color='gray')
ax.plot([a*2.5, 1.5*a], [b, 3*b], lw=.5, color='gray')

ax.plot([a/2, 2.5*a], [b, b], lw=.5, color='gray')
ax.plot([0, 2*a], [2*b, 2*b], lw=.5, color='gray')
ax.plot([a/2, 1.5*a], [3*b, 3*b], lw=.5, color='gray')

# ni atoms
ax.scatter(x_points, y_points, color='#888', label='Ni atom', s=50)

# alt line
# ax.plot([a/2, 2*a], [b, 2*b], lw=.5, color='#395')

# points
msize = 50
ax.scatter([a/2], [b], label='top a', marker='x', lw=2, s=msize,
           color='#c33')
ax.scatter([a/2+vx], [b+vy], label='hcp a', marker='x', lw=2, s=msize,
           color='#e63')
ax.scatter([a/2+ux], [b+uy], label='bridge a', marker='x', lw=2, s=msize,
           color='#b69')
ax.scatter([a/2+2*vx], [b+2*vy], label='fcc a', marker='x', lw=2, s=msize,
           color='#865')

ax.scatter([a/2], [b*3], label='top b', marker='x', lw=2, s=msize,
           color='#eb2')
ax.scatter([a/2], [b*(1+4/3)], label='hcp b', marker='x', lw=2, s=msize,
           color='#395')
ax.scatter([a/2], [b*2], label='bridge b', marker='x', lw=2, s=msize,
           color='#3ac')
ax.scatter([a/2], [b*(1+2/3)], label='fcc b', marker='x', lw=2, s=msize,
           color='#38e')

ax.set_aspect('equal', 'box')
ax.legend(loc='upper right', fontsize=6)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.tick_params(which='major', width=.8, length=4)
ax.tick_params(which='minor', width=.6, length=3)
ax.grid(color='grey', linestyle='-', linewidth=.25)

fig.supxlabel(r'Posición x [angs]', va='top', y=.05)
fig.supylabel('Posición y [angs]', x=0)
fig.tight_layout(pad=.4)
plt.show()
