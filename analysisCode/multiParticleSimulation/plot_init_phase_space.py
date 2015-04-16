
from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from matplotlib.patches import Ellipse
import math
import helper
import os
# import pandas as pd
# import seaborn as sns
import numpy as np
import scipy as sp
from scipy import stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0*np.array(data)
    n = len(a)
    mean, se = np.mean(a), stats.sem(a)
    int_h = se * stats.t.ppf((1+confidence)/2., n-1)
    return mean, mean-int_h, mean+int_h

def plot_phase_space(parameters, kick_strength, number_of_particles):
    alpha   = ell_parameters['alpha']
    beta    = ell_parameters['beta']
    epsilon = ell_parameters['eps']
    x, px, y, py = helper.get_initial_particle_position_and_momentum(alpha, beta, epsilon, number_of_particles)
    
    x_kick = np.sqrt( (kick_strength[0]*beta[0]) / (alpha[0]**2 +1)) # amplitude of kick (about 8sig8sig)
    y_kick = np.sqrt( (kick_strength[1]*beta[1]) / (alpha[1]**2 +1))
    x_new = x + x_kick
    y_new = y + y_kick
    
    x       = x*1000
    x_new   = x_new*1000
    y       = y*1000
    y_new   = y_new*1000
        

    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor('white')
    tx = fig.add_subplot(1, 1, 1)
    tx.set_xlim([-6, 6])
    tx.set_ylim([-.00008, .00008])
    tx.ticklabel_format(axis='y', style='sci', scilimits=(-1,1) )
    tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    tx.scatter(x, px, label='Before kick',color='cornflowerblue')
    tx.scatter(x_new, px, label='After kick',color='salmon')
    tx.set_xlabel(r'$x$ $[mm]$')
    tx.set_ylabel(r'$p_x$')
    
    cov = np.cov(x, px)
    lambda_, v = np.linalg.eig(cov)
    lambda_ = np.sqrt(lambda_)

    ell = Ellipse(xy=(np.mean(x), np.mean(px)),
                  width=lambda_[0]*1*2, height=lambda_[1]*1*2,
                  angle=-np.rad2deg(np.arccos(v[0, 0])),
                  color= 'black',
                  label= r'$\sigma$',
                  lw=2)
    ell.set_facecolor('none')
    tx.add_patch(ell)

    ell = Ellipse(xy=(np.mean(x), np.mean(px)),
                  width=lambda_[0]*12.3*2, height=lambda_[1]*12.3*2,
                  angle=-np.rad2deg(np.arccos(v[0, 0])),
                  linestyle='dashed',
                  color= 'black',
                  label= r'$12.3$ $\sigma$',
                  lw=2)
    ell.set_facecolor('none')
    tx.add_patch(ell)


    fig2 = plt.figure(figsize=(10, 8))
    fig2.patch.set_facecolor('white')
    ty = fig2.add_subplot(1, 1, 1)
    ty.scatter(y, py, label='Before kick',color='cornflowerblue')
    ty.scatter(y_new, py, label='After kick',color='salmon')
    ty.ticklabel_format(axis='y', style='sci', scilimits=(-1,1) )
    ty.set_xlabel(r'$y$ $[mm]$')
    ty.set_ylabel(r'$p_y$')
    ty.set_xlim([-6, 6])
    ty.set_ylim([-.00008, .00008])
    ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')

    covy = np.cov(y, py)
    lambda_, vy = np.linalg.eig(covy)
    lambda_ = np.sqrt(lambda_)

    elly = Ellipse(xy=(np.mean(y), np.mean(py)),
                  width=lambda_[0]*1*2, height=lambda_[1]*1*2,
                  angle=np.rad2deg(np.arccos(vy[0, 0])),
                  color= 'black',
                  label= r'$\sigma$',
                  lw=2)
    elly.set_facecolor('none')
    ty.add_patch(elly)

    elly = Ellipse(xy=(np.mean(y), np.mean(py)),
                  width=lambda_[0]*9.1*2, height=lambda_[1]*9.1*2,
                  angle=np.rad2deg(np.arccos(vy[0, 0])),
                  linestyle='dashed',
                  color= 'black',
                  label= r'$9.1$ $\sigma$',
                  lw=2)
    elly.set_facecolor('none')
    ty.add_patch(elly)

    tx.legend(fancybox=True, loc='lower left', prop={'size': 24})
    ty.legend(fancybox=True, loc='upper left' , prop={'size': 24})
#     fig.subplots_adjust(left=.2)
#     fig2.subplots_adjust(left=.2)
    fig.tight_layout()
    fig2.tight_layout()
    plt.show()

 
#====================================================================================================    
#               MAIN INVOCATION
#====================================================================================================

if __name__=='__main__':
    ell_parameters = {'alpha':(2.323750151, -2.609936877), 'beta':(122.1802439, 214.9669053), 'eps':(3.5e-9, 4.0e-9)} # alpha and beta from model twiss at S = 0 at IP3. Eps from measured values 2012.
    kick_strength = (0.53e-6, 0.33e-6)
    number_of_particles = 5000

    plot_phase_space(parameters=ell_parameters, kick_strength=kick_strength, number_of_particles=number_of_particles)



 
