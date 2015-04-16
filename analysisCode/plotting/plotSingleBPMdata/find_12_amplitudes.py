import os
import numpy as np

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

def sort_data(dataX, dataY):
    assert len(dataX) == len(dataY)
    dataX, dataY = zip(*sorted(zip(dataX, dataY)))
    return np.array(dataY)

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

    for plane in bpm_data:
        bpm_data[plane] = sort_data(*bpm_data[plane])

    return bpm_data

def fft_BPM_data(BPMdata):
    return abs(np.fft.fft(BPMdata))

def normalize_spectra(data):
    m = max(data)
    return np.divide(data, m)

def plot_single_BPM_data(bpm_name, sdds_model, sdds_experimental, output_file=None):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator

    bpm_model_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_model)
    bpm_experimental_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_experimental, start_turn=0)

    # setup data sets
    fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
    fft_bpm_experimental = [fft_BPM_data(bpm_experimental_data['X']), fft_BPM_data(bpm_experimental_data['Y'])]
    fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)
    fft_tune_experimental = np.fft.fftfreq(len(bpm_experimental_data['X']), d=1.)

    # sort data sets
    fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
    fft_bpm_experimental = [sort_data(fft_tune_experimental, d) for d in fft_bpm_experimental]
    fft_tune_model = np.array(sorted(fft_tune_model))
    fft_tune_experimental = np.array(sorted(fft_tune_experimental))

    maxima.append(max(fft_bpm_experimental[0][1001:1300]))
    max_index = np.argmax(fft_bpm_experimental[0][1001:1300])

    print used_coefficients
    print "maximum:", maxima, "1,2 tune:", fft_tune_experimental[max_index+1001]

def do_plot(sdds_experimental, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/MD12/models/result.sdds', bpms_to_plot=['BPM.33R3.B2']):
    for bpm in bpms_to_plot:
        if output_file_path: output_file = output_file_path + '_' + bpm + '.pdf'
        else: output_file = None
        plot_single_BPM_data(bpm, sdds_model, sdds_experimental, output_file=output_file)

if __name__=='__main__':
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MultipleLocator

    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/spectra/varF_'+"03asdf_44"

    # iteration_order = ['f_100', 'f_80', 'f_60', 'f_40', 'f_20', 'f_ref', 'f0', 'fref', 'f10', 'f20', 'f40', 'f60', 'f80', 'f100']
    iteration_order = ['f_60', 'f_40', 'f_20', 'f_ref', 'f0', 'fref', 'f10', 'f20', 'f40', 'f60']
    # coeff_list = {'f_100':-100 , 'f_80':-80 , 'f_60':-60 , 'f_40':-40 , 'f_20':-20 , 'f_ref':-1, 'f0':0 , 'fref':1 , 'f10':10 , 'f20':20 , 'f40':40 , 'f60':60 , 'f80':80 , 'f100':100 }
    coeff_list = {'f_60':-60 , 'f_40':-40 , 'f_20':-20 , 'f_ref':-1, 'f0':0 , 'fref':1 , 'f10':10 , 'f20':20 , 'f40':40 , 'f60':60}
    used_coefficients = []
    maxima = []

    for key in iteration_order:
        if key in coeff_list:
            # sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/varF/Beam2@Turn@2012_06_25@04_00_22_346_0/'+key+'/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'  #-100 to 100
            # sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/varF/Beam2@Turn@2012_06_25@03_55_09_762_0/'+key+'/Beam2@Turn@2012_06_25@03_55_09_762_0.sdds.new.nl_corrected.cleaned'  #-100 to 100
            # sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/varF/Beam2@Turn@2012_06_25@03_49_40_281_0/'+key+'/Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned'  #-60 to 60
            sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/varF/Beam2@Turn@2012_06_25@03_44_50_218_0/'+key+'/Beam2@Turn@2012_06_25@03_44_50_218_0.sdds.new.nl_corrected.cleaned'  #-60 to 60

            output_file_path = None
            value = coeff_list[key]
            used_coefficients.append(value)

            do_plot(sdds_experimental, output_file_path=output_file_path, bpms_to_plot=['BPM.33R3.B2']) #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])

    if output_file_path: output_file = output_file_path + '.pdf'
    else: output_file = None

    fig1 = plt.figure(figsize=(23, 13))
    fig1.patch.set_facecolor('white')
    fig1.suptitle('BPM.33R3.B2' + ' - ' + '03_44')

    plt.scatter(used_coefficients,maxima, label='Maxima', color='r')
    plt.plot(used_coefficients,maxima, label='Maxima', color='r',linestyle='--')
    plt.xlabel('n*F',fontsize = 12)
    plt.ylabel('Amplitude (a.u)', fontsize = 12)
    plt.grid(which='both', linewidth=.1, linestyle='-', color='grey')

    if not output_file:
        plt.show()
    else:
        plt.gcf().set_size_inches(20, 12)
        plt.savefig(output_file, dpi=400)

import numpy as np
