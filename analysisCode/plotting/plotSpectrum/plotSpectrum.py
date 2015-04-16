#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, re, sys
from BPMmap.readBPMmapFromFile import BPMmap
from outFile.read import read_out_file
from ResonanceLines import ResonanceLines

import matplotlib.pyplot as plt
from matplotlib import rc
rc('font', family='serif')
from matplotlib.ticker import MultipleLocator

import numpy as np

def make_plot(data, colors, mapBPM, title='', resonanceLines={}):
	assert len(colors) == len(data)

	fig = plt.figure()
	fig.patch.set_facecolor('white')

	ax = plt.subplot(111) #, projection='3d')

	if resonanceLines: # draw resonance lines and labels
		for c, lineSet in resonanceLines.items():
			drawnLines = []
			for resonanceLine in lineSet.getResonanceLines():
				if resonanceLine[1] != (0,0) and abs(resonanceLine[0]) < .5: # we don't need to draw obvious (0,0) and lines with tune > 0.5
					ax.vlines(abs(resonanceLine[0]), data['x']['s'].min()-1500., 0., linewidth=1., zorder=9, color=c)
					ax.vlines(abs(resonanceLine[0]), data['x']['s'].max(), data['x']['s'].max()+1500., linewidth=1., zorder=9, color=c)
					if (-resonanceLine[1][0], -resonanceLine[1][1]) not in drawnLines and resonanceLine[1] not in drawnLines: # e.g. (-1, 2) == (1, -2)
						if resonanceLine[1][0] <= 0 and resonanceLine[1][1] <= 0:
							resonanceLine[1] = (-resonanceLine[1][0], -resonanceLine[1][1])
						if c=='black': ypos = data['x']['s'].max()+1700. # resonance label above
						else: ypos = data['x']['s'].min()-2200.           # or below the resonance line
						
						ax.text(abs(resonanceLine[0])-1e-2, ypos, '(%d, %d)' % (resonanceLine[1][0], resonanceLine[1][1]))
						drawnLines.append(resonanceLine[1])
			
	for i in range(len(data)-1):
		dataSet = sorted(data.keys())[i]
		ax.scatter(data[dataSet]['freq'], data[dataSet]['s'], marker='o', label='$'+dataSet+'$', alpha=.5, color=colors[i], zorder=len(data)-i)

	#sList = list(set(data[dataSet]['s']))
	#for s in sList: # BPM names
	#	ax.text(2e-3, s, mapBPM.getBPMsOfS(s)[0])

	ax.set_xlabel('$Q_x$/$Q_y$')
	ax.set_ylabel('$s$')
	plt.title(title)


	plt.xlim([-0., .5])
	ax.xaxis.set_major_locator(MultipleLocator(0.05))
	ax.xaxis.set_minor_locator(MultipleLocator(0.01))
	ax.yaxis.set_major_locator(MultipleLocator(2000))
	ax.yaxis.set_minor_locator(MultipleLocator(1000))
	plt.grid(which='major', linestyle='-', color='grey')
	plt.grid(which='minor')
	
	plt.legend(title='Legend', shadow=True, ncol=1, fancybox=True)
	plt.subplots_adjust(left=0.07, right=0.97, top=0.96, bottom=0.07)
	
	#plt.gcf().set_size_inches(12, 7)
	#plt.savefig('/afs/cern.ch/user/r/rwestenb/Desktop/test.png', dpi=400)
	plt.show()


