#!/usr/bin/env python
# -*- coding: utf8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc
rc('font', family='serif')

def read_matching_file(file_path):
    detuning_parameters = {
        'qx':[0, 0],
        'qy':[0, 0],
        'dqx_dex':[0, 0],
        'dqy_dex':[0, 0],
        'dqx_dey':[0, 0],
        'dqy_dey':[0, 0],
        'd2qx_dex':[0, 0],
        'd2qy_dex':[0, 0],
        'd2qx_dey':[0, 0],
        'd2qy_dey':[0, 0],
        'd2qx_dexey':[0, 0],
        'd2qy_dexey':[0, 0]
    }
    
    file_to_parameters = {
        ' "Q1"                         0          0          0          0':'qx',
        ' "Q2"                         0          0          0          0':'qy',
        ' "ANHX"                       1          0          0          0':'dqx_dex',
        ' "ANHY"                       0          1          0          0':'dqy_dey',
        ' "ANHX"                       0          1          0          0':'dqx_dey',
        ' "ANHY"                       1          0          0          0':'dqy_dex',
        ' "ANHX"                       2          0          0          0':'d2qx_dex',
        ' "ANHX"                       1          1          0          0':'d2qx_dexey',
        ' "ANHX"                       0          2          0          0':'d2qx_dey',
        ' "ANHY"                       0          2          0          0':'d2qy_dey',
        ' "ANHY"                       1          1          0          0':'d2qy_dexey',
        ' "ANHY"                       2          0          0          0':'d2qy_dex'
    }
    with open(file_path) as matching_file:
        line_length = 64 # length of the line to identify the parameter
        for line in matching_file:
            if not line.startswith('@') and not line.startswith('*') and not line.startswith('$'):
                if line[:line_length] in file_to_parameters:
                    detuning_parameters[file_to_parameters[line[:line_length]]][0] = float(line[line_length:])
                    
    return detuning_parameters
                

def detuning(x_values, plot, pars):
    q, j = plot[1], plot[3]
    return pars['q%s' % q][0] + pars['dq%s_de%s' % (q, j)][0]*x_values*1e-6 + .5*pars['d2q%s_de%s' % (q, j)][0]*x_values**2*(1e-6)**2

def detuning_error_band(x_values, plot, pars, upper=True):
    q, j = plot[1], plot[3]
    if upper:
        return pars['q%s' % q][0] + pars['q%s' % q][1] + (pars['dq%s_de%s' % (q, j)][0] + pars['dq%s_de%s' % (q, j)][1])*x_values*1e-6 + .5 * (pars['d2q%s_de%s' % (q, j)][0] + pars['d2q%s_de%s' % (q, j)][1])* x_values**2*(1e-6)**2
    else:
        return pars['q%s' % q][0] - pars['q%s' % q][1] + (pars['dq%s_de%s' % (q, j)][0] - pars['dq%s_de%s' % (q, j)][1])*x_values*1e-6 + .5 * (pars['d2q%s_de%s' % (q, j)][0] - pars['d2q%s_de%s' % (q, j)][1])* x_values**2*(1e-6)**2

def plot_detuning(plots, detuning_parameters, c='blue', plot_errors=True, label=None):
    x_values = np.arange(0, 1, .01)

    for plot in plots:
        plots[plot].set_xlabel('$2J_%s$ [$\mu$m]' % plot[3])
        plots[plot].set_ylabel('$Q_%s$' % plot[1])
        plots[plot].xaxis.set_major_locator(MultipleLocator(.2))
        plots[plot].xaxis.set_minor_locator(MultipleLocator(.1))
        plots[plot].yaxis.set_major_locator(MultipleLocator(.01))
        plots[plot].yaxis.set_minor_locator(MultipleLocator(.005))
        plots[plot].plot(x_values, detuning(x_values, plot, detuning_parameters), label=label, c=c)
        if plot_errors:
            plots[plot].plot(x_values, detuning_error_band(x_values, plot, detuning_parameters, upper=True), label='Error band', c='.5')
            plots[plot].plot(x_values, detuning_error_band(x_values, plot, detuning_parameters, upper=False), c='.5')
        
        plots[plot].set_xlim(0, 1)
        if plot[1] == 'x':
            plots[plot].set_ylim(0.25, 0.29)
        else:
            plots[plot].set_ylim(0.29, 0.33)

def init_plot():
    fig = plt.figure(figsize=(20, 13))
    fig.patch.set_facecolor('white')
    plots = {
        'qyjx':fig.add_subplot(2, 2, 1),
        'qyjy':fig.add_subplot(2, 2, 2),
        'qxjx':fig.add_subplot(2, 2, 3),
        'qxjy':fig.add_subplot(2, 2, 4)
    }
    return plots

def show_plot():
    plt.legend(loc=4)
    plt.subplots_adjust(left=0.07, right=0.98, top=0.98, bottom=0.08)
    plt.gcf().set_size_inches(10, 6.5)

    plt.savefig("/afs/cern.ch/user/r/rwestenb/Desktop/detuning_with_amplitude.pdf", dpi=200)
    #plt.show()

if __name__ == '__main__':
    detuning_parameters_measured = {
        'qx':(0.28061, 6e-5),
        'qy':(0.31151, 2e-5),
        'dqx_dex':( 0.8e3, 1.0e3),
        'dqy_dex':(-1.4e3, 0.4e3),
        'dqx_dey':(-2.0e3, 0.7e3),
        'dqy_dey':( 2.8e3, 1.0e3),
        'd2qx_dex':(-18e9, 5e9),
        'd2qy_dex':(  6e9, 1e9),
        'd2qx_dey':( 11e9, 3e9),
        'd2qy_dey':(-20e9, 3e9),
        'd2qx_dexey':(7.6e9, 3e9),
        'd2qy_dexey':(8.0e9, 3e9)
    }
    detuning_parameters_model = read_matching_file('/afs/cern.ch/user/r/rwestenb/Desktop/model/ptc_normal.matched.1det.3.q.dat')
    detuning_parameters_model_old = read_matching_file('/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/modelB2inj_correctedoptics/ptc_normal.dat')
    
    plots = init_plot()
    plot_detuning(plots, detuning_parameters_measured, c='b', label='Measurement')
    plot_detuning(plots, detuning_parameters_model_old, c='r', plot_errors=False, label='Model before matching')
    plot_detuning(plots, detuning_parameters_model, c='g', plot_errors=False, label='Model after matching')
    show_plot()
