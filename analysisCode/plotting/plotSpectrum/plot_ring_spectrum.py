import os
import numpy as np

def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
    bpm_data = {}

    assert os.path.exists(sdds_file_path)
    with open(sdds_file_path) as sdds_file:
        for line in sdds_file:
            line = line.split()
            if not line.startswith('#'):
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

    #sussix_model_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_model)
    #sussix_experimental_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_experimental)

    fig = plt.figure(figsize=(23, 13))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(2,2,1)
    tx = fig.add_subplot(2,2,2)
    ay = fig.add_subplot(2,2,3)
    ty = fig.add_subplot(2,2,4)

    #tx = fig.add_subplot(1,1,1)
    #ty = fig.add_subplot(2,1,2)

    fig.suptitle(bpm_name)# + "  " + "F = F*40")
    ax.set_xlabel('$N$ [1]')
    tx.set_xlabel('$Q_x$ [1/turn]')
    ay.set_xlabel('$N$ [1]')
    ty.set_xlabel('$Q_y$ [1/turn]')
    ax.set_ylabel('X [mm]')
    tx.set_ylabel('Amp [a.u.]')
    ay.set_ylabel('Y [mm]')
    ty.set_ylabel('Amp [a.u.]')

    '''
    # rescale model data by factor 1000 (m -> mm)
    model_rescale_factor = 1000.
    bpm_model_data['X'] = [d*model_rescale_factor for d in bpm_model_data['X']]
    bpm_model_data['Y'] = [d*model_rescale_factor for d in bpm_model_data['Y']]
    sussix_model_data['X'][1] = [d*model_rescale_factor for d in sussix_model_data['X'][1]]
    sussix_model_data['Y'][1] = [d*model_rescale_factor for d in sussix_model_data['Y'][1]]
    '''

    # setup data sets
    fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
    fft_bpm_experimental = [fft_BPM_data(bpm_experimental_data['X']), fft_BPM_data(bpm_experimental_data['Y'])]
    fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)
    fft_tune_experimental = np.fft.fftfreq(len(bpm_experimental_data['X']), d=1.)

    # sort data sets
    #fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
    fft_bpm_experimental = [sort_data(fft_tune_experimental, d) for d in fft_bpm_experimental]
    #fft_tune_model = np.array(sorted(fft_tune_model))
    fft_tune_experimental = np.array(sorted(fft_tune_experimental))

    print fft_tune_experimental

    #sussix_bpm_model = {'X':sussix_model_data['X'][1], 'Y':sussix_model_data['Y'][1]}
    #sussix_bpm_experimental = {'X':sussix_experimental_data['X'][1], 'Y':sussix_experimental_data['Y'][1]}
    #sussix_tune_model = {'X':sussix_model_data['X'][0], 'Y':sussix_model_data['Y'][0]}
    #sussix_tune_experimental = {'X':sussix_experimental_data['X'][0], 'Y':sussix_experimental_data['Y'][0]}

    # normalize spectra to maximum
    #fft_bpm_model['X'] = normalize_spectra(fft_bpm_model['X'])
    #fft_bpm_model['Y'] = normalize_spectra(fft_bpm_model['Y'])
    #fft_bpm_experimental['X'] = normalize_spectra(fft_bpm_experimental['X'])
    #fft_bpm_experimental['Y'] = normalize_spectra(fft_bpm_experimental['Y'])

    #sussix_bpm_model['X'] = normalize_spectra(sussix_bpm_model['X'])
    #sussix_bpm_model['Y'] = normalize_spectra(sussix_bpm_model['Y'])
    #sussix_bpm_experimental['X'] = normalize_spectra(sussix_bpm_experimental['X'])
    #sussix_bpm_experimental['Y'] = normalize_spectra(sussix_bpm_experimental['Y'])

    # actual plotting
    #ax.plot(bpm_model_data['X'], label='Model')
    #tx.plot(fft_tune_model, fft_bpm_model[0], label='FFT Model', color='black')
    #ay.plot(bpm_model_data['Y'], label='Model')
    #ty.plot(fft_tune_model, fft_bpm_model[1], label='FFT Model', color='black')

    ax.plot(bpm_experimental_data['X'], label='Data')
    tx.plot(fft_tune_experimental, fft_bpm_experimental[0], label='FFT Data', color='r')
    ay.plot(bpm_experimental_data['Y'], label='Data')
    ty.plot(fft_tune_experimental, fft_bpm_experimental[1], label='FFT Data', color='r')

    # Plot vertical lines for resonances of F*xy**2 and F*yx**2
    tx.plot((.13, .13), (.01, 5), 'k-')
    tx.plot((.25, .25), (.01, 5), 'k-')
    tx.plot((.1, .1), (.01, 5), 'k-')
    tx.plot((.34, .34), (.01, 5), 'k-')

    ty.plot((.13, .13), (.01, 5), 'k-')
    ty.plot((.25, .25), (.01, 5), 'k-')
    ty.plot((.1, .1), (.01, 5), 'k-')
    ty.plot((.34, .34), (.01, 5), 'k-')

    ax.set_xlim(0, len(bpm_model_data['X']))
    tx.set_xlim([0., .5])
    ay.set_xlim(0, len(bpm_model_data['Y']))
    ty.set_xlim([0., .5])

    ax.grid(which='both')
    tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
    ay.grid(which='both')
    ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')

    tx.xaxis.set_major_locator(MultipleLocator(.1))
    ty.xaxis.set_major_locator(MultipleLocator(.1))

    ax.legend(title='Legend', shadow=True, ncol=2, fancybox=True)
    tx.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
    ay.legend(title='Legend', shadow=True, ncol=2, fancybox=True)
    ty.legend(title='Y Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})

    tx.semilogy()
    ty.semilogy()

    #plt.subplots_adjust(left=0.04, right=0.98, top=0.95, bottom=0.05)
    plt.subplots_adjust(left=0.08, right=0.96, top=0.9, bottom=0.1)

    plt.show()

def do_plot(sdds_experimental, output_file_path=None, sdds_model='/afs/cern.ch/work/f/fcarlier/public/models/10k/multiParticle_10k_3mmKick.sdds', bpms_to_plot=['BPM.33R3.B2']):
    for bpm in bpms_to_plot:
        if output_file_path: output_file = output_file_path + '_' + bpm + '.pdf'
        else: output_file = None
        plot_single_BPM_data(bpm, sdds_model, sdds_experimental, output_file=output_file)


if __name__=='__main__':
    working_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/'
    measurement_folder = os.listdir(working_directory)[12] # There is a total of 28 measurements in folder MD12
    bpm_data_filepath = working_directory+measurement_folder+'/'+measurement_folder+'.sdds.new.nl_corrected.cleaned'
    
    bpm_name = 'BPM.33R3.B2'


    do_plot(sdds_experimental=bpm_data_filepath, output_file_path='/afs/cern.ch/work/f/fcarlier/public/', bpms_to_plot=['BPM.33R3.B2']) #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])
