import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
from pylab import *

#====================================================================================================    
#               MAIN PART 
#====================================================================================================

def determine_frequencies(sdds_experimental_path, bpm_name, output_file):
    sussix_experimental_data = []
    sussix_bpm_experimental  = []
    sussix_tune_experimental = [] 
    maxima = []
    freq   = []
    main_tunes = {'X':[], 'XRMS':[], 'Y':[], 'YRMS':[]}


    for n in range(len(sdds_experimental_path)):
        measurement = sdds_experimental_path[n]
        sussix_experimental_data = read_BPM_spectra_from_BPM_files(bpm_name, measurement)
        sussix_bpm_experimental = {'X':sussix_experimental_data['X'][1], 'Y':sussix_experimental_data['Y'][1]}
        sussix_tune_experimental = {'X':sussix_experimental_data['X'][0], 'Y':sussix_experimental_data['Y'][0]}
        
        [maximum, max_index] = find_12_spectral(sussix_bpm_experimental['X'])
        maxima.append(maximum)
        freq.append(sussix_tune_experimental['X'][max_index])

        [tune_x, tune_x_rms, tune_y, tune_y_rms] = get_main_tune(measurement)
        main_tunes['X'].append(tune_x)
        main_tunes['XRMS'].append(tune_x_rms)
        main_tunes['Y'].append(tune_y)
        main_tunes['YRMS'].append(tune_y_rms)

    print main_tunes
    [spectral_12, spectral_12_rms] = calc_expected_12(main_tunes)
    
    
    fig = plt.figure(figsize=(12, 10))
    fig.patch.set_facecolor('white')
    t1 = fig.add_subplot(1, 1, 1)
    # fig.suptitle('Change of 1,2 spectral line vs. main tunes')
    t1.set(xlabel='$Q_x + 2Q_y$',ylabel='Frequency of (1,2) spectral line', xlim= [.0939,.0961], ylim= [.0939,.0961])
    t1.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    t1.xaxis.set_major_locator(MultipleLocator(.0005))
    t1.yaxis.set_major_locator(MultipleLocator(.0005))
    t1.xaxis.set_tick_params(width=2, length=5)
    t1.yaxis.set_tick_params(width=2, length=5)
    
    fit = polyfit(freq, spectral_12, 1) 
    fit_fn = poly1d(fit)
    print 'fit:  ', fit
    x_range = np.linspace(0.0939,0.0961,10)
    t1.plot(x_range, fit_fn(x_range),'r--', ms=9, label='Linear fit')
    for i in range(7):
        t1.errorbar(freq[i], spectral_12[i], xerr=spectral_12_rms[i], yerr = 0, fmt='o',  ms=9, label='Expected 12')


    # fig = plt.figure(figsize=(23, 13))
    # fig.patch.set_facecolor('white')
    # t1 = fig.add_subplot(3, 1, 1)
    # tx = fig.add_subplot(3, 1, 2)
    # ty = fig.add_subplot(3, 1, 3)

    # fig.suptitle('Change of 1,2 spectral line vs. main tunes')
    # t1.set_xlabel('measurement [a.u.]')
    # t1.set_ylabel('12 frequency')
    # tx.set_xlabel('Main tune Qx')
    # tx.set_ylabel('12 frequency')
    # ty.set_xlabel('Main tune Qy')
    # ty.set_ylabel('12 frequency')

    # t1.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    # tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    # ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')

    # #   AS A FUNCTION OF MEASUREMENTS
    # t1.plot(range(1,6), spectral_12, 'ro--', label='Expected 12')
    # t1.plot(range(1,6), freq, 'bo--', label='Expected 12')

    # #   AS A FUNCTION OF Qx AND Qy
    # tx.plot(main_tunes['X'], spectral_12, 'ro--', label='Expected 12')
    # tx.plot(main_tunes['X'], freq, 'bo--', label='Expected 12')

    # ty.plot(main_tunes['Y'], spectral_12, 'ro--', label='Expected 12')
    # ty.plot(main_tunes['Y'], freq, 'bo--', label='Expected 12')

    if not output_file:
        plt.tight_layout()
        plt.show()
    else:
        plt.gcf().set_size_inches(20, 12)
        plt.savefig(output_file, dpi=400)

    print 'MAX:  ', maxima, 'FREQ:  ', freq
    print 'TUNE_X:  ', main_tunes['X'], 'TUNE_Y:  ', main_tunes['Y']
    print 'EXPECTED LINE:  ', spectral_12

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

def get_main_tune(sdds_file_path):
    getllm_directory = os.path.join(os.path.dirname(sdds_file_path), 'getllm/')
    tune_file_path   = os.path.join(getllm_directory,'getkick.out')
    
    for line in open(tune_file_path).readlines():
        line = line.split()
        if line[0] == '0.0':
            tune_x      = float(line[1])
            tune_x_rms  = float(line[2])
            tune_y      = float(line[3])
            tune_y_rms  = float(line[4])

    return [tune_x, tune_x_rms, tune_y, tune_y_rms]


    
def calc_expected_12(main_tunes):
    result = []
    rms = []
    for i in range(len(main_tunes['X'])):
        spectral_line = 1 - (main_tunes['X'][i] + 2*main_tunes['Y'][i])
        spectral_rms  = np.sqrt(main_tunes['XRMS'][i]**2 + 4*main_tunes['YRMS'][i]**2)
        result.append(spectral_line)
        rms.append(spectral_rms)
    return [result, rms]

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
