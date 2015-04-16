#!/usr/bin/env python
# -*- coding: utf8 -*-

"""Mean AMP12 vs kick sig plot."""

import os
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc

from analysisCode.outFile.read import read_out_file


def cut_zero_values(data):
    returnData = []
    for i in range(len(data)):
        if data[i] != 0.:
            returnData.append(data[i])
    return returnData


def make_plot(fileNames, kicks, columnsY, jxjy=None):
    dataDict = {}
    for fileName in fileNames:
        dataDict[fileName] = read_out_file(fileName)  # read_out_file data

    fig = plt.figure(figsize=(10, 7))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(1, 1, 1)

    # x and ydata for fitting
    xdata = np.zeros(len(fileNames))
    ydata = np.zeros(len(xdata))
    yerr = np.zeros(len(xdata))

    for i in range(len(fileNames))[::-1]:
        try:
            data = dataDict[fileNames[i]][columnsY[i]]
            data = cut_zero_values(data)
            #data = cut_outliers(data, sig=1.)
            amp_mean = np.mean(data)
            amp_sig = np.std(data)
            if not jxjy: # assume we have kicks (sig_x, err_sig_x, sig_y, err_sig_y)
                kick = np.sqrt(kicks[i][0]**2 + kicks[i][2])
                err_kick = np.sqrt((kicks[i][0]**2*kicks[i][1]**2+kicks[i][2]**2*kicks[i][3]**2)/kick**2)
            else: # assume we have jxjy (sqrt(Jx)*Jy, err)
                kick = jxjy[i][0]
                err_kick = jxjy[i][1]

            label = '(%.1f, %.1f)' % (kicks[i][0], kicks[i][2])

            xdata[i] = kick
            #xdata[i][1] = err_kick
            ydata[i] = amp_mean
            yerr[i] = amp_sig

            ax.errorbar(kick, amp_mean, xerr=err_kick, yerr=amp_sig, zorder=0, marker='o')

            ax.yaxis.set_major_locator(MultipleLocator(.02))
            ax.yaxis.set_minor_locator(MultipleLocator(.01))
            ax.set_ylim(0, .09)
            if not jxjy:
                ax.set_xlim(4, 10)
                # ax.xaxis.set_major_locator(MultipleLocator(1))
                # ax.xaxis.set_minor_locator(MultipleLocator(.5))
            else:
                ax.set_xlim(0, .3)
                # ax.xaxis.set_major_locator(MultipleLocator(.05))
                # ax.xaxis.set_minor_locator(MultipleLocator(.01))
 
            #ax.set_title('Relative amplitude of (1,2) resonance for different kicks')
            ax.set_ylabel(r'Relative resonance amplitude')
            if not jxjy: ax.set_xlabel(r'Nominal kick amplitude $\sqrt{\sigma_x^2 + \sigma_y^2}$')
            else: ax.set_xlabel(r'Kick amplitude  $2J_y\sqrt{2J_x}$')
        except KeyError:
            print([dataDict[f].keys() for f in dataDict.keys()])
            raise

    # fitting
    fitfunc = lambda x, a: a * x
    fit = curve_fit(fitfunc, xdata[2:], ydata[2:], sigma=yerr[2:]/ydata[2:])
    print 'Fit parameter: %.5f +/- %.5f (%.3f%%)' % (fit[0], fit[1], fit[1]/fit[0]*100)
    xfit = np.array([0,1])
    ax.plot(xfit, xfit*fit[0], c='0', label='Least square linear fit')
    ax.annotate('Fit parameter: $ax=y$\n$a=%.5f\pm%.5f$' % (fit[0], fit[1]), xy=(.006, .075), ha='left', va='bottom', bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=1), fontsize=18)

    # ax.grid(which='both')
    # ax.legend(shadow=True, ncol=1, fancybox=True, loc=2)
    # plt.subplots_adjust(left=0.09, right=0.97, top=0.99, bottom=0.11)
    plt.tight_layout()

    #plt.show()

    plt.gcf().set_size_inches(8, 5)
#     plt.savefig('/afs/cern.ch/user/r/rwestenb/Desktop/AMP12_for_different_kicks.pdf', dpi=400)
    plt.show()
    
def printNonZeroResonances(filePaths):
    for filePath in filePaths:
        print('%s: ' % os.path.basename(filePath))
        data = read_out_file(filePath)
        for col in sorted(data.keys()):
            if 'AMP' in col and np.mean(data[col]) != 0.:
                print(col),
        print


def get_kick_sqrtJx_Jy_from_getkick(measurement_path):
    content = read_out_file(os.path.join(measurement_path, 'getllm/getkick.out'))
    return (content['sqrt2JX'][0]*content['2JY'][0], np.sqrt((content['2JY'][0]*content['sqrt2JXSTD'][0])**2 + (content['sqrt2JX'][0]*content['2JYSTD'][0])**2))

if __name__ == '__main__':
    modelPath = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/modelB2inj_correctedoptics/analysis/simulated_data/'
    correctedMeasurements  = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings'

    # define your out files which contain the data, the columns you wan to plot in x and y, the label of each data set and the colors (not needed)
    fileNames = [
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_25_13_860_0/Beam2@Turn@2012_06_25@03_25_13_860_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_30_55_508_0/Beam2@Turn@2012_06_25@03_30_55_508_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_36_40_108_0/Beam2@Turn@2012_06_25@03_36_40_108_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_44_50_218_0/Beam2@Turn@2012_06_25@03_44_50_218_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_49_40_281_0/Beam2@Turn@2012_06_25@03_49_40_281_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@03_55_09_762_0/Beam2@Turn@2012_06_25@03_55_09_762_0.sdds.new.nl_corrected.cleaned_linx'),
        os.path.join(correctedMeasurements , 'Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned_linx')
    ]

    #printNonZeroResonances(fileNames)

    columnsY = ['AMP12']*7

    jxjy = [ get_kick_sqrtJx_Jy_from_getkick(os.path.dirname(f)) for f in fileNames ] # comment for plots over |sig| else you will get sqrt(2Jx)*2Jy

    kicks = [ # nominal (sig_x, err sig_x, sig_y, err sig_y)
        (5.5, 0.5, 5.1, 0.3),
        (6.2, 0.2, 4.9, 0.3),
        (6.9, 0.3, 5.4, 0.5),
        (7.2, 0.3, 5.7, 0.2),
        (7.6, 0.3, 6.1, 0.3),
        (7.8, 0.3, 6.2, 0.3),
        (8.2, 0.3, 6.5, 0.3)
    ]

    make_plot(fileNames, kicks, columnsY, jxjy=jxjy)
    
    
    
    
    
    
    
    

