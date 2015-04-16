import os
import numpy as np
from scipy.interpolate import interp1d
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


#====================================================================================================    
#               MAIN PART
#====================================================================================================


def plot_single_BPM_data(bpm_name, sdds_model, sdds_experimental, output_file=None, SUSSIX=True):

    
    ''' SET FIGURE 1'''
    fig = plt.figure(figsize=(23, 18))
    fig.patch.set_facecolor('white')
#     fig.suptitle(bpm_name + " : " +"Single Particle Simulation - Re 2020")
    tx = fig.add_subplot(2,1,1)
    ty = fig.add_subplot(2,1,2)



    tx.set(xlabel=('X Plane - Frequency [tune units] '), ylabel=('Normalized amplitude'), xlim=([0., .5]), ylim=([1e-5, 1.3]))
    ty.set(xlabel=('Y Plane - Frequency [tune units] '), ylabel=('Normalized amplitude'), xlim=([0., .5]), ylim=([1e-5, 1.3]))
    tx.xaxis.set_major_locator(MultipleLocator(.05))
    ty.xaxis.set_major_locator(MultipleLocator(.05))
    tx.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
    ty.legend(title='Y Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})

    if SUSSIX:
        interp_function = []
        xnew = np.linspace(0,.4,100)

        for n in range(len(sdds_model)):
            sussix_model_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_model[n])

            sussix_bpm_model = {'X':sussix_model_data['X'][1], 'Y':sussix_model_data['Y'][1]}
            sussix_tune_model = {'X':sussix_model_data['X'][0], 'Y':sussix_model_data['Y'][0]}

            sussix_bpm_model['X'] = normalize_spectra(sussix_bpm_model['X'])
            sussix_bpm_model['Y'] = normalize_spectra(sussix_bpm_model['Y'])

#             n_label= ['all off', 'mco val', '100x mco val', '1000x mco val', '2000x mco val', '5000x mco val']
            n_label= ['MCOs off',  'New MCO strengths', '2000x mco val', '5000x mco val']
                
            '''Plotting of SUSSIX data'''
            tx.plot(sussix_tune_model['X'], sussix_bpm_model['X'], label=' %s' % (n_label[n]), linewidth=2)
            ty.plot(sussix_tune_model['Y'], sussix_bpm_model['Y'], label=' %s' % (n_label[n]), linewidth=2)

    else:
        for n in range(len(sdds_model)):
            bpm_model_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_model[n])

            fft_bpm_model = [fft_BPM_data(bpm_model_data['X']), fft_BPM_data(bpm_model_data['Y'])]
            fft_tune_model = np.fft.fftfreq(len(bpm_model_data['X']), d=1.)
            n_label= ['MCOs off',  'New MCO strengths', '2000x mco val', '5000x mco val']

            fft_bpm_model = [sort_data(fft_tune_model, d) for d in fft_bpm_model]
            fft_bpm_model = [normalize_spectra(fft_bpm_model[0]),normalize_spectra(fft_bpm_model[1])]
            fft_tune_model = np.array(sorted(fft_tune_model))
            
            tx.plot(fft_tune_model, fft_bpm_model[0], label='FFT %s' % (n_label[n]), linewidth='2pt')
            ty.plot(fft_tune_model, fft_bpm_model[1], label='FFT %s' % (n_label[n]))
