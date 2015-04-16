import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
    bpm_data = {}

    assert os.path.exists(sdds_file_path)
    with open(sdds_file_path) as sdds_file:
        for line in sdds_file:
            line = line.split()
            if line[1] == bpm_name:
                assert line[0] in ['0', '1']
                if line[0] == '0':
                    plane = 'X'
                else:
                    plane = 'Y'
                if not start_turn: start_turn = 0
                if not end_turn: end_turn = len(line)
                bpm_data[plane] = [float(d) * normalization_factor for d in line[3 + start_turn:end_turn]]
    return bpm_data


def sort_data(dataX, dataY):
    assert len(dataX) == len(dataY)
    dataX, dataY = zip(*sorted(zip(dataX, dataY)))
    return np.array(dataY)


def read_BPM_spectra_from_BPM_files(bpm_name, sdds_file_path):
    bpm_data = {'X': [[], []], 'Y': [[], []]}
    bpm_directory = os.path.join(os.path.dirname(sdds_file_path), 'BPM/')
    bpm_file_paths = {'X': os.path.join(bpm_directory, bpm_name + '.x'),
                      'Y': os.path.join(bpm_directory, bpm_name + '.y')}

    for plane in bpm_file_paths:
        with open(bpm_file_paths[plane]) as bpm_file:
            for line in bpm_file:
                if not line.startswith('*') and not line.startswith('$'):
                    line = line.split()
                    bpm_data[plane][0].append(float(line[0]))
                    bpm_data[plane][1].append(float(line[1]))

    bpm_data['X'][0],bpm_data['X'][1] = zip(*sorted(zip(bpm_data['X'][0],bpm_data['X'][1])))
    bpm_data['Y'][0],bpm_data['Y'][1] = zip(*sorted(zip(bpm_data['Y'][0],bpm_data['Y'][1])))

    bpm_data['X'] = np.array(bpm_data['X'], dtype=np.double)
    bpm_data['Y'] = np.array(bpm_data['Y'], dtype=np.double)
    bpm_data['X'][1] = bpm_data['X'][1]/np.amax(bpm_data['X'][1]) 
    bpm_data['Y'][1] = bpm_data['Y'][1]/np.amax(bpm_data['Y'][1]) 

    return bpm_data


def fft_BPM_data(BPMdata):
    return abs(np.fft.fft(BPMdata))


def normalize_spectra(data):
    m = max(data)
    return np.divide(data, m)

def norm_sussix(data):
    maxx =  max(data['X'][0])
    maxy =  max(data['Y'][0])
    data['X'][0] = tuple(x/maxx for x in data['X'][0]) 
    data['Y'][0] = tuple(y/maxy  for y in data['Y'][0])
    return data  

def plot_single_BPM_data(bpm_name, sdds_model, measurement_list, output_file=None):

    fft_bpm = []

    bpm_model_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_model) 
    bpm_experimental_data = read_BPM_data_from_SDDS_file(bpm_name, measurement_list, start_turn=0)
    
#     bpm_sussix_mod = read_BPM_spectra_from_BPM_files(bpm_name, sdds_model)
#     bpm_sussix_exp = read_BPM_spectra_from_BPM_files(bpm_name, measurement_list)
#     bpm_sussix_mod = norm_sussix(bpm_sussix_mod)
#     bpm_sussix_exp = norm_sussix(bpm_sussix_exp)
    # setup data sets

    fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
    fft_bpm_experimental = [fft_BPM_data(bpm_experimental_data['X'][45:1600]), fft_BPM_data(bpm_experimental_data['Y'][45:1600])]
    fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)
    fft_tune_experimental = np.fft.fftfreq(len(bpm_experimental_data['X'][45:1600]), d=1.)


    # sort data sets
    fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
    fft_bpm_model = [normalize_spectra(fft_bpm_model[0]), normalize_spectra(fft_bpm_model[1])]
    fft_bpm_experimental = [sort_data(fft_tune_experimental, d) for d in fft_bpm_experimental]
    fft_bpm_experimental = [normalize_spectra(fft_bpm_experimental[0]), normalize_spectra(fft_bpm_experimental[1])]

    fft_tune_model = np.array(sorted(fft_tune_model))
    fft_tune_experimental = np.array(sorted(fft_tune_experimental))

