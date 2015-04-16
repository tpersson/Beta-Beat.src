import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from math import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib import colors, cm
import time
import os
import matplotlib.lines as mlines




def anharmonicities():
    Qxx_mod  =   .1e3
    Qxy_mod  = -2.1e3
    Qyx_mod  = -2.1e3
    Qyy_mod  =  1.8e3
    Qxxx_mod = -23.0e9
    Qxxy_mod =   7.0e9
    Qyxx_mod =   7.0e9
    Qyxy_mod =   8.3e9
    Qyyy_mod = -23.0e9
    Qxyy_mod =   8.3e9

    Qxx_mod  = 88.64619921
    Qxy_mod  = -2091.597532
    Qyx_mod  = -2091.597532
    Qyy_mod  = 1798.466543
    Qxxx_mod = -2.300000847e+10
    Qxxy_mod = 7000020083
    Qyxx_mod = 7000020083
    Qyxy_mod =  8299984697
    Qyyy_mod =  -2.299999245e+10
    Qxyy_mod =  8299984697

    # Qxx_mod  =  799.7987731
    # Qxy_mod  =  -1599.598495
    # Qyx_mod  =  -1599.598495
    # Qyy_mod  =  2799.625931
    # Qxxx_mod =  -1.765842735e+10
    # Qxxy_mod =  7446230914
    # Qyxx_mod =  7446230914
    # Qyxy_mod =  9410095632
    # Qyyy_mod =  -2.005940021e+10
    # Qxyy_mod =  9410095632

    
    Qxx  =   0.8e3
    Qxy  =  -2.0e3
    Qyx  =  -1.4e3
    Qyy  =  2.8e3
    Qxxx = -18e9
    Qxxy = 7.6e9
    Qyxx =   6e9
    Qyxy =   8e9
    Qyyy = -20e9
    Qxyy =  11e9

    Qxx_err  = 1e3
    Qxy_err  =.4e3
    Qyx_err  =.7e3
    Qyy_err  = 1e3
    Qxxx_err = 5e9
    Qxxy_err = 1e9
    Qyxx_err = 3e9
    Qyxy_err = 3e9
    Qyyy_err = 3e9
    Qxyy_err = 3e9


    D = (Qxxx_mod+2*Qyxx_mod)*(Qxyy_mod +2*Qyyy_mod) - (Qxxy_mod+2*Qyxy_mod)**2
    print D
    
    Jx = np.linspace(0.,.9e-6,80)
    Jy = np.linspace(0.,.9e-6,80)
    Jyplot = np.zeros(len(Jx)*len(Jy))
    Jxplot = np.zeros(len(Jx)*len(Jy))
    det    = np.zeros(len(Jx)*len(Jy))
    det_djx= np.zeros(len(Jx)*len(Jy))
    det_djy= np.zeros(len(Jx)*len(Jy))
    det_mod= np.zeros(len(Jx)*len(Jy))

    for i in range(len(Jx)):
        for j in range(len(Jy)):
            n = i*len(Jy) + j
            det[n] = (Qxx + 2*Qyx)*Jx[i] + (Qxy + 2*Qyy)*Jy[j] + .5*(Qxxx + 2*Qyxx)*Jx[i]**2 + .5*(Qxyy + 2*Qyyy)*Jy[j]**2 + (Qxxy + 2*Qyxy)*Jx[i]*Jy[j]
            
            det_mod_temp = (Qxx_mod + 2*Qyx_mod)*Jx[i] + (Qxy_mod + 2*Qyy_mod)*Jy[j] + .5*(Qxxx_mod + 2*Qyxx_mod)*Jx[i]**2 + .5*(Qxyy_mod + 2*Qyyy_mod)*Jy[j]**2 + (Qxxy_mod + 2*Qyxy_mod)*Jx[i]*Jy[j]
            det_mod[n] = -det_mod_temp
            Jxplot[n] = Jx[i]
            Jyplot[n] = Jy[j]
            
    m = -1
    n = -2

    Jy_xzero = -((m*Qxx + n*Qyx) + (m*Qxxx + n*Qyxx)*Jx ) / (m*Qxxy + n*Qyxy)
    Jy_yzero = -((m*Qxy + n*Qyy) + (m*Qxxy + n*Qyxy)*Jx )  / (m*Qxyy + n*Qyyy)
    Jy_xzero_mod = -((Qxx_mod + 2*Qyx_mod) + (Qxxx_mod + 2*Qyxx_mod)*Jx ) / (Qxxy_mod + 2*Qyxy_mod)
    Jy_yzero_mod = -((Qxy_mod + 2*Qyy_mod) + (Qxxy_mod + 2*Qyxy_mod)*Jx ) / (Qxyy_mod + 2*Qyyy_mod)
    Jy_xmod = -((m*Qxx_mod + n*Qyx_mod) + (m*Qxxx_mod + n*Qyxx_mod)*Jx ) / (m*Qxxy_mod + n*Qyxy_mod)
    Jy_ymod = -((m*Qxy_mod + n*Qyy_mod) + (m*Qxxy_mod + n*Qyxy_mod)*Jx ) / (m*Qxyy_mod + n*Qyyy_mod)
         
    a = (Qxy_mod +2*Qyy_mod)/(Qxyy_mod +2*Qyyy_mod) - (Qxx_mod +2*Qyx_mod)/(Qxxy_mod +2*Qyxy_mod)
    b = (Qxxx_mod +2*Qyxx_mod)/(Qxxy_mod+2*Qyxy_mod) - (Qxxy_mod +2*Qyxy_mod)/(Qxyy_mod +2*Qyyy_mod) 
    
    jxtest = a/b
    jytest = -((Qxx_mod + 2*Qyx_mod) + (Qxxx_mod + 2*Qyxx_mod)*jxtest ) / (Qxxy_mod + 2*Qyxy_mod)  
    print jxtest, jytest
    
    errtop = (Qxx_err**2 + 4*Qxy_err**2) + Jx**2*(Qxxx_err**2 + 4*Qyxx_err**2)
    bot    = ((Qxx + 2*Qxy) + 2*(Qxxx + 2*Qyxx)*Jx)**2
    Jy_xzero_err = np.sqrt(  (Qxxy_err**2+4*Qyxy_err**2)/(Qxxy**2+4*Qyxy**2)   +  (errtop)/(bot)   )  
            
    affected_kicks = [
        (5.5e-6, 0.5, 5.1e-6, 0.3),
        (6.2e-6, 0.2, 4.9e-6, 0.3),
        (6.9e-6, 0.3, 5.4e-6, 0.5),
        (7.2e-6, 0.3, 5.7e-6, 0.2),
        (7.6e-6, 0.3, 6.1e-6, 0.3),
        (7.8e-6, 0.3, 6.2e-6, 0.3),
        (8.2e-6, 0.3, 6.5e-6, 0.3)
    ]
    

    npts = 10000
    xi = np.linspace(0.,.9e-6,100)
    yi = np.linspace(0.,.6e-6,100)

    model = True
    if model:
        fig1 = plt.figure(figsize=(10,7))
        fig1.patch.set_facecolor('white')
        t1 = fig1.add_subplot(111)
        t1.set_xlim([0,.9e-6])
        t1.set_ylim([0,.6e-6])
        detm    = griddata((Jxplot, Jyplot), det, (xi[None,:], yi[:,None]), method='cubic')
        cmap = plt.cm.bone
        v = np.linspace(-0.005, .005, 21, endpoint=True)
        norm = colors.BoundaryNorm(v, cmap.N)
        plt.contour(xi,yi, detm,v,linewidths=0.5,colors='k')
        plt.contourf(xi,yi,detm,v,cmap=cmap, norm=norm) 
        plt.xlabel(r'$2J_x$ $\cdot 10^{-1} [\mu m]$')
        plt.ylabel(r'$2J_y$ $\cdot 10^{-1} [\mu m]$')
        dx = t1.plot(Jx,Jy_xzero, 'r', lw=4)
        dy = t1.plot(Jx,Jy_yzero, 'b', lw=4)
        cbar = plt.colorbar() 
        ax = cbar.ax
        ax.text(6.8,.7,r"$\Delta Q$ [tune units]",rotation=90, fontsize=23)
        l1 = mlines.Line2D([],[],color='r', lw=4) 
        l2 = mlines.Line2D([],[],color='b', lw=4) 
        t1.legend([l1, l2], 
                  [r'$\frac{\partial}{\partial 2J_x}(-Q_x-2Q_y) = 0$' , r'$\frac{\partial}{\partial 2J_y}(-Q_x-2Q_y) = 0$'],
                  loc='lower right', fontsize=24)
        fig1.canvas.draw()
        labelsx = range(9)
        labelsy = range(6)
        labelsy[0] = ' '
        # labels = labels*10e6
        t1.set_xticklabels(labelsx)
        t1.set_yticklabels(labelsy)


        fig2 = plt.figure(figsize=(10,7))
        fig2.patch.set_facecolor('white')
        t2 = fig2.add_subplot(111)
        t2.set_xlim([0,.9e-6])
        t2.set_ylim([0,.6e-6])
        detm    = griddata((Jxplot, Jyplot), det_mod, (xi[None,:], yi[:,None]), method='cubic')
        cmap = plt.cm.bone_r
        v = np.linspace(0.0, .008, 17, endpoint=True)
        norm = colors.BoundaryNorm(v, cmap.N)
        plt.contour(xi,yi, detm,v,linewidths=0.5,colors='k')
        plt.contourf(xi,yi,detm,v,cmap=cmap, norm=norm)
        plt.xlabel(r'$2J_x$ $ [10^{-1} \mu m]$')
        plt.ylabel(r'$2J_y$ $ [10^{-1} \mu m]$')
        t2.plot(Jx,Jy_xzero_mod, 'r', lw=4)
        t2.plot(Jx,Jy_yzero_mod, 'b', lw=4)
