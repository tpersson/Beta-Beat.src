import multiParticleSimulation.helper as helper
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(23, 13))
fig.patch.set_facecolor('white')
ax = fig.add_subplot(1, 2, 1)
ax.grid()
ax.set_xlim([-.03, .03])
ax.set_ylim([-.001, .001])
ay = fig.add_subplot(1, 2, 2)
ay.grid()
ay.set_xlim([-.03, .03])
ay.set_ylim([-.001, .001])

twiss = {'alpha':(2.323750151, -2.609936877), 'beta':(122.1802439, 214.9669053), 'eps':(0.53e-6, 0.33e-6)} # alpha and beta from model twiss at S = 0 at IP3. Eps from measured values 2012.

x, p_x, y, p_y = helper.get_initial_particle_position_and_momentum(twiss['alpha'], twiss['beta'], twiss['eps'], number_of_particles=5000)

ax.scatter(x, p_x, alpha=.5)
ay.scatter(y, p_y, alpha=.5)

plt.subplots_adjust(left=0.04, right=0.97, top=0.97, bottom=0.04)
plt.show()
