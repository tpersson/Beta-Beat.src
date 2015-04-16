#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import numpy as np
from scipy.integrate import simps
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc
rc('font', family='serif')

from outFile.read import read_out_file
from BPMmap.readBPMmapFromFile import BPMmap
# from BPMmapFromTwiss import BPMmap

def sort_data_before_plot(dataX, dataY):
    assert len(dataX) == len(dataY)
    return zip(*sorted(zip(dataX, dataY)))


def cut_zero_values(data):
    assert len(data[0]) == len(data[1])
    newDat = ([], [])
    for x, y in zip(*data):
        if y != 0.:
            newDat[0].append(x)
            newDat[1].append(y)
    return newDat


def cut_outliers(data, sig=1.): # used for IRs, ...
    assert len(data[0]) == len(data[1])
    mean = np.mean(data[1])
    sigma = np.std(data[1])
    newDat = ([], [])
    for x, y in zip(*data):
        if abs(y - mean) < sig*sigma:
            newDat[0].append(x)
            newDat[1].append(y)
    return newDat


def normalize_data(data):
    assert len(data[0]) == len(data[1])
    norm = simps(data[1], data[0])
    print('Norm: %.3f' % norm)
    return (data[0], data[1] / norm)


def abs_data(data):
    return (np.array(data[0]), np.array([abs(d) for d in data[1]]))


def subtract_data_sets(data, data_to_subtract):
    assert len(data) == len(data_to_subtract)
    return np.array(data) - np.array(data_to_subtract)


def divide_data(data, division_factor):
    return (data[0], data[1]/division_factor)


def make_plot(fileNames, columnsX, columnsY, labels, colors, bpm_map_file='/afs/cern.ch/work/f/fcarlier/private/Beta-Beat.src/analysisCode/BPMmap/bpmMap.dat', fft=False, division_factors=[], legend=[]):
    if division_factors: assert len(division_factors) == len(fileNames)
    dataDict = {}
    for fileName in fileNames:
        dataDict[fileName] = read_out_file(fileName)  # read_out_file data

    fig = plt.figure(figsize=(23, 13))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(1, 1, 1)

    fileNamesList = [os.path.basename(fileName) for fileName in fileNames]
    ax.set_title(r'Files: %s' % ', '.join(fileNamesList))

    ax.set_xlabel(', '.join(columnsX))
    ax.set_ylabel(', '.join(columnsY))

    for i in range(len(fileNames)):
        try:
            data = sort_data_before_plot(dataDict[fileNames[i]][columnsX[i]], dataDict[fileNames[i]][columnsY[i]])

            data = cut_zero_values(data)
            data = cut_outliers(data, sig=3)
            try:
                assert len(data[0]) > 0  # are there data points left over after zero cut
            except AssertionError:
                print('No datapoints left over, after cutting zero values for dataset: %s over %s!' % (
                    columnsY[i], columnsX[i]))
                continue

            #data = normalize_data(data)
            data = abs_data(data)
            if division_factors: data = divide_data(data, division_factors[i])

            if fft:
                # first find linx/liny file
                linFile = ''
                for fileName in fileNames:
                    if '_lin' in fileName:
                        linFile = fileName
                try:
                    assert linFile
                except AssertionError:
                    print('Could not find linx/liny file for BPM map... Using build in value for BPM distance!')

                # get BPM map from this file

                realDist = 106.9 / 2.  # fodoLength/2
                if linFile:
                    bpmmap = BPMmap(bpm_map_file)
                    meanDist = bpmmap.getMeanDistanceBetweenBPMs()[0]
                else:
                    meanDist = realDist

                # FFT and plot
                x = 1. / np.fft.fftfreq(len(data[0]), d=meanDist)
                y = abs(np.fft.fft(data[1]))
                #ax.plot(x, y, label='FFT(%s)' % labels[i], color=colors[i])
                ax.scatter(x, y, label='FFT(%s)' % labels[i], color=colors[i], alpha=.5)
                ax.semilogx()
                ax.semilogy()
                for i in [2, 3, 4, 8]:
                    ax.vlines(i * realDist, min(y), max(y), linewidth=.5, color='red')
                    ax.vlines(i * meanDist, min(y), max(y), linewidth=.5, color='black')
            else:
                ax.xaxis.set_major_locator(MultipleLocator(5000))
                ax.xaxis.set_minor_locator(MultipleLocator(500))

                label = legend[i] if legend else fileNames[i][-1] + ': ' + labels[i]
                
                ax.plot(data[0], data[1], label=label, color=colors[i], zorder=0)
                ax.scatter(data[0], data[1], color=colors[i], alpha=.5)
                ax.set_xlim(min(data[0]), max(data[0]))
                #ax.set_ylim(min(data[1]), max(data[1]))
                #ax.semilogy()
                ax.set_ylim(0, 0.12)
                #ax.set_ylim(1e-6, 1e-3)

                ax.set_title('Amplitude of (1,2) resonance for different kicks')
                ax.set_xlabel('S $[m]$')
                ax.set_ylabel('Normalized amplitude')
        except KeyError:
            print([dataDict[f].keys() for f in dataDict.keys()])
            raise

    ax.grid(which='both')

    ax.legend(title='Legend', shadow=True, ncol=3, fancybox=True, loc=0)
    plt.subplots_adjust(left=0.06, right=0.98, top=0.97, bottom=0.06)
    plt.show()
    
    #plt.gcf().set_size_inches(12, 8)
    #plt.savefig('/afs/cern.ch/user/r/rwestenb/Desktop/AMP12.pdf', dpi=400)