#             ax.plot(bpm_model_data['X'], label='Model')
#             tx.plot(fft_tune_model, fft_bpm_model[0], label='FFT %s' % (n_label))
#             ay.plot(bpm_model_data['Y'], label='Model')
#             ty.plot(fft_tune_model, fft_bpm_model[1], label='FFT %s' % (n_label))

    # for n in range(len(sdds_model)):
    #     ax.plot(get_init_value(n,'X')*1000,get_init_value(n,'PX'), 'o', ms=15, label='Initial position of %s' % (n))
    #     ax.annotate(
    #         'Job %s' % (n), 
    #         xy = (get_init_value(n,'X')*1000,get_init_value(n,'PX')), xytext = (-20, 20),
    #         textcoords = 'offset points', ha = 'right', va = 'bottom',
    #         bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.25),
    #         arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
    #         )
    #     ay.plot(get_init_value(n,'Y')*1000,get_init_value(n,'PY'), 'o', ms=15, label='Initial position of %s' % (n))
    #     ay.annotate(
    #         'Job %s' % (n), 
    #         xy = (get_init_value(n,'Y')*1000,get_init_value(n,'PY')), xytext = (-20, 20),
    #         textcoords = 'offset points', ha = 'right', va = 'bottom',
    #         bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.25),
    #         arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
    #         )
    #     az.plot(get_init_value(n,'X')*1000,get_init_value(n,'Y')*1000, 'o', ms=15, label='Initial position of %s' % (n))
    #     az.annotate(
    #         'Job %s' % (n), 
    #         xy = (get_init_value(n,'X')*1000,get_init_value(n,'Y')*1000), xytext = (-20, 20),
    #         textcoords = 'offset points', ha = 'right', va = 'bottom',
    #         bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.25),
    #         arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
    #         )

    tx.semilogy()
    ty.semilogy()

    plt.subplots_adjust(left=0.08, right=0.96, top=0.9, bottom=0.1)

    if not output_file:
        plt.legend(numpoints=1, loc='upper left')
        plt.show()
    else:
        plt.gcf().set_size_inches(20, 12)
        plt.savefig(output_file, dpi=400)


 
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


def get_init_value(job_id,key):
    initial_positions = {
                            'X' : [0.00395709 , 0.00337924 , 0.00347445 , 0.0019382  , 0.00310816 , 0.00319779 , 0.00210226 , 0.00272459 , 0.00394366 , 0.00461975 ],
                            'PX': [-9.37e-06  , -1.076e-05 , -1.282e-05 , 2.005e-05  , 4.97e-06   , 1.47e-06   , 1.168e-05  , 1.017e-05  , -1.386e-05 , -2.553e-05 ],
                            'Y' : [0.00300795 , 0.00167912 , 0.00283212 , 0.00461225 , 0.00277203 , 0.00350478 , 0.00161325 , 0.00359441 , 0.00185542 , 0.00433845 ],
                            'PY': [ 5.96e-06  , -2.013e-05 , -1.58e-06  , 8.94e-06   , -3.03e-06  , 4.83e-06   , -1.544e-05 , 8.97e-06   , -1.119e-05 , 1.817e-05  ],
                        }
    result = initial_positions[key][job_id]
    return result


def get_models(job_directory):
    model_list = []
    for i in range(0,3):
        model_list.append(os.path.join(job_directory,'job000%s/SPS%s_77sig.sdds' % (i,i))) #_FRINGE

    return model_list

 
#====================================================================================================    
#               MAIN INVOCATION

#====================================================================================================
if __name__=='__main__':

    sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_49_40_281_0/Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned'
    model_directory   = '/afs/cern.ch/work/f/fcarlier/public/simulations/equal/'#fringe/8sig8sig/'
    # model_directory   = '/afs/cern.ch/work/f/fcarlier/public/simulations/single_part_jobs/'
    # sdds_models       = get_models(model_directory)


    sdds_models         = [ 
                            '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/ref/nomultipoles.sdds',
#                             '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/Re2020/fac1/nos2020Re.sdds',
#                             '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/Re2020/fac100/nos2020Re100.sdds',
#                             '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/Re2020/fac1000/nos2020Re1000.sdds',
                            '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/Re2020/fac2000/nos2020Re2000.sdds',
#                             '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nosextupoles/Re2020/fac5000/nos2020Re5000.sdds'
                            ]


    
    output_file_path  = '/afs/cern.ch/work/f/fcarlier/public/plots/model/spectra/multiple2.pdf'
    output_file_path  = None

    plot_single_BPM_data(bpm_name='BPM.33R3.B2', sdds_model=sdds_models, sdds_experimental=sdds_experimental, output_file=output_file_path, SUSSIX = True  )
