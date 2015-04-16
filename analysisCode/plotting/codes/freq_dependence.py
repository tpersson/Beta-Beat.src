import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from pylab import *
import scipy as sp
from scipy import stats
#====================================================================================================    
#               MAIN PART 
#====================================================================================================

def determine_frequencies(sdds_experimental_path, bpm_name, output_file):
    sussix_experimental_data = []
    sussix_bpm_experimental  = []
    sussix_tune_experimental = [] 
    maxima = []
    freq   = []
    main_tunes = {'X':[], 'Y':[]}


    for n in range(len(sdds_experimental_path)):
        measurement = sdds_experimental_path[n]
        sussix_experimental_data = read_BPM_spectra_from_BPM_files(bpm_name, measurement)
        sussix_bpm_experimental = {'X':sussix_experimental_data['X'][1], 'Y':sussix_experimental_data['Y'][1]}
        sussix_tune_experimental = {'X':sussix_experimental_data['X'][0], 'Y':sussix_experimental_data['Y'][0]}
        
        [maximum, max_index] = find_12_spectral(sussix_bpm_experimental['X'])
        maxima.append(maximum)
        freq.append(sussix_tune_experimental['X'][max_index])

        [tune_x, tune_y] = get_main_tunes(measurement)
        main_tunes['X'].append(tune_x)
        main_tunes['Y'].append(tune_y)

    spectral_12 = calc_expected_12(main_tunes)

    spectral = {'measured_12':np.array(spectral_12), 'calculated_12':np.array(freq) }

    label=['(0.53 , 0.33)','(0.48 , 0.30)','(0.45 , 0.29)','(0.4  , 0.25)','(0.37 , 0.23)','(0.3  , 0.19)','(0.24 , 0.20)']
 

    fig = plt.figure(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    t1 = fig.add_subplot(1, 1, 1)
    # fig.suptitle('Change of 1,2 spectral line vs. main tunes')
    t1.set(xlabel='$-Qx - 2Qy$',ylabel='Measured $(-1,-2)$', xlim= [.0942,.0956])
    # t1.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    t1.xaxis.set_major_locator(MultipleLocator(.0005))
    t1.yaxis.set_major_locator(MultipleLocator(.0005))
    t1.xaxis.set_tick_params(width=2, length=5)
    t1.yaxis.set_tick_params(width=2, length=5)
        
    fit = polyfit(freq, spectral_12, 1) 
    fit_fn = poly1d(fit)
    x_range = np.linspace(0.094,0.096,10)
    t1.set_xlim([0.094,0.096])
    t1.set_ylim([0.094,0.096])
    t1.plot(x_range, fit_fn(x_range),'k--', ms=9, label='Linear fit')
    t1.plot([-1,-3], [-1,-3],'white', label=' ')
    t1.plot([-1,-3], [-1,-3],'white', label='2Jx   ,   2Jy')


    for i in range(len(freq)):
        t1.plot(freq[i], spectral_12[i], 'o',  ms=20, label=label[i])
    t1.legend(shadow=False, fancybox=False, numpoints=1, loc=9, bbox_to_anchor=(1.26,0.9), fontsize=20)


    fig.canvas.draw()
    labels = [item.get_text() for item in t1.get_xticklabels()]
    labels[0] = ' '
    # labels = labels*10e6
    t1.set_xticklabels(labels)

    fig.subplots_adjust(left=.16, right=.71, bottom=.15, top=.9)
    plt.show()

#====================================================================================================    
#               SUPPLEMENTARY FUNCTIONS
#====================================================================================================

''' Read bpm data functions '''
def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
    bpm_data = {}

    assert os.path.exists(sdds_file_path)
    with open(sdds_file_path) as sdds_file:
        for line in sdds_file:
            line = line.split()
            if line[1] == bpm_name:
                assert line[0] in ['0', '1']
                if line[0] == '0': plane = 'X'
                else: plane = 'Y'
                if not start_turn: start_turn = 0
                if not end_turn: end_turn = len(line)
                bpm_data[plane] = [float(d)*normalization_factor for d in line[3+start_turn:end_turn]]
    return bpm_data

def read_BPM_spectra_from_BPM_files(bpm_name, sdds_file_path):
    bpm_data = {'X':[[], []], 'Y':[[], []]}
    bpm_directory = os.path.join(os.path.dirname(sdds_file_path), 'BPM/')
    bpm_file_paths = {'X':os.path.join(bpm_directory, bpm_name + '.x'), 'Y':os.path.join(bpm_directory, bpm_name + '.y')}

    for plane in bpm_file_paths:
        with open(bpm_file_paths[plane]) as bpm_file:
            for line in bpm_file:
                if not line.startswith('*') and not line.startswith('$'):
                    line = line.split()
                    bpm_data[plane][0].append(float(line[0]))
                    bpm_data[plane][1].append(float(line[1]))

    bpm_data_sorted = sort_bpm_data(bpm_data)               
    return bpm_data_sorted


''' Sort data functions '''
def sort_data(dataX, dataY):
    assert len(dataX) == len(dataY)
    dataX, dataY = zip(*sorted(zip(dataX, dataY)))
    return np.array(dataY)

def sort_bpm_data(bpm_data):
    sorted_data = {'X':[[],[]], 'Y':[[],[]]}
    for plane in bpm_data:
        frequency = bpm_data[plane][0]
        amplitude = bpm_data[plane][1]
        sorted_data[plane][0],sorted_data[plane][1] = zip(*sorted(zip(frequency, amplitude)))
    return sorted_data


''' Other tools '''
def fft_BPM_data(BPMdata):
    return abs(np.fft.fft(BPMdata))

def normalize_spectra(data):
    m = max(data)
    return np.divide(data, m)

def find_12_spectral(data):
    data_start = len(data)/2 + 5
    data_end   = len(data)/2 + len(data)/8
    sample_data = data[data_start:data_end]
    [maximum, max_index] = find_maximum(sample_data)
    return [maximum, max_index + data_start]

def find_maximum(data):
    maximum = max(data)
    max_index = np.argmax(data)
    return [maximum, max_index]

def get_main_tunes(sdds_file_path):
    getllm_directory = os.path.join(os.path.dirname(sdds_file_path), 'getllm/')
    tune_file_path   = os.path.join(getllm_directory,'getphasetotx.out')

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

def calc_expected_12(main_tunes):
    result = []
    for i in range(len(main_tunes['X'])):
        spectral_line = 1 - (main_tunes['X'][i] + 2*main_tunes['Y'][i])
        result.append(spectral_line)
    return result

#====================================================================================================    
#               MAIN INVOCATION
#====================================================================================================

if __name__=='__main__':
    sdds_experimental_path=['/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_55_09_762_0/Beam2@Turn@2012_06_25@03_55_09_762_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_49_40_281_0/Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_44_50_218_0/Beam2@Turn@2012_06_25@03_44_50_218_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_36_40_108_0/Beam2@Turn@2012_06_25@03_36_40_108_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_30_55_508_0/Beam2@Turn@2012_06_25@03_30_55_508_0.sdds.new.nl_corrected.cleaned',
                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_25_13_860_0/Beam2@Turn@2012_06_25@03_25_13_860_0.sdds.new.nl_corrected.cleaned',
                         ]

    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/spectral_dependency.pdf'
    output_file_path = None

    determine_frequencies(sdds_experimental_path, bpm_name='BPM.33R3.B2', output_file=output_file_path)
