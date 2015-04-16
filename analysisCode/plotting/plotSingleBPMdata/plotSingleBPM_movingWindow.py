#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Single BPM moving window plot."""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc

from analysisCode.linePicker import linePicker

def cut_zero_values(data):
    returnData = []
    for d in data:
        if d != 0.:
            returnData.append(d)
    return returnData

def make_plot(sdds_file_path, bpm=None):
    bpm_data_x, bpm_data_y = (linePicker.read_BPM_data_from_SDDS_file(sdds_file_path, 'X'), linePicker.read_BPM_data_from_SDDS_file(sdds_file_path, 'Y'))
    if bpm:
        bpm_data_x = {bpm:bpm_data_x[bpm]}
        bpm_data_y = {bpm:bpm_data_y[bpm]}

    window_length = 256
    turn_windows = [(i, i+window_length) for i in np.arange(93, 2000-window_length, 10)]

    fig = plt.figure(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    ax_signal = fig.add_subplot(1, 1, 1)
    ax = ax_signal.twinx()

    turn_data = []
    res_amp_data = []
    main_amp_data_x = []
    main_amp_data_y = []
    rel_amp_data = []
    for i in range(len(turn_windows)):
        fft_data_x, fft_freqs_x = linePicker.get_fft(bpm_data_x, turn_window=turn_windows[i])
        fft_data_y, fft_freqs_y = linePicker.get_fft(bpm_data_y, turn_window=turn_windows[i])
    
        # main horizontal tune line
        freq_window = (0.276, 0.282)
        line_data = linePicker.get_line_amplitude_and_phase(fft_data_x, fft_freqs_x, freq_window)
        #main_tune = np.mean(np.array([line_data[bpm][2] for bpm in line_data]))
        main_amp_x = cut_zero_values([np.abs(line_data[bpm][1]) for bpm in line_data])

        # main vertical tune line
        freq_window = (0.29, 0.31)
        line_data = linePicker.get_line_amplitude_and_phase(fft_data_y, fft_freqs_y, freq_window)
        main_amp_y = cut_zero_values([np.abs(line_data[bpm][1]) for bpm in line_data])

        # horizontal (1,2) line
        freq_window = (0.092, 0.097)
        line_data = linePicker.get_line_amplitude_and_phase(fft_data_x, fft_freqs_x, freq_window)
        #res_tune = cut_zero_values([line_data[bpm][2] for bpm in line_data])
        res_amp = cut_zero_values([np.abs(line_data[bpm][1]) for bpm in line_data])

        #bpm_positions = np.array([bpm_data[bpm][0] for bpm in bpm_data])
        turn_data.append(turn_windows[i][0])
        res_amp_data.append(np.mean(res_amp))
        main_amp_data_x.append(np.mean(main_amp_x))
        main_amp_data_y.append(np.mean(main_amp_y))
        #rel_amp_data.append(np.mean(res_amp)/np.mean(main_amp))

    if not bpm:
        ax_signal.plot(np.linspace(0, 2000, 2000), bpm_data_x['BPM.33R2.B2'][1], c='0', alpha=.3)
    else:
        ax_signal.plot(np.linspace(0, 2000, 2000), bpm_data_x[bpm][1], c='0', alpha=.3)

    ax.plot(turn_data, main_amp_data_x/main_amp_data_x[0], label='$Q_x$')#, marker='o')
    ax.plot(turn_data, main_amp_data_y/main_amp_data_y[0], label='$Q_y$')#, marker='o')
    ax.plot(turn_data, res_amp_data/res_amp_data[0], label='$Q_x +2Q_y$')#, marker='o')

    ax_signal.set_ylim(-5, 5)
    ax_signal.set_ylabel('Signal amplitude [mm]')
    
    ax.semilogy()
    ax.set_xlim(0, 1200)
    ax.set_ylim(1e-3, 2)
    #ax.set_title('Relative amplitude of (1,2) resonance')
    ax_signal.set_xlabel('Turn')
    ax.set_ylabel('Relative line amplitude')
    ax.legend(fancybox=False, loc = 'upper center', ncol=3, bbox_to_anchor=(0.5, 1.17))

    labelx = [0,200,400,600,800,1000,""]
    ax_signal.set_xticklabels(labelx)

    fig.subplots_adjust(left=0.1, right=0.85, top=0.87, bottom=0.11)
    # fig.tight_layout()
    plt.show()

if __name__ == '__main__':
    corrected_measurements  = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings'
    sdds_file_path = os.path.join(corrected_measurements , 'Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned')

    #make_plot(sdds_file_path, bpm='BPM.31L1.B2')
    make_plot(sdds_file_path)
    
    
    
    
    
    
    
    
    
    
    
         
            
