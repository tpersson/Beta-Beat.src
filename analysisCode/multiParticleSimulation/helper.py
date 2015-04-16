import numpy as np
import logging
import time
import os

#====================================================================================================    
#               HELPER FUNCTIONS
#====================================================================================================


def get_initial_particle_position_and_momentum(alpha, beta, eps, number_of_particles=1000):
    try: assert alpha[0] != 0. and beta[0] != 0. and eps[0] != 0.
    except: logging.critical('Alpha, Beta and Epsilon have to be != 0!')
    alpha, beta, eps = np.array(alpha), np.array(beta), np.array(eps)
    
    x, y, p_x, p_y = [], [], [], []
    for _ in range(number_of_particles):
        A = np.sqrt(2*np.random.exponential(scale=eps)) # random sqrt(E)
        phi = np.array([2*np.pi*np.random.random(), 2*np.pi*np.random.random()])
    
        x.append(A[0]*np.sqrt(beta[0]) * np.cos(phi[0]))
        y.append(A[1]*np.sqrt(beta[1]) * np.cos(phi[1]))
        p_x.append(-A[0]/np.sqrt(beta[0]) * (alpha[0]*np.cos(phi[0]) + np.sin(phi[0])))
        p_y.append(-A[1]/np.sqrt(beta[1]) * (alpha[1]*np.cos(phi[1]) + np.sin(phi[1])))
    return (np.array(x), np.array(p_x), np.array(y), np.array(p_y))



def calculate_BPM_data(tracking_data):
    t0 = time.time()
    for element in tracking_data.keys(): # .keys() is needed here, because of the manager dict type
        for plane in ['X', 'Y']:
            if tracking_data[element]['PARTICLES'].all() != 0.:
                tracking_data[element]['DATA'][plane] = np.divide(tracking_data[element]['DATA'][plane], tracking_data[element]['PARTICLES'])
            else: # all particles lost!
                logging.warning('All particles for element %s (%s) lost! Skipping this data!' % (element, plane))
                tracking_data[element]['DATA'][plane] = np.zeros(len(tracking_data[element]['DATA'][plane]))
                break
    logging.debug('BPM signal calculation time: %.3fs' % (time.time()-t0))

    return tracking_data



def write_BPM_data(bpm_data, sdds_file_path):
    number_of_turns = len(bpm_data[bpm_data.keys()[0]]['DATA']['X'])
    number_of_monitors = len(bpm_data)
    header = '''#SDDSASCIIFORMAT v1
#Beam: LHCB2
#Created: 2014-04-15#12-49-43 By: Multiparticle Simulation
#number of particles: %s
#bunchid :0
#number of turns :%d
#number of monitors :%d
''' % (' '.join(np.char.mod('%d', bpm_data[bpm_data.keys()[0]]['PARTICLES'])), number_of_turns, number_of_monitors)
    with open(sdds_file_path, 'w') as sdds_file:
        sdds_file.write(header)
        for bpm in bpm_data.keys(): # .keys() is needed here, because of the manager dict type
            sdds_file.write('%d %s      %.5f %s\n' % (0, bpm, bpm_data[bpm]['S'], '  '.join(format(d, '.5f') for d in bpm_data[bpm]['DATA']['X'])))
            sdds_file.write('%d %s      %.5f %s\n' % (1, bpm, bpm_data[bpm]['S'], '  '.join(format(d, '.5f') for d in bpm_data[bpm]['DATA']['Y'])))

#====================================================================================================    
#               STATIC FILES FOR MADX
#====================================================================================================

madx_script_parts = {
  'call_model':'''
call file="/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/madx_codes/{{USED_MODEL}}"; 
''',
    'tracking_prefix':'''
ptc_create_universe;
ptc_create_layout,model=3,method=4,nst=10,exact;
ptc_align;
ptc_setswitch, fringe = true;
''',
    'tracking_script':'''
ptc_start, x=%.8f, px=%.8f, y=%.8f, py=%.8f;''',
    'tracking_suffix':'''
call, file="/afs/cern.ch/work/f/fcarlier/public/Beta-Beat.src/analysisCode/madx_codes/static_files/ptcobserveLIST";
ptc_track,icase=5,closed_orbit,dump,turns=%d,norm_no=5,ELEMENT_BY_ELEMENT, onetable, file='{{OUTPUT_PATH}}/track';
ptc_track_end;
ptc_end;

stop;
''',
    'tracking_prefix_thick':'''
ptc_create_universe;
ptc_create_layout,model=2,method=2,nst=3; !,exact,resplit,thin=.0005,xbend=.0005;
ptc_align; 
ptc_setswitch, fringe = False;
'''
}
