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

def sort_bpm_data(bpm_data):
    sorted_data = {'X':[[],[]], 'Y':[[],[]]}
    for plane in bpm_data:
        frequency = bpm_data[plane][0]
        amplitude = bpm_data[plane][1]
        sorted_data[plane][0],sorted_data[plane][1] = zip(*sorted(zip(frequency, amplitude)))
    return sorted_data

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

    colors = ['c','r','b','g']

    fig = plt.figure(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    tx = fig.add_subplot(111)

    fig2 = plt.figure(figsize=(10, 7))
    fig2.patch.set_facecolor('white')
    ty = fig2.add_subplot(111)

    SUSSIX = False
    if SUSSIX:
        for n in range(len(measurement_list)):
            sussix_exp_data = read_BPM_spectra_from_BPM_files(bpm_name, measurement_list[n])

            sussix_bpm_model = {'X':sussix_exp_data['X'][1], 'Y':sussix_exp_data['Y'][1]}
            sussix_tune_model = {'X':sussix_exp_data['X'][0], 'Y':sussix_exp_data['Y'][0]}

            # sussix_bpm_model['X'] = normalize_spectra(sussix_bpm_model['X'])
            # sussix_bpm_model['Y'] = normalize_spectra(sussix_bpm_model['Y'])
            sussix_bpm_stemx = sussix_bpm_model['X']
            # for i in range(len(sussix_bpm_model['X'])):
            #     if sussix_bpm_model['X'][i] < 1e-4:
            #         sussix_bpm_stemx[i] = 0.

    #             n_label= ['all off', 'mco val', '100x mco val', '1000x mco val', '2000x mco val', '5000x mco val']
            n_label= ['all off',  '1000x mco val', '2000x mco val', '5000x mco val']
            

            '''Plotting of SUSSIX data'''
            # tx.plot(sussix_tune_model['X'], sussix_bpm_model['X'],label='SUSSIX %s' % (n_label[n]), linewidth=2)
            # ty.plot(sussix_tune_model['Y'], sussix_bpm_model['Y'],label='SUSSIX %s' % (n_label[n]), linewidth=2)
            markerline, stemlines, baseline = tx.stem(sussix_tune_model['X'], sussix_bpm_model['X'], '-.', bottom=1e-9, markerfmt = " ")
            plt.setp(baseline, 'color','r', 'linewidth', 1)
            plt.setp(stemlines, 'color' , colors[n] , 'linewidth', 4, 'linestyle', 'solid')





    tx.set_xlabel('X Plane - Frequency [tune units] ')
    ty.set_xlabel('Y Plane - Frequency [tune units] ')
    tx.set_ylabel('Normalized amplitude (log.)')
    ty.set_ylabel('Normalized amplitude (log.)')

#     tx.plot(fft_tune_experimental, fft_bpm[2][0], label='Old corr.', color='b')
    tx.plot(fft_tune_experimental, fft_bpm[0][0], label='Old corr. ', color='r')
    tx.plot(fft_tune_experimental, fft_bpm[1][0], label='Adjusted data', color='b' )


    ty.plot(fft_tune_experimental, fft_bpm[0][1], label='Old corr. ', color='b')
    ty.plot(fft_tune_experimental, fft_bpm[1][1], label='Adjusted corr.', color='r')
#     ty.plot(fft_tune_experimental, fft_bpm[2][1], label='Old corr.', color='b')


    tx.text(.08, .12, '(-1,-2)', fontsize=18)
    tx.text(.26, 1.2, '(1,0)', fontsize=18)
    tx.text(.295, .15, '(0,1)', fontsize=18)
    tx.text(.36, .02, '(0,2)', fontsize=18)
    tx.text(.39, .04, '(1,1)', fontsize=18)
    tx.text(.42, .02, '(2,0)', fontsize=18)
    tx.text(.011, .015, '(-1,1)', fontsize=18)
    tx.text(.33, .07, '(1,-2)', fontsize=18)
    tx.text(.12, .02, '(2,1)', fontsize=18)


    tx.set_xlim([0., .5])
    ty.set_xlim([0., .5])
    tx.set_ylim([5e-4,2])
    ty.set_ylim([5e-4,1])

#     tx.xaxis.set_tick_params(width=2, length=5)
#     tx.yaxis.set_tick_params(width=2, length=5)
#     ty.xaxis.set_tick_params(width=2, length=5)
#     ty.yaxis.set_tick_params(width=2, length=5)
#     tx.xaxis.set_major_locator(MultipleLocator(.05))
#     ty.xaxis.set_major_locator(MultipleLocator(.05))

    tx.legend(fancybox=False, loc='upper left', fontsize=18)
    ty.legend(fancybox=True, loc=1)

    tx.semilogy()
    ty.semilogy()

    #plt.subplots_adjust(left=0.04, right=0.98, top=0.95, bottom=0.05)
    plt.subplots_adjust(left=0.08, right=0.96, top=0.9, bottom=0.1)


    fig.tight_layout()
    fig2.tight_layout()
    plt.show()


def do_plot(measurement_list, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/models/old/result.sdds',
            bpms_to_plot=['BPM.12L6.B2']):
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
    
#     for item in type_list:
#         measurement_path = os.path.join(measurement_directory,item,measurement_name,sdds_experimental)
#         sdds_path_list.append(measurement_path)
#     
#     sdds_path_list.append('/afs/cern.ch/work/f/fcarlier/public/MD12/old_corrections/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.cleaned')

    # sdds_experimental =     '/afs/cern.ch/work/f/fcarlier/public/MD12/variation_Fcoefficient/Beam2@Turn@2012_06_25@04_00_22_346_0/f20/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
    # sdds_experimental_ref = '/afs/cern.ch/work/f/fcarlier/public/MD12/variation_Fcoefficient/Beam2@Turn@2012_06_25@04_00_22_346_0/fref/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
    # sdds_experimental_raw = '/afs/cern.ch/work/f/fcarlier/public/MD12/old_corrections/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.cleaned'

    # measurement_list = [sdds_experimental_raw, sdds_experimental_ref, sdds_experimental]
    output_file_path = '/afs/cern.ch/work/f/fcarlier/public/plots/spectra/ONR_04_00_old_corr'

#     sdds_path_list =  ['/afs/cern.ch/work/f/fcarlier/public/MD12/variation_Fcoefficient/Beam2@Turn@2012_06_25@04_00_22_346_0/fnew/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
#                         '/afs/cern.ch/work/f/fcarlier/public/MD12/raw_svd18/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
#                         '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned']

    sdds_path_list =  ['/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
                        # '/afs/cern.ch/work/f/fcarlier/public/MD12/raw_svd18/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',
                       '/afs/cern.ch/work/f/fcarlier/public/MD12/variation_f20/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned',]

                      

    output_file_path = None

    do_plot(measurement_list=sdds_path_list, output_file_path=output_file_path,bpms_to_plot=['BPM.33R3.B2'])  #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])
