''' calc coefficients and errors '''

import numpy as np
import scipy as scp
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator



def calc_coeff(data_from_model=True):
    # FROM MODEL
    value_dict_mod = {  'a': 660.455818         ,
                        'b': -1798.907127       ,
                        'c': -7801481843 / 2    ,
                        'd': 6576611431 / 2     ,
                        'e': 2736984974         ,
                        'f': 3630.78782         ,
                        'g': -1.221292873e10 / 2
                        }

    alpha_mod       = value_dict_mod['a'] + 2*value_dict_mod['b']
    beta_mod        = 2*value_dict_mod['c'] + 2*value_dict_mod['e']
    gamma_mod       = 4*value_dict_mod['d'] + value_dict_mod['e']
    delta_mod       = value_dict_mod['b'] + 2*value_dict_mod['f']
    epsilon_mod     = 2*value_dict_mod['d'] + 4*value_dict_mod['g'] 
    
    print 'alpha mod:  ', alpha_mod
    print 'beta mod :  ', beta_mod
    print 'gamma_mod:  ', gamma_mod
    print 'delta mod:  ', delta_mod
    print 'epsilon mod:  ', epsilon_mod

    # FROM MEASUREMENT
    value_dict = {  'a': [.8e3  , 1e3    ],
                    'b': [-1.7e3, .55e3  ],
                    'c': [-9e9  , 2.5e9  ], 
                    'd': [9.5e9 , 3e9    ],
                    'e': [6.8e9 , 2e9    ],
                    'f': [2.8e3 , 1e3    ],
                    'g': [-10e9 , 1.5e9  ]
                    }

    alpha       = value_dict['a'][0] + 2*value_dict['b'][0]
    beta        = 2*value_dict['c'][0] + 2*value_dict['e'][0]
    gamma       = 4*value_dict['d'][0] + value_dict['e'][0]
    delta       = value_dict['b'][0] + 2*value_dict['f'][0]
    epsilon     = 2*value_dict['d'][0] + 4*value_dict['g'][0]    


    alpha_sig   = np.sqrt( (value_dict['a'][1])**2 + (2*value_dict['b'][1])**2 )
    beta_sig    = np.sqrt( (2*value_dict['c'][1])**2 + (2*value_dict['e'][1])**2 )
    gamma_sig   = np.sqrt( (4*value_dict['d'][1])**2 + (value_dict['e'][1])**2 )
    delta_sig   = np.sqrt( (value_dict['b'][1])**2 + (2*value_dict['f'][1])**2 )
    epsilon_sig = np.sqrt( (2*value_dict['d'][1])**2 + (4*value_dict['g'][1])**2 )

    print 'alpha:  ', alpha
    print 'beta :  ', beta
    print 'gamma:  ', gamma
    print 'delta:  ', delta
    print 'epsil:  ', epsilon

    print 'alpha sig:  ', alpha_sig
    print 'beta sig:  ', beta_sig
    print 'gamma_sig:  ', gamma_sig
    print 'delta sig:  ', delta_sig
    print 'epsil sig:  ', epsilon_sig
                 
    Jx = np.linspace(-.5e-6,.5e-6,80)
    Jy_1 = ( alpha + beta*Jx ) / gamma
    Jy_2 = ( delta + gamma*Jx ) / epsilon
    Jy_1_mod = ( alpha_mod + beta_mod*Jx ) / gamma_mod
    Jy_2_mod = ( delta_mod + gamma_mod*Jx ) / epsilon_mod

    Jy_1_err = Jy_1*np.sqrt( ( np.sqrt(delta_sig**2 + (Jx*gamma_sig)**2) / (delta + gamma*Jx) )**2 + (epsilon_sig/epsilon)**2 ) 
    Jy_2_err = Jy_2*np.sqrt( ( np.sqrt(alpha_sig**2 + (Jx*beta_sig)**2 ) / (alpha + beta*Jx)  )**2 + (gamma_sig/gamma)**2 )
    print Jy_1_err    

    ''' SET FIGURE PARAMETERS'''
    fig = plt.figure(figsize=(27, 11))
    tx = fig.add_subplot(1,2,1)
    ty = fig.add_subplot(1,2,2)
    
    tx.set(xlabel=('$2J_x$'+'  '+'$[\mu m]$'), ylabel=('$2J_y$'+'  '+'$[\mu m]$'), xlim=([-.5, .5]), ylim=[-.5,.5])
    tx.ticklabel_format(useOffset=False)
    tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    tx.axhline(y=0, color='k', linewidth=1.0)
    tx.axvline(x=0, color='k', linewidth=1.0)

    ty.set(xlabel=('$2J_x$'+'  '+'$[\mu m]$'), ylabel=('$2J_y$'+'  '+'$[\mu m]$'), xlim=([-.5, .5]), ylim=[-.5,.5])
    ty.ticklabel_format(useOffset=False)
    ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    ty.axhline(y=0, color='k', linewidth=1.0)
    ty.axvline(x=0, color='k', linewidth=1.0)

    ''' DO THE PLOTTING '''

    tx.plot(Jx*10**6,Jy_1*10**6,'-', label=r'$\frac{\partial}{\partial 2J_x}(Q_x + 2Q_y) = 0 $ Meas')
    tx.plot(Jx*10**6,Jy_2*10**6,'-', label=r'$\frac{\partial}{\partial 2J_y}(Q_x + 2Q_y) = 0 $ Meas')
    tx.plot(Jx*10**6,Jy_1_mod*10**6,'-', label=r'$\frac{\partial}{\partial 2J_x}(Q_x + 2Q_y) = 0 $ Model')
    tx.plot(Jx*10**6,Jy_2_mod*10**6,'-', label=r'$\frac{\partial}{\partial 2J_y}(Q_x + 2Q_y) = 0 $ Model')

    ty.errorbar(Jx*10**6,Jy_1*10**6, xerr=0, yerr=Jy_2_err*10**6, label=r'$\frac{\partial}{\partial 2J_x}(Q_x + 2Q_y) = 0 $ Meas', elinewidth=.5)
    ty.errorbar(Jx*10**6,Jy_2*10**6, xerr=0, yerr=Jy_1_err*10**6, label=r'$\frac{\partial}{\partial 2J_y}(Q_x + 2Q_y) = 0 $ Meas', elinewidth=.5)   
    ty.plot(Jx*10**6,Jy_1_mod*10**6,'-', label=r'$\frac{\partial}{\partial 2J_x}(Q_x + 2Q_y) = 0 $ Model')
    ty.plot(Jx*10**6,Jy_2_mod*10**6,'-', label=r'$\frac{\partial}{\partial 2J_y}(Q_x + 2Q_y) = 0 $ Model')

    lgd = plt.legend(loc = 'upper center', ncol=2, numpoints=1, bbox_to_anchor=(-0.1, 1.22))
    fig.savefig('surviving_lines', bbox_extra_artists=(lgd,), bbox_inches='tight')
    #Note that the bbox_extra_artists must be an iterable
    plt.show()  


if __name__ == '__main__':
    # constant_dict = calc_coeff()
    # plot_lines(constant_dict)
    calc_coeff(data_from_model=True)

