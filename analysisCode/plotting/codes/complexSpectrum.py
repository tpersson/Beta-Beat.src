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

def plot_single_BPM_spectra(bpm_name, complex_spectra, complex_spectra2):
	'''Plot spectra in X and Y for the given BPM.
	
	:param string bpm_name: Name of the BPM which spectra should be drawn.
	:param dict complex_spectra: Dictionary which holds the spectra of all BPMs in both planes.
	'''

	''' SET FIGURE 1'''
	fig = plt.figure(figsize=(10, 7))  ## for note: (20,7)  ## for IPAC :
	fig.patch.set_facecolor('white')
	tx = fig.add_subplot(111)
	fig2 = plt.figure(figsize=(10, 7))
	fig2.patch.set_facecolor('white')
	ty = fig2.add_subplot(111)

	tx.set(xlabel=('Frequency [tune units]'), ylabel=('Normalized amplitude'), xlim=([-.5, .5]), ylim=([1e-4, 1.2]))
	# tx.text()



	ty.set(xlabel=('Y Plane - Frequency [tune units]'), ylabel=('Normalized amplitude'), xlim=([-.5, .5]), ylim=([1e-4, 1.2]))

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

		magnitude2 = np.abs(np.array(complex_spectra2[bpm_name][plane]))
		max_magnitude2 = max(magnitude2[100:len(magnitude2)/2.]) # to not take into account the very high values around 0.0
		magnitude2 = np.divide(magnitude2, max_magnitude2)

		freqs2 = np.fft.fftfreq(len(complex_spectra2[bpm_name][plane]), 1.)
		phase2 = [np.angle(p) for p in complex_spectra2[bpm_name][plane]]
		freqs_mag2, magnitude2 = sort_data_before_plot(freqs2, magnitude2)
		freqs_phase2, phase2 = sort_data_before_plot(freqs2, phase2)

		if plane == 'X':
			tx.plot(freqs_mag, magnitude, color='r', label='Measurement')
			tx.plot(freqs_mag2, magnitude2, color='b', label='5k tracking')
			tx.semilogy()
		elif plane == 'Y':
			ty.plot(freqs_mag, magnitude, color='r', label='Complex Spectrum')
			ty.plot(freqs_mag2, magnitude2, color='b', label='Complex Spectrum')
			ty.semilogy()

	tx.set_ylim([1e-4,2.5])
	tx.text(.06, .12, '(-1,-2)', fontsize=18)
	tx.text(.25, 1.2, '(1,0)', fontsize=18)
	tx.text(.3, .3, '(0,1)', fontsize=18)
	tx.text(-.30, .11, '(-1,0)', fontsize=18)
	tx.text(-.37, .06, '(0,-1)', fontsize=18)
	tx.text(.35, .05, '(0,-2)', fontsize=18)
	tx.text(.39, .02, '(-1,-1)', fontsize=18)

	tx.legend(shadow=False, fancybox=False, loc='upper left')

	fig.tight_layout()
	fig2.tight_layout()
	plt.show()

def main():
	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_55_09_762_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_49_40_281_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_44_50_218_0'
# 	sdds_directory = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@03_36_40_108_0'

	
# 	model_twiss_file_path ='/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/madx_codes/from_Ewen/twiss_nonlinear.dat'#ptc_codes/twissel.dat'
	model_twiss_file_path ='/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/madx_codes/ptc_codes/twissel.dat'
	
	
	'''
	calculate_and_output_RDT_comparison(
		#os.path.dirname(model_twiss_file_path),
		model_twiss_file_path,
		sdds_directory
	)
	'''

# 	sdds_directory2 = '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/nonlinear_8skick/forcomplex/'
	sdds_directory2 = '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newdet/2500/'
	
	cs = complex_spectra(sdds_directory, model_twiss_file_path)
	cs2 = complex_spectra(sdds_directory2, model_twiss_file_path)
	# plot_single_BPM_spectra('BPM.33R3.B2', cs)
	plot_single_BPM_spectra('BPM.33R3.B2', cs, cs2)
	#plot_single_BPM_spectra('BPM.31L2.B2', cs)

	print('Done!')

if __name__ == '__main__':
	main()
