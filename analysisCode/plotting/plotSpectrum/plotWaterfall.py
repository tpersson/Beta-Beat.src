# only if you run without X
import matplotlib as mpl
mpl.use('Agg')
#

import matplotlib.pyplot as plt
from matplotlib import ticker, rc
rc('font', family='serif')
import numpy as np
from scipy.interpolate import griddata
import os
from BPMmap.readBPMmapFromFile import BPMmap
from outFile.read import read_out_file

def normalize_spectrum(data, data_max=None):
	if data_max:
		return data/data_max
	else:
		return data/max(data)

def cut_anomalies(data, sig=2.):
	data_mean = np.mean(data)
	data_std = np.std(data)
	
	for i in range(len(data)):
		if data[i] > data_mean+sig*data_std:
			data[i] = data_mean+sig*data_std
		elif data[i] < data_mean-sig*data_std:
			data[i] = data_mean-sig*data_std

	return data

def readin_BPM_data(bpm_directory, bpm_map):
	bpm_data = {} # bpm_data = {'BPM.NAME':{'pos':1234.5678, 'data':{'x':[[],[]], 'y':[[], []]}}}
	for bpm_file in os.listdir(bpm_directory):
		if 'BPM' in bpm_file and bpm_file.endswith('.x') or bpm_file.endswith('.y'): # should be BPM file
			bpm_plane = bpm_file.split('.')[-1]
			bpm_name = '.'.join(bpm_file.split('.')[:-1])
			temp_data = read_out_file(os.path.join(bpm_directory, bpm_file))
			if bpm_name not in bpm_data:
				bpm_data[bpm_name] = {'pos':bpm_map.getSofBPM(bpm_name), 'data':{}}
			bpm_data[bpm_name]['data'][bpm_plane] = [np.array(temp_data['FREQ']),np.array(temp_data['AMP'])]
	return bpm_data

def readin_BPM_data_from_SDDS(sdds_file_path, bpm_map):
	bpm_data = {}
	with open(sdds_file_path) as sdds_file:
		for line in sdds_file:
			if line.startswith('#'): continue
			line = line.split()
			assert line[0] in ['0', '1']
			if line[0] == '0': bpm_plane = 'x'
			else: bpm_plane = 'y'
			bpm_name = line[1]
			if bpm_name not in bpm_data:
				bpm_data[bpm_name] = {'pos':bpm_map.getSofBPM(bpm_name), 'data':{}}
			
			tbt_data = [float(p) for p in line[3:]]
			bpm_data[bpm_name]['data'][bpm_plane] = [np.fft.fftfreq(len(tbt_data), d=1), abs(np.fft.fft(tbt_data))]
	return bpm_data

def do_plotting(bpm_data, plane='x'):
	plt.figure()
	for s in range(len(bpm_data)):
		number_of_bpms = len(bpm_data[s])
		number_of_lines = len(bpm_data[s][bpm_data[s].keys()[0]]['data'][plane][0])
		
		tune = np.zeros(number_of_lines*number_of_bpms)
		s = np.zeros(number_of_lines*number_of_bpms)
		amp = np.zeros(number_of_lines*number_of_bpms)
	
		bpm_list = sorted(bpm_data[s].keys())
		for i in range(number_of_bpms): # go through all bpms -> s
			bpm = bpm_list[i]
			s_val = bpm_data[s][bpm]['pos']
			for j in range(number_of_lines): # go through all lines -> tune
				try: data_set = bpm_data[s][bpm]['data'][plane]
				except KeyError: continue # no data for this bpm
				tune[i*number_of_lines+j] = data_set[0][j]
				s[i*number_of_lines+j] = s_val
				amp[i*number_of_lines+j] = data_set[1][j]
		
		# define grid
		tune_grid = np.linspace(-.5, .5, number_of_lines)
		s_grid = np.linspace(0, max(s), number_of_bpms)
		
		normalized_amp = cut_anomalies(normalize_spectrum(amp, data_max=max(amp)), sig=.5)
		
		#amp_grid = griddata((tune, s), cut_anomalies(normalized_amp, sig=3.), (tune_grid[None,:], s_grid[:,None]), method='linear')
		#amp_grid = griddata((tune, s), normalized_amp, (tune_grid[None,:], s_grid[:,None]), method='linear')
		amp_grid = griddata((tune, s), normalized_amp, (tune_grid[None,:], s_grid[:,None]), method='linear')

	
		if s == 0:
			#ax = plt.subplot(2, 2, 1)
			ax = plt.subplot(1, 2, 1)
			ax.set_title('FFT')
		else:
			ax = plt.subplot(2, 2, 3)
			ax.set_title('SUSSIX')

		ticker_space = np.logspace(-6.1, -2.4, 200)
		#ticker_space = np.linspace(min(normalized_amp), max(normalized_amp), 200)
		CF = plt.contourf(tune_grid, s_grid, amp_grid, locator=ticker.FixedLocator(ticker_space), cmap=plt.get_cmap('Blues_r'))
		#CF = plt.contourf(tune_grid, s_grid, amp_grid, locator=ticker.FixedLocator(ticker_space), cmap=plt.get_cmap('prism'))
		#plt.scatter(tune, s, marker=',')

		cb = plt.colorbar(CF, format='%.1e')
		cb.locator = ticker.FixedLocator([1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2])
		cb.formatter = ticker.FixedFormatter(
			['$1\\times10^{-6}$', '$5\\times10^{-6}$', '$1\\times10^{-5}$', '$5\\times10^{-5}$', '$1\\times10^{-4}$', '$5\\times10^{-4}$', '$1\\times10^{-3}$', '$5\\times10^{-3}$']
		)
		cb.update_ticks()
		cb.set_label('Spectral line amplitude [a.u.]')
	
		ax.xaxis.set_major_locator(ticker.MultipleLocator(0.1))
		ax.yaxis.set_major_locator(ticker.MultipleLocator(2000))
	
		plt.xlabel('$Q_x$ $[$1/turn$]$')
		plt.ylabel('$S$ $[$m$]$')
		plt.xlim(0., .5)
		plt.grid(which='both')
	
	# histogram
	plt.subplot(1, 2, 2)
	hist = plt.hist(normalized_amp, np.logspace(-7, 1, 100))
	plt.vlines(ticker_space, 0, max(hist[0]), zorder=9, linewidth=1., color='g', alpha=.5)
	plt.semilogx()
	plt.grid(which='both')
	
	plt.subplots_adjust(left=0.04, right=0.98, top=0.97, bottom=0.04)

