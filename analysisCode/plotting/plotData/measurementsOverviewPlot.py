#!/usr/bin/env python
# -*- coding: utf8 -*-

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from matplotlib import rc
rc('font', family='serif')

if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 8))
    fig.patch.set_facecolor('white')
    ax = fig.add_subplot(1, 1, 1)

    #ax.set_title('MD 2012 measurements (24th June)')

    ax.set_xlabel('$N\sigma_{x\ \mathrm{nominal}}$')
    ax.set_ylabel('$N\sigma_{y\ \mathrm{nominal}}$')
    
    ax.grid(which='both')
    ax.xaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_locator(MultipleLocator(1))
    
    # kicks = [(sig_x, error_sig_x, sig_y, error_sig_y), ...]
    affected_kicks = [
        (5.5, 0.5, 5.1, 0.3),
        (6.2, 0.2, 4.9, 0.3),
        (6.9, 0.3, 5.4, 0.5),
        (7.2, 0.3, 5.7, 0.2),
        (7.6, 0.3, 6.1, 0.3),
        (7.8, 0.3, 6.2, 0.3),
        (8.2, 0.3, 6.5, 0.3)
    ]
    
    ax.errorbar([k[0] for k in affected_kicks], [k[2] for k in affected_kicks], xerr=[k[1] for k in affected_kicks], yerr=[k[3] for k in affected_kicks], c='r', capsize=4, zorder=1, fmt='.', label='affected')
    ax.scatter([k[0] for k in affected_kicks], [k[2] for k in affected_kicks], c='r', s=20, zorder=100)
    
    other_kicks = [
        (5.7, 0.2, 0.6, 0.1),
        (4.1, 0.2, 4.8, 0.3),
        (4.4, 0.2, 4.8, 0.3),
        (3.8, 0.2, 0.65, 0.09),
        (1.01, 0.06, 3.2, 0.1),
        (2.7, 0.1, 2.2, 0.1),
        (1.8, 0.1, 0.81, 0.06),
        (0.9, 0.4, 1.52, 0.04),
        (1.29, 0.05, 0.95, 0.05),
        (7.5, 0.3, 0.6, 0.2),
        (2.8, 0.2, 6.4, 0.7),
        (1.3, 0.1, 7.3, 0.4),
        (1.4, 0.2, 8.0, 0.4),
        (1.4, 0.2, 8.4, 0.4),
        (1.5, 0.2, 8.8, 0.4),
        (1.6, 0.2, 9.1, 0.4),
        (7.6, 0.3, 1.5, 0.2),
        (8.1, 0.3, 0.5, 0.1),
        (9.3, 0.3, 0.6, 0.2),
        (10.2, 0.4, 0.7, 0.2),
        (9.9, 0.4, 0.6, 0.2)
    ]
    
    ax.errorbar([k[0] for k in other_kicks], [k[2] for k in other_kicks], xerr=[k[1] for k in other_kicks], yerr=[k[3] for k in other_kicks], c='g', capsize=4, zorder=1, fmt='.', label='not affected')
    ax.scatter([k[0] for k in other_kicks], [k[2] for k in other_kicks], c='g', s=20, zorder=100)
    
    ax.set_xlim(0,11)
    ax.set_ylim(0,11)
    
    ax.legend()
    
    plt.subplots_adjust(left=0.11, right=0.97, top=0.97, bottom=0.11)
    
    plt.gcf().set_size_inches(5, 5)
    plt.savefig("/afs/cern.ch/work/f/fcarlier/private/plots/affectedMeasurements.pdf", dpi=200)
    #plt.show()
