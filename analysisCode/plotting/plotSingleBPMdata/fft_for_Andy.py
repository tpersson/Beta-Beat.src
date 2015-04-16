import os
import numpy as np

#====================================================================================================    
#               MAIN PART
#====================================================================================================


def plot_single_BPM_data(bpm_name, sdds_model, output_file=None, SUSSIX=True):

    if SUSSIX:
        for n in range(len(sdds_model)):
            sussix_model_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_model[n])

            sussix_bpm_model = {'X':sussix_model_data['X'][1], 'Y':sussix_model_data['Y'][1]}
            sussix_tune_model = {'X':sussix_model_data['X'][0], 'Y':sussix_model_data['Y'][0]}

            # sussix_bpm_model['X'] = normalize_spectra(sussix_bpm_model['X'])
            # sussix_bpm_model['Y'] = normalize_spectra(sussix_bpm_model['Y'])

    else:
        for n in range(len(sdds_model)):
            bpm_model_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_model[n])

            fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
            fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)

            fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
            fft_bpm_model = [normalize_spectra(fft_bpm_model[0]),normalize_spectra(fft_bpm_model[1])]
            fft_tune_model = np.array(sorted(fft_tune_model))
 
#====================================================================================================    
#               HELPER FUNCTIONS
#====================================================================================================


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


''' Sort obtained dictionary: bpm_data in order of frequency '''
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


def find_12_spectral(data):
    data_start = len(data)/2 + 2
    data_end   = len(data)/2 + len(data)/8
    sample_data = data[data_start:data_end]
    [maximum, max_index] = find_maximum(sample_data)
    return [maximum, max_index + data_start]


def find_maximum(data):
    maximum = max(data)
    max_index = np.argmax(data)
    return [maximum, max_index]

#====================================================================================================    
#               MAIN INVOCATION
#====================================================================================================


if __name__=='__main__':

    sdds_models         = [ '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newmco/nom/mco_nonew.sdds',
                            '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newmco/new/mcovar.sdds',
                            '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newmco/no_oct/mco_no_oct.sdds',
                            '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newmco/otherline1102/mcovar_new.sdds']

    output_file_path  = '/afs/cern.ch/work/f/fcarlier/public/plots/model/spectra/multiple2.pdf'
    output_file_path  = None

    plot_single_BPM_data(bpm_name='BPM.33R3.B2', sdds_model=sdds_models, output_file=output_file_path, SUSSIX = False )