#     fig3 = plt.figure(figsize=(10,7))
#     t3 = fig3.add_subplot(111)
#     t3.plot(bpm_sussix_exp['X'][0], bpm_sussix_exp['X'][1], label='Measurement' )
#     # t3.plot(bpm_sussix_mod['X'][0], bpm_sussix_mod['X'][1], label='Measurement' )
# 
#     # markerline2, stemlines2, baseline2 = t3.stem(bpm_sussix_exp['X'][0], bpm_sussix_exp['X'][1], '-.', bottom=1e-9, markerfmt = " ")
#     # plt.setp(baseline2, 'color','r', 'linewidth', 3)
#     # plt.setp(stemlines2, 'color', 'r', 'linewidth', 2, 'linestyle', 'solid')
# 
#     markerline, stemlines, baseline = t3.stem(bpm_sussix_mod['X'][0], bpm_sussix_mod['X'][1], '-.', bottom=1e-9, markerfmt = " ")
#     plt.setp(baseline, 'color','r', 'linewidth', 3)
#     plt.setp(stemlines, 'color', 'b', 'linewidth', 2, 'linestyle', 'solid')
# 
#     t3.set_xlabel('X Plane - Frequency [tune units] ')
#     t3.set_ylabel('Norm. amplitude (log.)')
#     t3.set_xlim([0., .5])
#     t3.set_ylim([2e-4, 2.5])
#     
    fig = plt.figure(figsize=(20, 7))
    fig.patch.set_facecolor('white')
    tx = fig.add_subplot(111)
    
    fig2 = plt.figure(figsize=(20, 7))
    fig2.patch.set_facecolor('white')
    ty = fig2.add_subplot(111)


    tx.set_xlabel('X Plane - Frequency [tune units] ')
    ty.set_xlabel('Y Plane - Frequency [tune units] ')
    tx.set_ylabel('Norm. amplitude (log.)')
    ty.set_ylabel('Norm. amplitude (log.)')

#     t3.plot([-10,-12],[-10,-12], color='b', label='5k tracking' )
    
    tx.plot(fft_tune_experimental, fft_bpm_experimental[0], label='Measurement', color='r')
    ty.plot(fft_tune_experimental, fft_bpm_experimental[1], label='Measurement', color='r')

    tx.plot(fft_tune_model, fft_bpm_model[0], label='5k tracking', color='b')
    ty.plot(fft_tune_model, fft_bpm_model[1], label='Model - 5k particle tracking', color='b')

#     tx.annotate('$Q_x + 2Q_y$', xy=(.1, 40), xytext=(.12, 100), arrowprops=dict(facecolor='black', shrink=0.05))
    tx.text(.09, .12, '(-1,-2)', fontsize=18)
    tx.text(.28, 1.3, '(1,0)', fontsize=18)  
    tx.text(.305, .18, '(0,1)', fontsize=18)  
    tx.text(.37, .07, '(0,2)', fontsize=18)  
    tx.text(.40, .04, '(1,1)', fontsize=18)  
    tx.text(.44 , .02, '(2,0)', fontsize=18)  
    tx.text(.01, .02, '(-1,1)', fontsize=18) 


#     t3.text(.08, .12, '(-1,-2)', fontsize=18)
#     t3.text(.26, 1.2, '(1,0)', fontsize=18)
#     t3.text(.295, .2, '(0,1)', fontsize=18)
#     t3.text(.35, .07, '(0,2)', fontsize=18)
#     t3.text(.39, .04, '(1,1)', fontsize=18)
#     t3.text(.42, .02, '(2,0)', fontsize=18)
#     t3.text(.01, .02, '(-1,1)', fontsize=18)


    tx.set_xlim([0., .5])
    tx.set_ylim([5e-4, 2.5])
    ty.set_xlim([0., .5])
    ty.set_ylim([5e-4, 2.5])

    tx.legend(shadow=False, fancybox=False, loc='upper left')
    ty.legend(shadow=False, fancybox=False, loc='upper left')
