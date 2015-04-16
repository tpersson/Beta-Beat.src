"""Single BPM moving window plot."""

import os
import __init__
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc
rc('font', family='serif')
import linePicker
from linePicker import linePicker

def make_plot(sdds_file_path):
    bpm_data = linePicker.read_BPM_data_from_SDDS_file(sdds_file_path, 'X')
    fft_data, fft_freqs = linePicker.get_fft(bpm_data)

    freq_window = (0.276, 0.282)
    line_data = linePicker.get_line_amplitude_and_phase(fft_data, fft_freqs, freq_window)
    #main_tune = np.array([line_data[bpm][2] for bpm in line_data])
    main_amp = np.array([np.abs(line_data[bpm][1]) for bpm in line_data])

    freq_window = (0.092, 0.097)
    line_data = linePicker.get_line_amplitude_and_phase(fft_data, fft_freqs, freq_window)
    res_tune = np.array([line_data[bpm][2] for bpm in line_data])
    res_amp = np.array([np.abs(line_data[bpm][1]) for bpm in line_data])

    fig = plt.figure(figsize=(23, 13))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(1, 1, 1)

    #bpm_positions = np.array([bpm_data[bpm][0] for bpm in bpm_data])
    ax.scatter(res_tune, res_amp/main_amp)
    
    # labels all bpms
    for label, x, y in zip(line_data.keys(), res_tune, res_amp/main_amp):
        ax.annotate(
            label, 
            xy = (x, y), xytext = (-20, 20),
            textcoords = 'offset points', ha = 'right', va = 'bottom',
            bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.25),
            arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0')
        )

    ax.set_title('Relative amplitude of (1,2) resonance')
    ax.set_xlabel('$Q_x$')
    ax.set_ylabel('Relative resonance amplitude')
    ax.grid()

    plt.subplots_adjust(left=0.06, right=0.98, top=0.97, bottom=0.07)
    plt.show()

if __name__ == '__main__':
    # correctedMeasurements  = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings'
    # sdds_file_path = os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned')
    sdds_file_path = '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/single_part_jobs/job0002/SPS2.sdds' #  combined/SPS_p1_j10_n4.sdds'
    make_plot(sdds_file_path)