#         t2.plot(Jx,Jy_xmod, 'r', lw=4)
#         t2.plot(Jx,Jy_ymod, 'b', lw=4)
        cbar = plt.colorbar() 
        ax = cbar.ax
        ax.text(5.4,.8,r"$\Delta (-Q_x-2Q_y)$ [tune units]",rotation=90, fontsize=23)
        l1 = mlines.Line2D([],[],color='r', lw=4) 
        l2 = mlines.Line2D([],[],color='b', lw=4) 
        t2.legend([l1, l2], 
                  [r'$\frac{\partial}{\partial 2J_x}(-Q_x-2Q_y) = 0$' , r'$\frac{\partial}{\partial 2J_y}(-Q_x-2Q_y) = 0$'],
                  loc='lower right', fontsize=24)
#         t2.scatter(jxtest,jytest, lw=0, color='k', s=180)
        fig1.canvas.draw()
        labelsx = range(9)
        labelsy = range(6)
        labelsy[0] = ' '
        # labels = labels*10e6
        t2.set_xticklabels(labelsx)
        t2.set_yticklabels(labelsy)  




    fig1.tight_layout()
    fig2.tight_layout()
    plt.show()



    '''

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

    # SET FIGURE PARAMETERS
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

    # DO THE PLOTTING

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
'''

if __name__ == '__main__':
    anharmonicities()

