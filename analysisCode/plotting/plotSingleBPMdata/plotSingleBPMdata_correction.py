import numpy as np

def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
	bpm_data = {}

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

def fft_BPM_data(BPMdata):
	return abs(np.fft.fft(BPMdata))

def normalize_spectra(data):
	return np.divide(data, max(data))
	#return np.divide(data, 330)

def plot_single_BPM_data(bpm_name, sdds_experimental, sdds_old, sdds_new, output_file=None):
	import matplotlib.pyplot as plt
	from matplotlib.ticker import MultipleLocator

	turns = (93, 1200)
	bpm_experimental = read_BPM_data_from_SDDS_file(bpm_name, sdds_experimental, start_turn=turns[0], end_turn=turns[1])
	bpm_old = read_BPM_data_from_SDDS_file(bpm_name, sdds_old, start_turn=turns[0], end_turn=turns[1])
	bpm_new = read_BPM_data_from_SDDS_file(bpm_name, sdds_new, start_turn=turns[0], end_turn=turns[1])
	
	fig = plt.figure(figsize=(8, 5))
	fig.patch.set_facecolor('white')
	
	#ax = fig.add_subplot(2,1,1)
	#tx = fig.add_subplot(2,1,2)
	tx = fig.add_subplot(2,1,1)
	ty = fig.add_subplot(2,1,2)
	
	#fig.suptitle(bpm_name + ': Measurement 04:00:22')
	#tx.set_xlabel('$Q_x$ [1/turn]')
	tx.set_ylabel('Norm. amplitude [a.u.]')
	ty.set_xlabel('$Q_{x/y}$ [1/turn]')
	ty.set_ylabel('Norm. amplitude [a.u.]')

	# setup data sets
	fft_bpm_experimental = [fft_BPM_data(bpm_experimental['X']), fft_BPM_data(bpm_experimental['Y'])]
	fft_bpm_old = [fft_BPM_data(bpm_old['X']), fft_BPM_data(bpm_old['Y'])]
	fft_bpm_new = [fft_BPM_data(bpm_new['X']), fft_BPM_data(bpm_new['Y'])]
	fft_freq = np.fft.fftfreq(len(bpm_experimental['X']), d=1.)
	
	# sort data sets
	fft_bpm_experimental = [sort_data(fft_freq, d) for d in fft_bpm_experimental]
	fft_bpm_old = [sort_data(fft_freq, d) for d in fft_bpm_old]
	fft_bpm_new = [sort_data(fft_freq, d) for d in fft_bpm_new]
	fft_freq = np.array(sorted(fft_freq))

	# normalize spectra to maximum
	fft_bpm_experimental = [normalize_spectra(fft_bpm_experimental[0]), normalize_spectra(fft_bpm_experimental[1])]
	fft_bpm_old = [normalize_spectra(fft_bpm_old[0]), normalize_spectra(fft_bpm_old[1])]
	fft_bpm_new = [normalize_spectra(fft_bpm_new[0]), normalize_spectra(fft_bpm_new[1])]
	
	# actual plotting
	#ax.plot(bpm_experimental['X'])
	#ax.plot(bpm_old['X'])
	#ax.plot(bpm_new['X'])
	tx.plot(fft_freq, fft_bpm_experimental[0], label='FFT Experimental', color='black')
	tx.plot(fft_freq, fft_bpm_old[0],          label='FFT Old correction', color='r')
	tx.plot(fft_freq, fft_bpm_new[0],          label='FFT New correction', color='g')
	ty.plot(fft_freq, fft_bpm_experimental[1], label='FFT Experimental', color='black')
	ty.plot(fft_freq, fft_bpm_old[1],          label='FFT Old correction', color='r')
	ty.plot(fft_freq, fft_bpm_new[1],          label='FFT New correction', color='g')
	
	tx.set_xlim(0., .5)
	tx.set_ylim(5e-4, 1)
	ty.set_xlim(0., .5)
	ty.set_ylim(5e-4, 1)
	
	tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
	ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')
	
	tx.xaxis.set_major_locator(MultipleLocator(.1))
	ty.xaxis.set_major_locator(MultipleLocator(.1))
	
	tx.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
	ty.legend(title='Y Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
	
	tx.semilogy()
	ty.semilogy()
	
	plt.subplots_adjust(left=0.09, right=0.98, top=0.97, bottom=0.1)
	
	if not output_file:
		plt.show()
	else:
		plt.gcf().set_size_inches(8, 5)
		plt.savefig('%s_%s_%d-%d.pdf' % (output_file, bpm_name, turns[0], turns[1]), dpi=400)

def do_plot(sdds_experimental, sdds_old, sdds_new, bpms_to_plot, output_file_path=None):
	for bpm in bpms_to_plot:
		plot_single_BPM_data(bpm, sdds_experimental, sdds_old, sdds_new, output_file=output_file_path)

if __name__=='__main__':
	sdds_experimental = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new'
	sdds_old          = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected'
	sdds_new          = '/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected.cleaned'
	#sdds_old          = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/modelB2inj_correctedoptics/analysis/simulated_data/model.sdds'
	#sdds_new          = '/afs/cern.ch/user/r/rwestenb/Desktop/working_directory/model.sdds'
	output_file_path  = '/afs/cern.ch/work/f/fcarlier/public/plots/spectrum'
	output_file_path = None

	do_plot(sdds_experimental, sdds_old, sdds_new, ['BPM.33R3.B2'], output_file_path=output_file_path)