def get_measurement_dir_dict(working_dir):
	# returns: measurement_dir_dict = {working_dir+'measurement_subdir':(bpm_directory, sdds_file_path), ...}
	measurement_dir_dict = {}
	
	dir_list = os.listdir(working_dir)
	
	for d in dir_list:
		if os.path.isdir(os.path.join(working_dir, d)) and 'plots' not in d:
			measurement_dir_dict[d] = (
				os.path.join(os.path.join(working_dir, d), '/BPM/'),
				os.path.join(os.path.join(working_dir, d), d+'.sdds.new')
				#os.file_path.join(os.file_path.join(working_dir, d), d+'.sdds.new.nl_corrected')
			)
	
	return measurement_dir_dict

def main():
	#bpm_directory  = '/afs/cern.ch/work/r/rwestenb/MD12/nominalSettings/Beam2@Turn@2012_06_24@23_24_12_666_0/BPM/'
	#sdds_file_path = '/afs/cern.ch/work/r/rwestenb/MD12/nominalSettings/Beam2@Turn@2012_06_24@23_24_12_666_0/Beam2@Turn@2012_06_24@23_24_12_666_0.sdds.new'
	#bpm_directory  = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/measurementsB2inj_diagonal/svd_scan_12/Corrected_8sig8sig_Beam2@Turn@2012_06_25@04_00_22_346_0/BPM/'
	#sdds_file_path = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/measurementsB2inj_diagonal/svd_scan_12/Corrected_8sig8sig_Beam2@Turn@2012_06_25@04_00_22_346_0/Corrected_8sig8sig_Beam2@Turn@2012_06_25@04_00_22_346_0.sdds.new.cleaned'

	#bpm_directory  = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/measurementsB2inj_diagonal/analysis/DriveFakeSignal/BPM/'
	#sdds_file_path = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/measurementsB2inj_diagonal/analysis/DriveFakeSignal/test.sdds.cleaned'


	# get directories
	bpm_map_path = '/afs/cern.ch/work/f/fcarlier/private/Beta-Beat.src/analysisCode/BPMmap/bpmMap.dat'
	#bpm_map_path = '/afs/cern.ch/user/r/rwestenb/workarea/bpmMap_fake.dat'
	#working_dir = '/afs/cern.ch/work/r/rwestenb/MD12/correctedSettings/'
	working_dir = '/afs/cern.ch/work/f/fcarlier/private/MD12/newtest/'
	measurement_dir_dict = get_measurement_dir_dict(working_dir)
	

	#do_plotting([readin_BPM_data_from_SDDS(measurement_dir_dict['Beam2@Turn@2012_06_24@23_24_12_666_0'][1], BPMmap(bpm_map_file=bpm_map_path))], plane='x')

	## to plot all measurements in measurements_to_plot
	j = 0 # just for output
	for i in range(len(measurement_dir_dict)):
		measurement = sorted(measurement_dir_dict.keys())[i]
		for plane in ['x', 'y']:
			j += 1
			print('Plotting (%d/%d): %s (%s)' % (j, len(measurement_dir_dict)*2, measurement, plane))
			do_plotting([
				readin_BPM_data_from_SDDS(measurement_dir_dict[measurement][1], BPMmap(bpm_map_file=bpm_map_path))
			], plane=plane)
			#plt.show()

			plot_path = os.path.join(working_dir, 'plots', measurement+'_'+plane+'.png')
			figure = plt.gcf() # get current figure
			figure.set_size_inches(25, 12)
			plt.savefig(plot_path, dpi=200)
			plt.close(figure)
			print('Saved figure to: %s' % plot_path)
	print('Done!')

if __name__ == '__main__':
	main()
