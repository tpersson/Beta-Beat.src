import os
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


#====================================================================================================    
#               MAIN PART
#====================================================================================================

def plot_tunes(sdds_file_path, output_file=None):

    ''' SET FIGURE 1'''
    fig = plt.figure(figsize=(11, 22))
    fig.patch.set_facecolor('white')
    fig.suptitle('Initial Action vs. GetLLM Action')
    tx = fig.add_subplot(2,1,1)
    tx.set(xlabel=('2Jx GetLLM [um]'), ylabel=('2Jx Initial [um]'), xlim=[.2,.65])
    tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    # tx.xaxis.set_major_locator(MultipleLocator(.05))
    tx.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
    ty = fig.add_subplot(2,1,2)
    ty.set(xlabel=('2Jy GetLLM [um]'), ylabel=('2Jy Initial [um]'), xlim=[.15,.45])
    ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    # ty.xaxis.set_major_locator(MultipleLocator(.05))
    ty.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})

    for n in range(len(sdds_file_path)):
        main_tunes = get_main_tunes(sdds_file_path[n])
        file_name =  os.path.basename(sdds_file_path[n])
        actions_init = get_initial_actions(file_name)
        actions    = get_actions(sdds_file_path[n])
        kick_label = get_kick_label(file_name)

        jx = actions[0]*10**6
        jy = actions[2]*10**6
        jx_err = actions[1]*10**6
        jy_err = actions[3]*10**6

        tx.errorbar(jx, actions_init[0]*10**6, xerr=jx_err , yerr = 0, ms=8, fmt='o',  label=kick_label )
        ty.errorbar(jy, actions_init[1]*10**6, xerr=jy_err , yerr = 0, ms=8, fmt='o',  label=kick_label )

    for n in range(len(sdds_file_path)):
        file_name =  os.path.basename(sdds_file_path[n])
        actions_init = get_initial_actions(file_name)       
        tx.plot(actions_init[0]*10**6,actions_init[0]*10**6, 'o', ms=8)
        ty.plot(actions_init[1]*10**6,actions_init[1]*10**6, 'o', ms=8)

    x = np.linspace(.2,.65)
    y = x
    x2= np.linspace(.15, .45)
    y2= x2
    tx.plot(x,y,'k--')
    ty.plot(x2,y2,'k--')
    plt.legend(numpoints=1, loc='lower right')
    plt.show()


#====================================================================================================    
#               HELPER FUNCTIONS
#====================================================================================================


def get_actions(sdds_file_path):
    get_kick_path = os.path.join(os.path.dirname(sdds_file_path),'getllm/getkick.out')
    for line in reversed(open(get_kick_path).readlines()):
        line_data = line.split()   
        [JX, JXstd, JY, JYstd] = [float(line_data[13]), float(line_data[14]), float(line_data[15]), float(line_data[16])]
        break
    return [JX, JXstd, JY, JYstd]

def get_main_tunes(sdds_file_path):
    tune_file_path = os.path.join(os.path.dirname(sdds_file_path), 'getllm/getphasetotx.out')
    with open(tune_file_path) as phase_file:
        line = phase_file.readline()
        while str(line).startswith('@'):  # read header 
            line = phase_file.readline()
            if str(line).startswith('@ Q1'):
                line_data = line.split()
                tune_x = float(line_data[3])
            elif str(line).startswith('@ Q2'):
                line_data = line.split()
                tune_y = float(line_data[3])
    return [tune_x, tune_y]


def get_kick_label(file_name):
    labels = {  'SPS_s82s65.sdds': '(8.2 , 6.5)',
                'SPS_s78s62.sdds': '(7.8 , 6.2)',
                'SPS_s76s61.sdds': '(7.6 , 6.1)',
                'SPS_s72s57.sdds': '(7.2 , 5.7)',
                'SPS_s69s54.sdds': '(6.9 , 5.4)',
                'SPS_s62s49.sdds': '(6.2 , 4.9)',
                'SPS_s55s51.sdds': '(5.5 , 5.1)'
                 }
    file_label = labels[file_name]
    return file_label

def get_initial_actions(file_name):
    actions = { 'SPS_s82s65.sdds': [.53e-6, .33e-6],
                'SPS_s78s62.sdds': [.48e-6, .30e-6],
                'SPS_s76s61.sdds': [.45e-6, .29e-6],
                'SPS_s72s57.sdds': [.40e-6, .25e-6],
                'SPS_s69s54.sdds': [.37e-6, .23e-6],
                'SPS_s62s49.sdds': [.30e-6, .19e-6],
                'SPS_s55s51.sdds': [.24e-6, .20e-6]
                 }
    init_action = actions[file_name]
    return init_action

def get_models(job_directory):
    model_list = []
    for simulation in job_directory:
        for i in range(0,3):
            model_list.append(os.path.join(simulation,'job000%s/SPS%s.sdds' % (i,i))) #
    return model_list


#====================================================================================================    
#               MAIN INVOCATION
#====================================================================================================


if __name__=='__main__':

    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/model/spectra/multiple2.pdf'
    output_file_path = None

    sdds_models =  ['/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s82s65/SPS_s82s65.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s78s62/SPS_s78s62.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s76s61/SPS_s76s61.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s72s57/SPS_s72s57.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s69s54/SPS_s69s54.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s62s49/SPS_s62s49.sdds',
                    '/afs/cern.ch/work/f/fcarlier/public/simulations/var_kick/s55s51/SPS_s55s51.sdds'
                    ]
    plot_tunes(sdds_file_path=sdds_models, output_file=None)