#     t3.legend(shadow=False, fancybox=False, loc='upper left')

#     t3.semilogy()
    tx.semilogy()
    ty.semilogy()

    fig.tight_layout()
    fig2.tight_layout()
#     fig3.tight_layout()

    plt.show()

# def do_plot(measurement_list, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/models/10k/multiParticle_10k_3mmKick.sdds', 
def do_plot(measurement_list, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nonlinear_8skick/combined/mps_combined.sdds',#mps_newdet_100.sdds', 
            bpms_to_plot=['BPM.33R3.B2']):#models/10k/multiParticle_10k_3mmKick.sdds',saddle2/mps_saddle_p100_j25_t1000_n2.sdds'
    for bpm in bpms_to_plot:
        if output_file_path:
            output_file = output_file_path + '_' + bpm + '.pdf'
        else:
            output_file = None
        plot_single_BPM_data(bpm_name=bpm, sdds_model=sdds_model, measurement_list=measurement_list, output_file=output_file)


if __name__ == '__main__':

    '''
        Add wanted measurements to plot by adding the directories to the type_list.
        measurement names may contain nl_corrected withouth having been corrected for path purposes
        - old_corrections :     Data with old linear corrections. not nl_corrected
        - variation_f20 :       Data with changed F coefficient in P5 corrections - 20*F
        - raw_svd18 :           Old corrections undone. SVD value of 18 to include 1,2 resonances
        - correctedSettings :   Old corrections reverted, and new P5 corrections applied

        Diagonal kicks measurement files:

        Beam2@Turn@2012_06_25@03_44_50_218_0/
        Beam2@Turn@2012_06_25@03_49_40_281_0/
        Beam2@Turn@2012_06_25@03_55_09_762_0/
        Beam2@Turn@2012_06_25@04_00_22_346_0/
    '''

    

    sdds_path_list = []
    measurement_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/'
    measurement_name = 'Beam2@Turn@2012_06_25@04_00_22_346_0'
    sdds_experimental = measurement_name+'.sdds.new.nl_corrected.cleaned'

    type_list = ['old_corrections','variation_f20', 'raw_svd18']#
    
    for item in type_list:
        measurement_path = os.path.join(measurement_directory,item,measurement_name,sdds_experimental)
        sdds_path_list.append(measurement_path)

    sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
#     sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/commissioning/Beam2@Turn@2015_04_09@01_58_48_846_0.new/Beam2@Turn@2015_04_09@01_58_48_846_0.sdds.new.new'
#     sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/commissioning/Beam1@Turn@2015_04_10@20_39_22_560_0.new/Beam1@Turn@2015_04_10@20_39_22_560_0.sdds.new.new'
    # sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@02_59_06_885_0/Beam2@Turn@2012_06_25@02_59_06_885_0.sdds.new.nl_corrected'
#     sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_02_48_230_0/Beam2@Turn@2012_06_25@03_02_48_230_0.sdds.new.nl_corrected'
#     sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_11_33_786_0/Beam2@Turn@2012_06_25@03_11_33_786_0.sdds.new.nl_corrected'
#     sdds_path_list = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_19_43_160_0/Beam2@Turn@2012_06_25@03_19_43_160_0.sdds.new.nl_corrected'
    # sdds_experimental =     '/afs/cern.ch/work/f/fcarlier/public/MD12/variation_Fcoefficient/Beam2@Turn@2012_06_25@04_00_22_346_0/f20/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
    # sdds_experimental_ref = '/afs/cern.ch/work/f/fcarlier/public/MD12/variation_Fcoefficient/Beam2@Turn@2012_06_25@04_00_22_346_0/fref/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
    # sdds_experimental_raw = '/afs/cern.ch/work/f/fcarlier/public/MD12/old_corrections/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.cleaned'

    # measurement_list = [sdds_experimental_raw, sdds_experimental_ref, sdds_experimental]
    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/spectra/ONR_04_00_old_corr'


    output_file_path = None

    do_plot(measurement_list=sdds_path_list, output_file_path=output_file_path,bpms_to_plot=['BPM.33R3.B2'])  #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])

