import multiParticleSimulation.helper as helper
import matplotlib.pyplot as plt

import os, re

def readMADXfile(madx_job_file):
	assert os.path.exists(madx_job_file)

	data = ([], [], [], [])
	
	for line in open(madx_job_file):
		if line.strip().startswith('ptc_start'):
			line = re.sub(', [a-z]+=', ' ', line).replace(';', '').split()[1:]
			for i in range(len(data)):
				data[i].append(float(line[i]))

	return data

fig = plt.figure(figsize=(23, 13))
fig.patch.set_facecolor('white')
ax = fig.add_subplot(1, 2, 1)
ax.grid()
ax.set_label('X')
ax.set_xlim([-.01, .01])
ax.set_ylim([-1e-4, 1e-4])
ay = fig.add_subplot(1, 2, 2)
ay.grid()
ay.set_label('Y')
ay.set_xlim([-.01, .01])
ay.set_ylim([-1e-4, 1e-4])

x, p_x, y, p_y = readMADXfile('/afs/cern.ch/work/f/fcarlier/public/multiParticleTest/job0001/job.multi_particle.madx')

ax.scatter(x, p_x, alpha=.5)
ay.scatter(y, p_y, alpha=.5)

plt.subplots_adjust(left=0.05, right=0.97, top=0.98, bottom=0.04)
plt.show()