if __name__=='__main__':
	#dataPath = '/afs/cern.ch/work/r/rwestenb/MD12/nominalSettings/'
	dataPath = '/afs/cern.ch/work/f/fcarlier/private/MD12/test/Beam2@Turn@2012_06_25@01_07_03_339_0/fref/'
	# dataPath = '/afs/cern.ch/work/f/fcarlier/private/Beta-Beat.src/analysisCode/multiParticleSimulation/'
	#dataPath = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/measurementsB2inj_diagonal/analysis/DriveFakeSignal/'
	#dataPath = '/afs/cern.ch/user/r/rwestenb/workarea/11_12_injectionMD/modelB2inj/analysis/'
	
	#dataPath = os.path.join(dataPath, 'Beam2@Turn@2012_06_25@01_07_03_339_0/')
	# dataPath = os.path.join(dataPath, 'results/')
	#dataPath = os.path.join(dataPath, 'Beam2@Turn@2012_06_24@22_36_59_922_0')
	#dataPath = os.path.join(dataPath, 'Corrected_2sig2sig_Beam2@Turn@2012_06_25@01_07_03_339_0')
	#dataPath = os.path.join(dataPath, 'Nominal-MOoff_2sig2sig_Beam2@Turn@2012_06_25@00_22_15_426_0')

	#sddsFileList = [f for f in os.listdir(dataPath) if re.match(r'^.*\.sdds\.new.\cleaned$', f) and os.path.isfile(os.path.join(dataPath, f))]
	sddsFileList = [f for f in os.listdir(dataPath) if re.match(r'^.*.sdds$', f) and os.path.isfile(os.path.join(dataPath, f))]
	#sddsFileList = [f for f in os.listdir(dataPath) if re.match(r'^.*.sdds.new.nl_corrected.cleaned$', f) and os.path.isfile(os.path.join(dataPath, f))]

	try: assert len(sddsFileList) >= 1
	except AssertionError:
		print('No sdds file to read_out_file the BPM positions found!')
		sys.exit(1)

	try: assert len(sddsFileList) == 1
	except AssertionError: print('More than one sdds file to read_out_file the BPM positions found. Choosing the first: %s' % sddsFileList[0])

	mapBPM = BPMmap()

	bpmPath = os.path.join(dataPath, 'BPM')
	bpmFilesList = [f for f in os.listdir(bpmPath) if re.match(r'^BPM.+\.[xy]$', f) and os.path.isfile(os.path.join(bpmPath, f))]

	data = {}

	dataSets = ['x', 'y']
	for dataSet in dataSets: data[dataSet] = {'s':np.array([]), 'freq':np.array([]), 'amp':np.array([])}

	for bpm in bpmFilesList:
		if bpm.endswith('.x'):
			axis = 'x'
		else: # y
			axis = 'y'
		bpmID = '.'.join(bpm.split('.')[:-1])
		bpmData = read_out_file(os.path.join(bpmPath, bpm))
		data[axis]['s'] = np.append(data[axis]['s'], np.array([mapBPM.getSofBPM(bpmID)]*len(bpmData['FREQ'])))
		data[axis]['freq'] = np.append(data[axis]['freq'], np.array(bpmData['FREQ']))
		data[axis]['amp'] = np.append(data[axis]['amp'], np.array(bpmData['AMP']))

	# For fake testing data
	#qx = 0.28
	#qy = 0.31
	
	# For model data
	#qx = 0.279526
	#qy = 0.311095
	
	# 8sig corrected
	qx = 2.797802e-01 # from
	qy = 3.130489e-01 # drive
	
	#qx = 2.646e-1 # to test
	#qy = 3.223e-1
	
	#qx = 0.280013#(1235) # calculated from
	#qy = 0.312762#(913)  # (1, 2) and (1, 1) [error 0.4/0.3%]
	
	#qx = 0.279446#(666) # calculated from
	#qy = 0.312847#(666) # (2, -1) and (-1, 2) [error 0.2/0.2%]
	
	#qx = 0.279698#(398) # calculated from
	#qy = 0.313097#(309) # (1, 1) and (-1, 2) [error 0.1/0.1%] # (1, 2) a bit off
	
	
	'''
	# 2sig corrected
	#qx = 0.281868 # from
	#qy = 0.314276 # drive
	
	#qx = 0.281764#(299) # calculated from
	#qy = 0.314859#(299) # (2, -1) and (-1, 2) [error 0.1/0.1%]
	
	#qx = 0.281466#(163) # calculated from
	#qy = 0.314710#(143) # (1, 1) and (-1, 2) [error 0.1/0.1%] # (2, -1) doesn't fit well
	
	qx = 0.281852#(39) # calculated from
	qy = 0.314322#(39) # (-1, 1) and (1, 1) [error 0.0/0.0%] # error too small, but fits good
	'''
	
	'''
	# 2sig nominal, MO off
	qx = 0.281381 # from
	qy = 0.313792 # drive [(1, 1) a bit off]
	
	#qx = 0.2815000 # by hand adjusted to
	#qy = 0.3137500 # (1, 0) and (1, 1) [error unknown]
	
	#qx = 0.279970 # calculated from
	#qy = 0.310003 # (1, 0) and (-1, 2) [error 1.2/0.6%] # bad: (1, 1) doesn't fit at all
	'''

	orderOfResonances=3
	resonanceLines = {'blue':ResonanceLines(qx=qx, qy=qy, orderOfResonances=orderOfResonances, oneMinus=True), 'black':ResonanceLines(qx=qx, qy=qy, orderOfResonances=orderOfResonances, oneMinus=False)}

	for dataSet in resonanceLines:
		for line in resonanceLines[dataSet].getResonanceLines():
			if line[0] < .5 and abs(line[1][0])+abs(line[1][1]) < 5:
				print('%s -> %s' % (line, dataSet))

	make_plot(data, ['red', 'green'], mapBPM, title=sddsFileList[0], resonanceLines=resonanceLines)
