# -*- coding: utf8 -*-

import __init__
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
import RDTs
from RDTs.complexSpectrum import complex_spectra

def sort_data_before_plot(dataX, dataY):
	assert len(dataX) == len(dataY)
	return zip(*sorted(zip(dataX, dataY)))

def plot_single_BPM_spectra(bpm_name, complex_spectra):
	'''Plot spectra in X and Y for the given BPM.
	
	:param string bpm_name: Name of the BPM which spectra should be drawn.
	:param dict complex_spectra: Dictionary which holds the spectra of all BPMs in both planes.
	'''

	''' SET FIGURE 1'''
	fig = plt.figure(figsize=(20, 7))
	fig.patch.set_facecolor('white')
	tx = fig.add_subplot(111)

	fig2 = plt.figure(figsize=(20, 7))
	fig2.patch.set_facecolor('white')
	ty = fig2.add_subplot(111)

	tx.set(xlabel=('X Plane - Frequency [tune units]'), ylabel=('Normalized amplitude'), xlim=([-.5, .5]), ylim=([1e-4, 1]))
	ty.set(xlabel=('Y Plane - Frequency [tune units]'), ylabel=('Normalized amplitude'), xlim=([-.5, .5]), ylim=([1e-4, 1]))

	for plane in ['X', 'Y']:
		# get magnitude and normalize
		magnitude = np.abs(np.array(complex_spectra[bpm_name][plane]))
		max_magnitude = max(magnitude[100:len(magnitude)/2.]) # to not take into account the very high values around 0.0
		magnitude = np.divide(magnitude, max_magnitude)
		# frequencies
		freqs = np.fft.fftfreq(len(complex_spectra[bpm_name][plane]), 1.)
		# get phase
		phase = [np.angle(p) for p in complex_spectra[bpm_name][plane]]

		freqs_mag, magnitude = sort_data_before_plot(freqs, magnitude)
		freqs_phase, phase = sort_data_before_plot(freqs, phase)

		if plane == 'X':
			tx.plot(freqs_mag, magnitude, color='r', label=r'Measurement : $8.2\sigma_{nom,x}$,$6.5\sigma_{nom,y}$')
			tx.semilogy()
		elif plane == 'Y':
			ty.plot(freqs_mag, magnitude, color='r', label=r'Measurement : $8.2\sigma_{nom,x}$,$6.5\sigma_{nom,y}$')
			ty.semilogy()

	tx.legend(shadow=True, fancybox=True, loc='upper left')
	ty.legend(shadow=True, fancybox=True, loc='upper left')
	
	fig.tight_layout()
	fig2.tight_layout()
	plt.show()

def main():
	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_55_09_762_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_49_40_281_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_44_50_218_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_36_40_108_0'

	
	model_twiss_file_path ='/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/madx_codes/ptc_codes/twissel.dat'
	
	
	'''
	calculate_and_output_RDT_comparison(
		#os.path.dirname(model_twiss_file_path),
		model_twiss_file_path,
		sdds_directory
	)
	'''
	
	cs = complex_spectra(sdds_directory, model_twiss_file_path)
# 	plot_single_BPM_spectra('BPM.33R3.B2', cs)
# 	plot_single_BPM_spectra('BPM.12L1.B2', cs)
	plot_single_BPM_spectra('BPM.31L2.B2', cs)

	print('Done!')

if __name__ == '__main__':
	main()
