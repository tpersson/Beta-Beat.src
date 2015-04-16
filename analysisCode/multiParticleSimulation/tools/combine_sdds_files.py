# -*- coding: utf8 -*-

# script to combine multiple sdds simulations to one file
# we multiply the positions by the number of particles and then add both positions, then divide by the sum of particle counts to get the avarage again

import numpy as np
import os, time

def read_BPM_data_from_SDDS_file(sdds_file_path, start_turn=None, end_turn=None):
        bpm_data = {}
	number_of_turns = end_turn-start_turn if start_turn and end_turn else 0

	print('Reading %s...' % sdds_file_path)
        assert os.path.exists(sdds_file_path)
        with open(sdds_file_path) as sdds_file:
                for line in sdds_file:
			if not line.startswith('#'):
                        	line = line.split()
				bpm_name = line[1]
				if number_of_turns == 0: number_of_turns = len(line)-3
	                        if 'BPM' in bpm_name:
					if bpm_name not in bpm_data: bpm_data[bpm_name] = {'DATA':{'X':[], 'Y':[]}, 'S':0}
	                                assert line[0] in ['0', '1']
	                                if line[0] == '0': plane = 'X'
	                                else: plane = 'Y'
	                                if not start_turn: start_turn = 0
	                                if not end_turn: end_turn = len(line)
					bpm_data[bpm_name]['S'] = float(line[2])
	                                bpm_data[bpm_name]['DATA'][plane] = np.array([float(d) for d in line[3+start_turn:end_turn]])
			else:
				if line.startswith('#number of particles'):
					bpm_data['PARTICLES'] = np.array([float(n) for n in line.split(':')[1].split()])
	assert 'PARTICLES' in bpm_data

	return (bpm_data, number_of_turns)

def write_BPM_data_to_SDDS_file(sdds_out_file, bpm_data):
	number_of_turns = len(bpm_data[bpm_data.keys()[0]]['DATA']['X'])
	number_of_monitors = len(bpm_data)-1
	header = '''#SDDSASCIIFORMAT v1
#Beam: LHCB2
#Created: %s By: SDDS combine script for multiparticle simulation
#number of particles: %s
#bunchid :0
#number of turns :%d
#number of monitors :%d
''' % (time.strftime('%Y-%m-%d#%H-%M-%S'), ' '.join(format(d, '.0f') for d in bpm_data['PARTICLES']), number_of_turns, number_of_monitors)
	with open(sdds_out_file, 'w') as sdds_file:
		sdds_file.write(header)
		for bpm in bpm_data.keys(): # .keys() is needed here, because of the manager dict type
			if 'BPM' in bpm:
				sdds_file.write('%d %s      %.5f %s\n' % (0, bpm, bpm_data[bpm]['S'], '  '.join(format(d, '.5f') for d in bpm_data[bpm]['DATA']['X'])))
				sdds_file.write('%d %s      %.5f %s\n' % (1, bpm, bpm_data[bpm]['S'], '  '.join(format(d, '.5f') for d in bpm_data[bpm]['DATA']['Y'])))
	print('Wrote data to %s!' % sdds_out_file)

def combine_sdds_files(sdds_file_names, sdds_out_file):
	bpm_data = {}
	number_of_particles = []

	for sdds_file_name in sdds_file_names:
		job_data, job_turns = read_BPM_data_from_SDDS_file(sdds_file_name)

		# combine data
		if 'PARTICLES' not in bpm_data: bpm_data['PARTICLES'] = np.zeros(job_turns)
		bpm_data['PARTICLES'] += job_data['PARTICLES']
		for bpm_name in job_data:
			if 'BPM' in bpm_name:
				if bpm_name not in bpm_data:
					bpm_data[bpm_name] = {'DATA':{'X':np.zeros(job_turns), 'Y':np.zeros(job_turns)}, 'S':0}
				for plane in job_data[bpm_name]['DATA']:
					if bpm_data[bpm_name]['S'] == 0: bpm_data[bpm_name]['S'] = job_data[bpm_name]['S']
					bpm_data[bpm_name]['DATA'][plane] += job_data[bpm_name]['DATA'][plane]*job_data['PARTICLES']

	# calc mean
	for bpm_name in bpm_data:
		if 'BPM' in bpm_name:
			for plane in bpm_data[bpm_name]['DATA']:
				bpm_data[bpm_name]['DATA'][plane] /= bpm_data['PARTICLES']

	# write out
	write_BPM_data_to_SDDS_file(sdds_out_file, bpm_data)

if __name__ == '__main__':
	combine_sdds_files(
		['/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newdet/2500/1/mps.newdet.2500.sdds',
          '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newdet/2500/2/mps.newdet.2500.2.sdds',
          '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newdet/2500/3/mps.newdet.2500.3.sdds'],
		 '/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/multiParticleSimulation/newdet/combined/mps_combined.sdds'
	)
	print('Done!')
