'''
Created on 10 January 2014

@author: alangner

@version: 0.0.1

templates.template_main_module <description>


'''

import sys
import optparse
import numpy as np
from operator import itemgetter
import re


#===================================================================================================
# parse_args()-function
#===================================================================================================
def parse_args():
    ''' Parses the arguments, checks for valid input and returns tupel '''
    parser = optparse.OptionParser()
#    parser.add_option("-a", "--accel",
#                    help="Which accelerator: LHCB1 LHCB2 LHCB4? SPS RHIC TEVATRON",
#                    metavar="ACCEL", default="LHCB1",dest="accel")
    parser.add_option("-f", "--file",
                    help="Input file in sdds format",
                    metavar="DATAFILE", default="./", dest="datafile")
    parser.add_option("-x", "--tunex",
                    help="TuneX from DRIVE",
                    metavar="TUNEX", default=0, dest="tunex")
    parser.add_option("-y", "--tuney",
                    help="TuneY from DRIVE",
                    metavar="TUNEY", default=0, dest="tuney")
    
    (options, args) = parser.parse_args()

    # Check arguments
#    if options.accel not in ("LHCB1", "LHCB2", "LHCB4", "SPS", "RHIC", "TEVATRON"):
#        raise ValueError("Invalid accelerator: "+options.accel)

    return options, args


#===================================================================================================
# main()-function
#===================================================================================================
def main(datafile, tunex, tuney):
    '''
    :Return: int
        0 if execution was successful otherwise !=0
    '''
    horizontal_data, vertical_data, horizontal_bpm_data, vertical_bpm_data, \
    horizontal_positions, vertical_positions, horizontal_names, vertical_names = read_input_file(datafile)

    #import matplotlib.pyplot as plt
    #plt.plot(freq, np.abs(a.real))
    #plt.yscale('log')
    #plt.show()
    #TODO: temporarily tunes as from drive should be read automatically or computed here
    tune_x = float(tunex)
    tune_y = float(tuney)
    if tune_x == 0:
        tune_x = get_tune(horizontal_data)
    if tune_y == 0:
        tune_y = get_tune(vertical_data)

    horizontal_phases, horizontal_amplitudes = harmonic_analysis(horizontal_bpm_data, horizontal_names, tune_x)
    vertical_phases, vertical_amplitudes = harmonic_analysis(vertical_bpm_data, vertical_names, tune_y)

    horizontal_co_phases, horizontal_co_amplitudes = harmonic_analysis(horizontal_bpm_data, horizontal_names, tune_y, 0)
    vertical_co_phases, vertical_co_amplitudes = harmonic_analysis(vertical_bpm_data, vertical_names, tune_x, 0)

    write_data(datafile, [horizontal_names, horizontal_positions, horizontal_phases, horizontal_amplitudes, tune_x, horizontal_co_phases, horizontal_co_amplitudes], [vertical_names, vertical_positions, vertical_phases, vertical_amplitudes, tune_y, vertical_co_phases, vertical_co_amplitudes], tune_x, tune_y)
    return 0


#===================================================================================================
# helper-functions
#===================================================================================================
def read_input_file(datafile):
    '''
    Does x...
    :Parameters:
        'values_list': list of float
            <description>
        'names_dict': dict: string --> float
            <description>
    :Return: float
        <description>
    '''
    horizontal_data = []
    vertical_data = []
    horizontal_bpm_data = {}
    vertical_bpm_data = {}
    horizontal_positions = {}
    vertical_positions = {}
    horizontal_names = []
    vertical_names = []
    with open(datafile) as infile:
#TODO: ---------------------------------------------------------------------------v
        for line in infile:
            if line.split(' ')[0] == '0':
                horizontal_data.extend(float(x) for x in re.split('\s+', line)[3:1000])
                horizontal_names.append(re.split('\s+', line)[1])
                horizontal_bpm_data[str(re.split('\s+', line)[1])] = [float(x) for x in re.split('\s+', line)[3:1000]]
                horizontal_positions[str(re.split('\s+', line)[1])] = float(re.split('\s+', line)[2])
            elif line.split(' ')[0] == '1':
                vertical_data.extend(float(x)  for x in re.split('\s+', line)[3:1000])
                vertical_names.append(re.split('\s+', line)[1])
                vertical_bpm_data[str(re.split('\s+', line)[1])] = [float(x) for x in re.split('\s+', line)[3:1000]]
                vertical_positions[str(re.split('\s+', line)[1])] = float(re.split('\s+', line)[2])
    return horizontal_data, vertical_data, horizontal_bpm_data, vertical_bpm_data, horizontal_positions, vertical_positions, horizontal_names, vertical_names


