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

    for plane in bpm_data:
        bpm_data[plane] = sort_data(*bpm_data[plane])

    return bpm_data


def fft_BPM_data(BPMdata):
    return abs(np.fft.fft(BPMdata))


def normalize_spectra(data):
    m = max(data)
    return np.divide(data, m)


def plot_single_BPM_data(bpm_name, sdds_model, measurement_list, output_file=None):

    fft_bpm = []

    bpm_model_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_model)
    for measurement in measurement_list:
        bpm_experimental_data = read_BPM_data_from_SDDS_file(bpm_name, measurement, start_turn=0)

        # setup data sets

        fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
        fft_bpm_experimental = [fft_BPM_data(bpm_experimental_data['X']), fft_BPM_data(bpm_experimental_data['Y'])]
        fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)
        fft_tune_experimental = np.fft.fftfreq(len(bpm_experimental_data['X']), d=1.)

        # sort data sets
        # fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
        fft_bpm_experimental = [sort_data(fft_tune_experimental, d) for d in fft_bpm_experimental]
        fft_bpm_experimental = [normalize_spectra(fft_bpm_experimental[0]), normalize_spectra(fft_bpm_experimental[1])]

        #fft_tune_model = np.array(sorted(fft_tune_model))
        fft_tune_experimental = np.array(sorted(fft_tune_experimental))
        fft_bpm.append(fft_bpm_experimental)

    fig = plt.figure(figsize=(23, 9))
    fig.patch.set_facecolor('white')
    tx = fig.add_subplot(1, 1, 1)


    tx.set_xlabel('X Plane - Frequency [tune units] ')
    tx.set_ylabel('Normalized amplitude (log.)')

    tx.plot(fft_tune_experimental, fft_bpm[2][0], label='Raw', color='b', linewidth=1.4)
    tx.plot(fft_tune_experimental, fft_bpm[0][0], label='Old corrections', color='g', linewidth=1.4)
    tx.plot(fft_tune_experimental, fft_bpm[1][0], label='New corrections', color='r', linewidth=1.4)

    tx.set_xlim([0., .5])
    tx.set_ylim([1e-4, 1.3])
    tx.grid(which='both', linewidth=.1, linestyle='dotted', color='black')
    tx.xaxis.set_tick_params(width=2, length=5)
    tx.yaxis.set_tick_params(width=2, length=5)
    tx.xaxis.set_major_locator(MultipleLocator(.05))

    tx.legend(shadow=True, fancybox=True, loc=1)

    tx.semilogy()

    #plt.subplots_adjust(left=0.04, right=0.98, top=0.95, bottom=0.05)
    plt.subplots_adjust(left=0.08, right=0.96, top=0.9, bottom=0.1)

    print "Outputfile:", output_file
    if not output_file:
        plt.show()
    else:
        plt.gcf().set_size_inches(20, 12)
        plt.savefig(output_file, dpi=400)


def do_plot(measurement_list, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/models/old/result.sdds',
            bpms_to_plot=['BPM.33R3.B2']):
    for bpm in bpms_to_plot:
        if output_file_path:
            output_file = output_file_path + '_' + bpm + '.pdf'
        else:
            output_file = None
        plot_single_BPM_data(bpm_name=bpm, sdds_model=sdds_model, measurement_list=measurement_list, output_file=output_file)


if __name__ == '__main__':

    sdds_path_list = []
    measurement_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/'
    measurement_name = 'Beam2@Turn@2012_06_25@04_00_22_346_0'
    sdds_experimental = measurement_name+'.sdds.new.nl_corrected.cleaned'

    type_list = ['old_corrections','variation_f20', 'raw_svd18']#
    
    for item in type_list:
        measurement_path = os.path.join(measurement_directory,item,measurement_name,sdds_experimental)
        sdds_path_list.append(measurement_path)
    sdds_path_list = ['/afs/cern.ch/work/f/fcarlier/public/MD12/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned']

    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/spectra/ONR_04_00_old_corr'


    output_file_path = None

    do_plot(measurement_list=sdds_path_list, output_file_path=output_file_path,bpms_to_plot=['BPM.33R3.B2'])  #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])

