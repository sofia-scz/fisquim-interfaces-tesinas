import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# plt set up
fm = fm.fontManager.addfont(path='Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rc('lines', linewidth=3)
colors = ['#c33', '#395', '#38e', '#eb2', '#865', '#a7a', '#e63']

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#            DATA  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
a = 1
h = 10

# data
cart_nodes = 10
cart_x = np.zeros(cart_nodes)
cart_y = np.linspace(0, h, cart_nodes)

# input
input_nodes = 4
input_x = np.zeros(input_nodes) + a
input_y = np.linspace(0, h/2, input_nodes) + h/4

# hidden 1
h1_nodes = 3
hidden1_x = np.zeros(h1_nodes) + 2*a
hidden1_y = np.linspace(0, h/3, h1_nodes) + h/3

# hidden 2
h2_nodes = 3
hidden2_x = np.zeros(h2_nodes) + 3*a
hidden2_y = np.linspace(0, h/3, h2_nodes) + h/3

# output
output_x = np.zeros(1) + 4*a
output_y = np.linspace(0, 1, 1) + h/2


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#       DO PLOTS  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
fig, ax = plt.subplots(1, 1, figsize=(7, 5), dpi=200)

node_size = 300

# plot joints
for i, cx in enumerate(cart_x):
    for j, ix in enumerate(input_x):
        x, y = [cx, ix], [cart_y[i], input_y[j]]
        ax.arrow(cx, cart_y[i], ix-cx, input_y[j]-cart_y[i], color='#f81',
                 lw=1, alpha=.5)

alpha = .5
for i, ix in enumerate(input_x):
    for j, hx in enumerate(hidden1_x):
        x, y = [ix, hx], [input_y[i], hidden1_y[j]]
        ax.plot(x, y, color='#999', lw=1, alpha=alpha)

for i, h1x in enumerate(hidden1_x):
    for j, h2x in enumerate(hidden2_x):
        x, y = [h1x, h2x], [hidden1_y[i], hidden2_y[j]]
        ax.plot(x, y, color='#999', lw=1, alpha=alpha)

for i, hx in enumerate(hidden2_x):
    for j, ox in enumerate(output_x):
        x, y = [hx, ox], [hidden2_y[i], output_y[j]]
        ax.plot(x, y, color='#999', lw=1, alpha=alpha)

# plot layers
ax.scatter(cart_x, cart_y, color='#f99', edgecolor='#c33', s=node_size)
ax.scatter(input_x, input_y, color='#80cdff', edgecolor='#0072bb', s=node_size)
ax.scatter(hidden1_x, hidden1_y, color='#bbb', edgecolor='#666', s=node_size)
ax.scatter(hidden2_x, hidden2_y, color='#bbb', edgecolor='#666', s=node_size)
ax.scatter(output_x, output_y, color='#8f8', edgecolor='#282',
           s=node_size)

# plot division lines
d = 1
ax.plot([a/2, a/2], [-d, h+d], color='#666', lw=1, ls='--')
ax.plot([3*a/2, 3*a/2], [-d, h+d], color='#666', lw=1, ls='--')
ax.plot([7*a/2, 7*a/2], [-d, h+d], color='#666', lw=1, ls='--')

# text
ax.text(-.45, h+1, 'Coordenadas\n  cartesianas')
ax.text(.83, h-1, 'Input\n layer')
ax.text(2.3, h-2, 'Hidden\n layers')
ax.text(3.7, h-3, 'Output\n  layer')

# # arrows + text
ax.annotate('Cambio a\ncoordenadas\ninvariantes', xy=(.5, 1),
            xytext=(.7, .2),
            arrowprops=dict(color='#444', shrink=0.0, lw=.5),
            horizontalalignment='left', verticalalignment='top',
            )

# ax.axis('off')
ax.get_xaxis().set_ticks([])
ax.get_yaxis().set_ticks([])
ax.set_xlim(-.7, 4.5)
ax.set_ylim(-2, 12.5)

fig.tight_layout(pad=.2)
plt.show()
