import os
import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches


#====================================================================================================    
#               MAIN PART
#====================================================================================================

def plot_tunes(sdds_file_path,sdds_experimental, output_file=None):

    ''' SET FIGURE 1'''
    fig1 = plt.figure(figsize=(24, 10))
#     fig2 = plt.figure(figsize=(10, 8))
    # fig.suptitle('Tune vs. Action cross term')
    tx = fig1.add_subplot(1,2,1)
    ty = fig1.add_subplot(1,2,2)
    tx.set(xlabel=('$2J_x2J_y$'), ylabel=('$Q_x$'), xlim=([0., .27]), ylim=[.2797,.2807])
    ty.set(xlabel=('$2J_x2J_y$'), ylabel=('$Q_y$'), xlim=([0., .27]), ylim=[.31185,.3133])

    for n in range(len(sdds_file_path)):
        main_tunes = get_main_tunes(sdds_file_path[n])
        actions    = get_actions(sdds_file_path[n])
        jx_jy = (actions[0]*actions[2])*10**12
        file_name =  os.path.basename(sdds_file_path[n])
        kick_label = get_kick_label(file_name)
        jx_jy_err = abs(jx_jy)*np.sqrt( (actions[1]/actions[0])**2 + (actions[3]/actions[2])**2 ) # ADD COV in sqrt: + (2cov)/(ab)

        tx.errorbar(jx_jy, main_tunes[0], xerr=jx_jy_err , yerr = 0, fmt='^', label=kick_label, elinewidth=1.5,capsize=5 )
        ty.errorbar(jx_jy, main_tunes[1], xerr=jx_jy_err , yerr = 0, fmt='^', elinewidth=1.5,capsize=4 )
        first_legend = plt.legend(numpoints=1, loc='lower left')


    for i in range(len(sdds_experimental)):
        main_tunes = get_main_tunes(sdds_experimental[i])
        actions    = get_actions(sdds_experimental[i])
        jx_jy = (actions[0]*actions[2])
        file_name =  os.path.basename(sdds_experimental[i])
        # print kick_name
        kick_label = get_kick_label(file_name)
        jx_jy_err = abs(jx_jy)*np.sqrt( (actions[1]/actions[0])**2 + (actions[3]/actions[2])**2 ) # ADD COV in sqrt: + (2cov)/(ab)

        tx.errorbar(jx_jy, main_tunes[0], xerr=jx_jy_err , yerr = 0, fmt='o', elinewidth=1.3,capsize=4)
#         cap.set_markeredgewidth(10)
        ty.errorbar(jx_jy, main_tunes[1], xerr=jx_jy_err , yerr = 0, fmt='o', label=kick_label, elinewidth=1.3,capsize=4)
 
    triangle =  tx.scatter(0,0,marker='^',s=250,facecolor='white')
    round =  tx.scatter(0,0,marker='o',s=250,facecolor='white')
    empty =  tx.scatter(0,0,marker='o',s=25,color='white')
    tx.xaxis.set_tick_params(width=2, length=5)
    tx.yaxis.set_tick_params(width=2, length=5)
    ty.xaxis.set_tick_params(width=2, length=5)
    ty.yaxis.set_tick_params(width=2, length=5)
    ty.yaxis.tick_right()
    ty.yaxis.set_label_position("right")


#     tx.legend(title='MODEL', shadow=True, fancybox=True, numpoints=1, loc=1)
#     ty.legend(title='MEASUREMENT', shadow=True, fancybox=True, numpoints=1, loc=2)

    p2 = mpatches.Patch(color='r', alpha=0.9) 
    p3 = mpatches.Patch(color='b', alpha=0.9) 
    p4 = mpatches.Patch(color='g', alpha=0.9) 
    p5 = mpatches.Patch(color='c', alpha=0.9) 
    p6 = mpatches.Patch(color='m', alpha=0.9) 
    p7 = mpatches.Patch(color='y', alpha=0.9) 
    p8 = mpatches.Patch(color='k', alpha=0.9)
    
    leg1 = tx.legend([triangle,round,empty, empty,p2,p3,p4,p5,p6,p7,p8],
                      ['Model', 'Measurement', '', r'$2J_x\,,\, 2J_y\, [\mu m]$','(0.53 , 0.33)','(0.48 , 0.30)','(0.45 , 0.29)','(0.4  , 0.25)','(0.37 , 0.23)','(0.3  , 0.19)','(0.24 , 0.20)'],
                      loc=9, bbox_to_anchor=(1.25,0.9),fancybox=True,scatterpoints=1, fontsize=24)



#     plt.legend(leg1)
    fig1.subplots_adjust(left=.1, right=.9, bottom=.1, top=.9,wspace=.5)
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
                'SPS_s55s51.sdds': '(5.5 , 5.1)',
                'Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned': '(8.2 , 6.5)',
                'Beam2@Turn@2012_06_25@03_55_09_762_0.sdds.new.nl_corrected.cleaned': '(7.8 , 6.2)',
                'Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned': '(7.6 , 6.1)',
                'Beam2@Turn@2012_06_25@03_44_50_218_0.sdds.new.nl_corrected.cleaned': '(7.2 , 5.7)',
                'Beam2@Turn@2012_06_25@03_36_40_108_0.sdds.new.nl_corrected.cleaned': '(6.9 , 5.4)',
                'Beam2@Turn@2012_06_25@03_30_55_508_0.sdds.new.nl_corrected.cleaned': '(6.2 , 4.9)',
                'Beam2@Turn@2012_06_25@03_25_13_860_0.sdds.new.nl_corrected.cleaned': '(5.5 , 5.1)'
                 }
    file_label = labels[file_name]
    return file_label

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

    # model_directory = []
    # kick_simulations = ['sig63', 'sig7', 'sig73', 'sig77', 'sig8', 'sig85']

    sdds_experimental = ['/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_55_09_762_0/Beam2@Turn@2012_06_25@03_55_09_762_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_49_40_281_0/Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_44_50_218_0/Beam2@Turn@2012_06_25@03_44_50_218_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_36_40_108_0/Beam2@Turn@2012_06_25@03_36_40_108_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_30_55_508_0/Beam2@Turn@2012_06_25@03_30_55_508_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_25_13_860_0/Beam2@Turn@2012_06_25@03_25_13_860_0.sdds.new.nl_corrected.cleaned',
                         ]
 
    # for simulation in kick_simulations:
    #     model_directory.append(os.path.join('/afs/cern.ch/work/f/fcarlier/public/simulations/kick_var/',simulation))

    # # model_directory = '/afs/cern.ch/work/f/fcarlier/public/simulations/single_part_jobs/'
    # sdds_models = get_models(model_directory)


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

    plot_tunes(sdds_file_path=sdds_models, sdds_experimental=sdds_experimental, output_file=None)
