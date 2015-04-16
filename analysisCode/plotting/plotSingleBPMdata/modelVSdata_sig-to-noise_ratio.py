import os
import numpy as np

def read_BPM_data_from_SDDS_file(bpm_name, sdds_file_path, normalization_factor=1, start_turn=None, end_turn=None):
	bpm_data = {}

	assert os.path.exists(sdds_file_path)
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

def read_BPM_spectra_from_BPM_files(bpm_name, sdds_file_path):
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
	
	for plane in bpm_data:
		bpm_data[plane] = sort_data(*bpm_data[plane])

	return bpm_data

def fft_BPM_data(BPMdata):
	return abs(np.fft.fft(BPMdata))

def normalize_spectra(data):
	m = max(data) 
	return np.divide(data, m)

def plot_single_BPM_data(bpm_name, sdds_measurement, sdds_simulation, output_file=None):
	bpm_measurement_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_measurement, start_turn=93, end_turn=1093)
	bpm_simulation_data = read_BPM_data_from_SDDS_file(bpm_name, sdds_simulation, start_turn=0)
		
	#sussix_model_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_model)
	#sussix_experimental_data = read_BPM_spectra_from_BPM_files(bpm_name, sdds_experimental)
	
	fig.suptitle(bpm_name)
	ax.set_xlabel('$N$ [1]')
	tx.set_xlabel('$Q_x$ [1/turn]')
	ay.set_xlabel('$N$ [1]')
	ty.set_xlabel('$Q_y$ [1/turn]')
	ax.set_ylabel('X [mm]')
	tx.set_ylabel('Amp [a.u.]')
	ay.set_ylabel('Y [mm]')
	ty.set_ylabel('Amp [a.u.]')
	
	'''
	# rescale model data by factor 1000 (m -> mm)
	model_rescale_factor = 1000.
	bpm_model_data['X'] = [d*model_rescale_factor for d in bpm_model_data['X']]
	bpm_model_data['Y'] = [d*model_rescale_factor for d in bpm_model_data['Y']]
	sussix_model_data['X'][1] = [d*model_rescale_factor for d in sussix_model_data['X'][1]]
	sussix_model_data['Y'][1] = [d*model_rescale_factor for d in sussix_model_data['Y'][1]]
	'''
	
	# setup data sets
	fft_bpm_measurement = [fft_BPM_data(bpm_measurement_data['X']), fft_BPM_data(bpm_measurement_data['Y'])]
	fft_bpm_simulation = [fft_BPM_data(bpm_simulation_data['X']), fft_BPM_data(bpm_simulation_data['Y'])]
	fft_tune_measurement = np.fft.fftfreq(len(bpm_measurement_data['X']), d=1.)
	fft_tune_simulation = np.fft.fftfreq(len(bpm_simulation_data['X']), d=1.)

	# sort data sets
	fft_bpm_measurement = [sort_data(fft_tune_measurement, d) for d in fft_bpm_measurement]
	fft_bpm_simulation = [sort_data(fft_tune_simulation, d) for d in fft_bpm_simulation]
	fft_tune_measurement = np.array(sorted(fft_tune_measurement))
	fft_tune_simulation = np.array(sorted(fft_tune_simulation))

	#sussix_bpm_model = {'X':sussix_model_data['X'][1], 'Y':sussix_model_data['Y'][1]}
	#sussix_bpm_experimental = {'X':sussix_experimental_data['X'][1], 'Y':sussix_experimental_data['Y'][1]}
	#sussix_tune_model = {'X':sussix_model_data['X'][0], 'Y':sussix_model_data['Y'][0]}
	#sussix_tune_experimental = {'X':sussix_experimental_data['X'][0], 'Y':sussix_experimental_data['Y'][0]}
	
	# normalize spectra to maximum
	#fft_bpm_model['X'] = normalize_spectra(fft_bpm_model['X'])
	#fft_bpm_model['Y'] = normalize_spectra(fft_bpm_model['Y'])
	#fft_bpm_experimental['X'] = normalize_spectra(fft_bpm_experimental['X'])
	#fft_bpm_experimental['Y'] = normalize_spectra(fft_bpm_experimental['Y'])
	
	#sussix_bpm_model['X'] = normalize_spectra(sussix_bpm_model['X'])
	#sussix_bpm_model['Y'] = normalize_spectra(sussix_bpm_model['Y'])
	#sussix_bpm_experimental['X'] = normalize_spectra(sussix_bpm_experimental['X'])
	#sussix_bpm_experimental['Y'] = normalize_spectra(sussix_bpm_experimental['Y'])
	
	# actual plotting
	ax.plot(bpm_measurement_data['X'], label='Measurement', alpha=0.4)
	ax.plot(bpm_simulation_data['X'], label='Multi particle simulation', alpha=0.4)
	tx.plot(fft_tune_measurement, fft_bpm_measurement[0], label='FFT Measurement', color='black')
	tx.plot(fft_tune_simulation, fft_bpm_simulation[0], label='FFT Simulation', color='r')
	ay.plot(bpm_measurement_data['Y'], label='Measurement', alpha=0.4)
	ay.plot(bpm_simulation_data['Y'], label='Multi particle simulation', alpha=0.4)
	ty.plot(fft_tune_measurement, fft_bpm_measurement[1], label='FFT Measurement', color='black')
	ty.plot(fft_tune_simulation, fft_bpm_simulation[1], label='FFT Simulation', color='r')
	
	ax.set_xlim(0, len(bpm_measurement_data['X']))
	tx.set_xlim(0., .5)
	ay.set_xlim(0, len(bpm_measurement_data['Y']))
	ty.set_xlim(0., .5)
	
	ax.grid(which='both')
	tx.grid(which='both', linewidth=.1, linestyle='-', color='grey')
	ay.grid(which='both')
	ty.grid(which='both', linewidth=.1, linestyle='-', color='grey')
	
	tx.xaxis.set_major_locator(MultipleLocator(.1))
	ty.xaxis.set_major_locator(MultipleLocator(.1))
	
	ax.legend(title='Legend', shadow=True, ncol=2, fancybox=True)
	tx.legend(title='X Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
	ay.legend(title='Legend', shadow=True, ncol=2, fancybox=True)
	ty.legend(title='Y Plane', shadow=True, fancybox=True, loc=1, prop={'size':10})
	
	tx.semilogy()
	ty.semilogy()
	
	#plt.subplots_adjust(left=0.04, right=0.98, top=0.95, bottom=0.05)
	plt.subplots_adjust(left=0.08, right=0.96, top=0.9, bottom=0.1)
	
	if not output_file:
		plt.show()
	else:
		plt.gcf().set_size_inches(10, 6)
		plt.savefig(output_file, dpi=200)

def do_plot(sdds_simulation, output_file_path=None, sdds_measurement='/afs/cern.ch/work/f/fcarlier/public/MD12/correctedSettings/Beam2@Turn@2012_06_25@04_00_22_346_0/Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.nl_corrected', bpms_to_plot=['BPM.33R3.B2']):
	for bpm in bpms_to_plot:
		if output_file_path: output_file = output_file_path + '_' + bpm + '.pdf'
		else: output_file = None
		plot_single_BPM_data(bpm, sdds_measurement, sdds_simulation, output_file=output_file)

def initialize_plots():
        import matplotlib.pyplot as plt
        from matplotlib.ticker import MultipleLocator

        fig = plt.figure(figsize=(23, 13))
        fig.patch.set_facecolor('white')
        ax = fig.add_subplot(2,2,1)
        tx = fig.add_subplot(2,2,2)
        ay = fig.add_subplot(2,2,3)
        ty = fig.add_subplot(2,2,4)

	return (fig, [ax,tx,ay,ty])
	

if __name__=='__main__':
	sdds_simulation = '/afs/cern.ch/work/f/fcarlier/public/multiParticleTest/results_combined.sdds'
	#sdds_simulation = '/afs/cern.ch/work/f/fcarlier/public/multiParticleTest/analysis/results_combined.cleaned.sdds'
	output_file_path = '/afs/cern.ch/user/r/rwestenb/Desktop/spectrum'
	output_file_path = None

	figure, plots = initialize_plots()
	do_plot(sdds_simulation, output_file_path=output_file_path, bpms_to_plot=['BPM.30L1.B2']) #['BPM.33R3.B2', 'BPM.15R7.B2', 'BPM.24L5.B2'])
