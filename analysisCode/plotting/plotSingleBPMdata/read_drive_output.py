import os
import numpy as np

''' Read BPM Drive output '''
def read_drive_output(sdds_file_path,bpm_name):
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


''' Sort obtained dictionary: bpm_data in order of frequency '''
def sort_bpm_data(bpm_data):
    sorted_data = {'X':[[],[]], 'Y':[[],[]]}
    for plane in bpm_data:
        frequency = bpm_data[plane][0]
        amplitude = bpm_data[plane][1]
        sorted_data[plane][0],sorted_data[plane][1] = zip(*sorted(zip(frequency, amplitude)))
    return sorted_data

bpm_data = {'X':[[1,3,2,5,4,7,6],['q','e','w','t','r','u','y']], 'Y':[[1,3,2,5,4,7,6], ['q','w','e','r','t','y','u']] }
sort_result = {}
sort_result = sort_bpm_data(bpm_data)
print sort_result['X']