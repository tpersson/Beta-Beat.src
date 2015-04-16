from pylab import figure, show, rand
from matplotlib.patches import Ellipse


ells = Ellipse(xy=(0,0),width=.5, height=.3, angle=30)

fig = figure()
ax = fig.add_subplot(111, aspect='equal')
# kwrg = {'facecolor':'none', 'edgecolor':ec, 'alpha':a, 'linewidth':lw}

ax.add_patch(ells)
ells.set_facecolor('none')
ells.set_edgecolor([0,0,0])

ax.set_xlim(-.6,.6)
ax.set_ylim(-.6,.6)

show()