def get_tune(tbt_data):
    '''
    Does x...
    :Parameters:
        'values_list': list of float
            <description>
        'names_dict': dict: string --> float
            <description>
    :Return: float
        <description>
    '''
    amp = np.fft.fft(tbt_data)
    t = np.arange(len(amp))
    freq = np.fft.fftfreq(t.shape[-1])
    temp = zip(freq, amp)
    tune = max(temp, key=itemgetter(1))[0]
    return np.abs(tune)


def harmonic_analysis(bpm_data, bpm_names, tune, order_phases=1):
    '''
    Does x...
    :Parameters:
        'values_list': list of float
            <description>
        'names_dict': dict: string --> float
            <description>
    :Return: float
        <description>
    '''
    phases = {}
    amplitudes = {}
    last_name = 0
    for name in bpm_names:
        C = 0
        S = 0
        for i in range(len(bpm_data[name])):
            C = C + bpm_data[name][i] * np.cos(2 * np.pi * tune * i)
            S = S + bpm_data[name][i] * np.sin(2 * np.pi * tune * i)
        phase_temp = - np.arctan(S / C) / (2 * np.pi)
        if last_name != 0 and order_phases == 1:
            if phase_temp < phases[last_name]:
                phase_temp = phase_temp + 0.5
            if phase_temp > phases[last_name] + 0.5:
                phase_temp = phase_temp - 0.5
            if (phase_temp - phases[last_name])%1 > 0.4:
                phase_temp = phase_temp + 0.5
        if phase_temp >= 0.5:
            phase_temp = phase_temp - 1
        phases[name] = phase_temp
        amplitudes[name] = 2 * np.sqrt(C**2 + S**2) / len(bpm_data[name])
        last_name = name
    return phases, amplitudes


def write_data(input_file_name, horizontal_data, vertical_data, tune_x, tune_y):
    '''
    Does x...
    :Parameters:
        'values_list': list of float
            <description>
        'names_dict': dict: string --> float
            <description>
    :Return: float
        <description>
    '''
    with open("".join([input_file_name, "_linx"]), 'w') as outfile:
        outfile.write("@ Q1 %le "+str(tune_x)+"\n")
        outfile.write("@ Q1RMS %le 0 \n")
        outfile.write("* NAME S    BINDEX SLABEL TUNEX MUX  AMPX PK2PK AMP01 PHASE01\n")
        outfile.write("$ %s  %le %le   %le   %le  %le %le %le  %le %le\n")
        for i in range(len(horizontal_data[0])):
            outfile.write("".join(['"',str(horizontal_data[0][i]),'" ',str(horizontal_data[1][horizontal_data[0][i]]),' ',str(i),' 1 ',str(horizontal_data[4]),' ',str(horizontal_data[2][horizontal_data[0][i]]),' ',str(horizontal_data[3][horizontal_data[0][i]]),' 1 ',str(horizontal_data[6][horizontal_data[0][i]]),' ',str(horizontal_data[5][horizontal_data[0][i]]),'\n']))
    with open("".join([input_file_name, "_liny"]), 'w') as outfile:
        outfile.write("@ Q2 %le "+str(tune_y)+" \n")
        outfile.write("@ Q2RMS %le 0 \n")
        outfile.write("* NAME S    BINDEX SLABEL TUNEY MUY  AMPY PK2PK AMP10 PHASE10\n")
        outfile.write("$ %s  %le %le   %le   %le  %le %le %le %le %le\n")
        for i in range(len(vertical_data[0])):
            outfile.write("".join(['"',str(vertical_data[0][i]),'" ',str(vertical_data[1][vertical_data[0][i]]),' ',str(550+i),' ',str(1),' ',str(vertical_data[4]),' ',str(vertical_data[2][vertical_data[0][i]]),' ',str(vertical_data[3][vertical_data[0][i]]),' 1 ',str(vertical_data[6][vertical_data[0][i]]),' ',str(vertical_data[5][vertical_data[0][i]]),'\n']))

    return 0


#===================================================================================================
# main invocation
#===================================================================================================
if __name__ == "__main__":
    (options, args) = parse_args()

    return_value = main(datafile=options.datafile, tunex=options.tunex, tuney=options.tuney)

    sys.exit(return_value)
