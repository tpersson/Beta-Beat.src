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

    (options, args) = parser.parse_args()

    # Check arguments
#    if options.accel not in ("LHCB1", "LHCB2", "LHCB4", "SPS", "RHIC", "TEVATRON"):
#        raise ValueError("Invalid accelerator: "+options.accel)

    return options, args


#===================================================================================================
# main()-function
#===================================================================================================
def main(datafile):
    '''
    :Return: int
        0 if execution was successful otherwise !=0
    '''
    horizontal_data, vertical_data = read_input_file(datafile)

    tune_x = get_tune(horizontal_data)
    tune_y = get_tune(vertical_data)
    print tune_x, tune_y
    #import matplotlib.pyplot as plt
    #plt.plot(freq, np.abs(a.real))
    #plt.yscale('log')
    #plt.show()
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
    with open(datafile) as infile:
        for line in infile:
            if line.split(' ')[0] == '0':
                horizontal_data.extend(float(x) for x in re.split('\s+', line)[3:1000])
            elif line.split(' ')[0] == '1':
                vertical_data.extend(float(x)  for x in re.split('\s+', line)[3:1000])
    return horizontal_data, vertical_data


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
    tune = max(temp, key = itemgetter(1))[0]
    return np.abs(tune)


#===================================================================================================
# main invocation
#===================================================================================================
if __name__ == "__main__":
    (options, args) = parse_args()

    return_value = main(datafile = options.datafile)

    sys.exit(return_value)