def printNonZeroResonances(filePaths):
    for filePath in filePaths:
        print('%s: ' % os.path.basename(filePath))
        data = read_out_file(filePath)
        for col in sorted(data.keys()):
            if 'AMP' in col and np.mean(data[col]) != 0.:
                print(col),
        print


if __name__ == '__main__':
    # modelPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/modelB2inj_correctedoptics/analysis/'
    #measurementPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/measurementsB2inj_diagonal/analysis/manual_data_preparation/Corrected_8sig8sig_Beam2@Turn@2012_06_25@04_00_22_346_0'
    #measurementPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/measurementsB2inj_diagonal/analysis/manual_data_preparation/test'
    # modelPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/Beam2\@Turn\@2012_06_25\@01_07_03_339_0/'
    measurementPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/'
    #measurementPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/modelB2inj_correctedoptics/analysis/simulated_data/'
    correctedMeasurements_test  = '/afs/cern.ch/work/f/fcarlier/private/MD12/'
    correctedMeasurements  = '/afs/cern.ch/work/f/fcarlier/private/MD12/'


    # define your out files which contain the data, the columns you wan to plot in x and y, the label of each data set and the colors (not needed)
    fileNames = [
        #os.path.join(modelPath, 'model.sdds_linx'),
        #os.path.join(measurementPath, 'model.sdds_linx'),
        #os.path.join(measurementPath2, 'model.sdds_linx'),
        #os.path.join(measurementPath, 'results/getsex3000.out'),
        #os.path.join(measurementPath, 'results/ph12_observable.out'),
        #os.path.join(modelPath, 'results/line_data.out'),
        #os.path.join(modelPath, 'results/line_data.out'),
        #os.path.join(measurementPath, 'results/line_data.out'),
        #os.path.join(measurementPath, 'results/line_data.out'),
        #os.path.join(measurementPath, 'results/line_data.out'),
        #os.path.join(measurementPath, 'results/line_data.out'),
        #os.path.join(measurementPath , 'results/f3000_line.out'),
        #os.path.join(measurementPath2, 'results/f3000_line.out'),
        # os.path.join(correctedMeasurements_test , 'result.sdds'),
        # os.path.join(correctedMeasurements , 'result.sdds')
        #os.path.join(measurementPath, 'results/f3000_comparison.out'),
        #os.path.join(measurementPath, 'Corrected_8sig8sig_Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned_linx')
        os.path.join(measurementPath,'Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned')
    ]

    printNonZeroResonances(fileNames)

    columnsX = ['S']*2
    columnsY = ['AMP12']*2
    
    legend = ['test', 'MD12']
    #legend = None

    labels = columnsY
    #colors = ['#ff0000', '#ff3232', '#ff4c4c', '#ff7f7f', '#ff9999', '#ffb2b2', '#ffcccc']#[::-1]
    colors = ['r', 'g']
    #division_factors = [1, 1]
    division_factors = None
    fft = False

    print('\nPlotting data sets:')
    for i in range(len(fileNames)):
        print('   %s over %s (%s)' % (columnsY[i], columnsX[i], os.path.basename(fileNames[i])))

    make_plot(fileNames, columnsX, columnsY, labels, colors, fft=fft, division_factors=division_factors, legend=legend)
