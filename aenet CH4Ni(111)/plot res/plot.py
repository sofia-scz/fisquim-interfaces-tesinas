import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import AutoMinorLocator
import matplotlib.font_manager as fm
from datetime import date

# set up
fm = fm.fontManager.addfont(path='/home/sofia/fonts/Ubuntu-Regular.ttf')
plt.rc('font', family='Ubuntu', size='14')
plt.rcParams['legend.title_fontsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rc('lines', linewidth=.3)
plt.rc('lines', markersize=2)
colors = ['#e8e', '#95c', '#38e', '#3bb', '#395', '#dc2', '#fa3',
          '#e63', '#c33', '#865']

red, green, yellow = '#c33', '#395', '#dc2'


def outlier_filter(data):
    bools = [True if (x > .5 and x < 3) else False for x in data]
    return data[bools], bools


# gather data
conv = pd.read_csv("res/convergence.dat", delim_whitespace=True, skiprows=1, header=None)
enertest = pd.read_csv("res/energies.test", delim_whitespace=True,  header=None, usecols=[0, 1])
enertrain = pd.read_csv("res/energies.train", delim_whitespace=True, header=None, usecols=[0, 1])

Edft = -89.51997675
Eann = -89.51997675
enertrain[0] -= Edft
enertrain[1] -= Eann
enertest[0] -= Edft
enertest[1] -= Eann
dft_enes = np.hstack((enertrain[0].values, enertest[0].values))
Emin, Emax = round(dft_enes.min(), 4), round(dft_enes.max(), 4)
# remove outliers
dft_enes_clean, _ = outlier_filter(dft_enes)

# start plots
fig, axes = plt.subplots(2, 3, gridspec_kw={'width_ratios': [1.2, 1, 1]},
                         figsize=(17, 9), dpi=200)

axes[1, 1].sharex(axes[0, 1])
axes[1, 2].sharex(axes[0, 2])

axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('error')
axes[0, 0].set_yscale('log')
axes[0, 0].plot(conv[0], conv[1], color=red, label=' MAE ')
axes[0, 0].plot(conv[0], conv[2], color=green, label=' RMSE ')
axes[0, 0].plot(conv[0], conv[3], color=red, ls='--', label=' MAE Test ')
axes[0, 0].plot(conv[0], conv[4], color=green, ls='--', label=' RMSE Test ')
axes[0, 0].legend(loc='upper right')

dE = .1  # target error
axes[0, 1].set_title(r'Select energias')
axes[0, 1].set_ylabel('Energia ANN')
etrain_filtered, bools = outlier_filter(enertrain[0])
axes[0, 1].scatter(etrain_filtered, enertrain[1][bools], color=yellow, label='Trainset')
etest_filtered, bools = outlier_filter(enertest[0])
axes[0, 1].scatter(etest_filtered, enertest[1][bools], color=green, label='Testset')
axes[0, 1].plot(etrain_filtered, etrain_filtered, color=red)
axes[0, 1].plot(etrain_filtered, etrain_filtered+dE, color=red)
axes[0, 1].plot(etrain_filtered, etrain_filtered-dE, color=red)
axes[0, 1].xaxis.set_minor_locator(AutoMinorLocator())
axes[0, 1].yaxis.set_minor_locator(AutoMinorLocator())
axes[0, 1].legend(loc='upper left')


axes[0, 2].set_title(r'Dataset completo')
axes[0, 2].scatter(enertrain[0], enertrain[1], color=yellow, label='Trainset')
axes[0, 2].scatter(enertest[0], enertest[1], color=green, label='Testset')
axes[0, 2].plot(enertrain[0], enertrain[0], color=red)
axes[0, 2].plot(enertrain[0], enertrain[0]+.1, color=red)
axes[0, 2].plot(enertrain[0], enertrain[0]-.1, color=red)
axes[0, 2].xaxis.set_minor_locator(AutoMinorLocator())
axes[0, 2].yaxis.set_minor_locator(AutoMinorLocator())
axes[0, 2].legend(title=f'Emin$={Emin}$\n Emax$={Emax}$', loc='upper left')


axes[1, 0].set_xlabel('N° de config')
axes[1, 0].set_ylabel('Energia DFT')
axes[1, 0].scatter(range(len(dft_enes)), dft_enes, color=red)

axes[1, 1].set_xlabel('Energia DFT')
axes[1, 1].set_ylabel('Ocurrencias')
axes[1, 1].hist(dft_enes_clean, bins=100, edgecolor=red, facecolor='#fff')

axes[1, 2].set_xlabel('Energia DFT')
axes[1, 2].hist(dft_enes, bins=100, edgecolor=red, facecolor='#fff')

for axis in axes:
    for ax in axis:
        ax.tick_params(which='both', direction='in', top=True, right=True)
        ax.tick_params(which='major', width=.8, length=4)
        ax.tick_params(which='minor', width=.6, length=3)
        ax.grid(color='grey', linestyle='-', linewidth=.25)

fig.suptitle(f'aenet training {date.today().strftime("%d-%m-%Y")}')
fig.tight_layout()
plt.show()
