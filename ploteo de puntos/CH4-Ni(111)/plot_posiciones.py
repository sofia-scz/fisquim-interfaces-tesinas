import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator,
                               FormatStrFormatter)

# plt set up
fm = fm.fontManager.addfont(path='Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=1)
colors = ['#c33', '#395', '#38e', '#eb2', '#865', '#a7a', '#e63']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            DATA  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
a = 7.5431893271500003/6
h = 6.5325935828699997/3

# ni points
# layer 1
x1_ni = a*np.array([0, 1, 1, 2, 2, 3, 3, 4, 5])
y1_ni = h*np.array([2, 1, 3, 0, 2, 1, 3, 2, 1])
# layer 2
x2_ni = x1_ni.copy()
y2_ni = y1_ni.copy() - 2*h/3

x2_ni[3], y2_ni[3] = -a, h*(2+1/3)

# grid lines
grid_lines = [([1, 5], [1, 1]),
              ([0, 4], [2, 2]),
              ([1, 3], [3, 3]),

              ([0, 2], [2, 0]),
              ([1, 3], [3, 1]),
              ([3, 5], [3, 1]),

              ([2, 4], [0, 2]),
              ([1, 3], [1, 3]),
              ([0, 1], [2, 3]),
              ]

# site points
site_points = {'top': (2*a, 2*h),
               'bridge': (2.5*a, 1.5*h),
               'fcc': (2*a, 4*h/3),
               'hcp': (3*a, 5*h/3),
               'top-bridge': (2.25*a, 1.75*h),
               'top-fcc': (2*a, 5*h/3),
               'top-hcp': (2.5*a, h*(1+5/6))}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       DO PLOTS  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig, ax = plt.subplots(1, 1, figsize=(5, 5), dpi=200)

# plot grid

ax.plot([0], [0], lw=.5, color='gray', label='lattice grid')
for line in grid_lines:
    x, y = line
    x, y = a*np.array(x), h*np.array(y)
    ax.plot(x, y, lw=.5, color='gray')

# plot ni atoms
ax.scatter(x1_ni, y1_ni, color='#888', label='Ni atom layer 1', s=50)
ax.scatter(x2_ni, y2_ni, color='#ccc', edgecolor='#888',
           label='Ni atom layer 2', s=50)

# plot site points
msize = 50
for i, p_key in enumerate(site_points):
    x, y = site_points[p_key]
    ax.scatter(x, y, label=p_key, marker='x', lw=2, s=msize,
               color=colors[i])

ax.set_aspect('equal', 'box')
ax.legend(loc='upper right', fontsize=6)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.tick_params(which='major', width=.8, length=4)
ax.tick_params(which='minor', width=.6, length=3)
ax.grid(color='grey', linestyle='-', linewidth=.25)

fig.supxlabel(r'Posición x [angs]', y=.05)
fig.supylabel('Posición y [angs]')
fig.tight_layout(pad=.4)
plt.show()
