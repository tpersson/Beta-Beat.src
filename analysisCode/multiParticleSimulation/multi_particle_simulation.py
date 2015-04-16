import __init__
import logging, subprocess, os, sys, time
from optparse import OptionParser
from multiprocessing import Manager, Pool
import numpy as np
from Python_Classes4MAD import madxrunner
import helper

all_tracking_data = {}

def madx_job(job_id, working_directory, number_of_particles, number_of_turns):
    def init_files(working_directory, number_of_particles, twiss, kick_strength):
        logger.debug("Getting initial conditions")
        if not os.path.exists(working_directory): os.makedirs(working_directory)
        tracking_code = helper.madx_script_parts['tracking_prefix']
#         tracking_code = helper.madx_script_parts['tracking_prefix_thick']
        '''Create the needed madx script including the static model part and the generated tracking code.'''
        # tracking_code = helper.madx_script_parts['tracking_prefix']
        time_seed = int(time.time())
        np.random.seed(time_seed*job_id)
        x, px, y, py = helper.get_initial_particle_position_and_momentum(twiss['alpha'], twiss['beta'], twiss['eps'], number_of_particles=number_of_particles)
#         px = px*0.
#         py = py*0.
#         x = x*0.
#         y = y*0.
        # kick particles with sqrt(Action*beta)
        x += np.sqrt(kick_strength[0]*(twiss['beta'][0]/(twiss['alpha'][0]**2 +1))) # amplitude of kick (about 8sig8sig)
        y += np.sqrt(kick_strength[1]*(twiss['beta'][1]/(twiss['alpha'][1]**2 +1)))

        for i in range(number_of_particles):
            tracking_code += helper.madx_script_parts['tracking_script'] % (x[i], px[i], y[i], py[i])
        tracking_code += helper.madx_script_parts['tracking_suffix'] % number_of_turns
        tracking_code = helper.madx_script_parts['call_model'] + tracking_code
#         tracking_code = tracking_code.replace("{{USED_MODEL}}", "ptc_codes/non_linear_thin_newdetune.madx") #nominal_thick_mps.madx")
#         tracking_code = tracking_code.replace("{{USED_MODEL}}", "ptc_codes/non_linear_thin_mps.madx") #nominal_thick_mps.madx")
        tracking_code = tracking_code.replace("{{USED_MODEL}}", "ptc_codes/non_linear_surv.line.mps.madx") #nominal_thick_mps.madx")
        tracking_code = tracking_code.replace("{{OUTPUT_PATH}}", working_directory)
 
#         print tracking_code
#         for i in range(number_of_particles):
#             tracking_code += helper.madx_script_parts['tracking_script'] % (x[i], px[i], y[i], py[i])
#         tracking_code += helper.madx_script_parts['tracking_suffix'] % number_of_turns
#         tracking_code = helper.madx_script_parts['model'] + tracking_code
#         tracking_code = tracking_code.replace("{{STATIC}}", os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','madx_codes', "static_files"))
#         tracking_code = tracking_code.replace("{{OUTPUT_PATH}}", working_directory)
     
#         print tracking_code
        
        with open('madx_nom_thick_fringe_off','w') as madx_log_file:
            madx_log_file.write(tracking_code)
        
        logger.debug('Executing madx...')
        t0 = time.time()
        with open(os.path.join(working_directory, 'madx.log'), 'w') as log_file:
            madxrunner.runForInputString(tracking_code, stdout=log_file)
        logger.info('Simulation done (%.3fs)...', (time.time()-t0))

    def collect_data(trackone_path, number_of_turns):
        logging.info('Starting collect')
        tracking_data = {}
        with open(trackone_path) as track_file: 
            line = '' 
            while not line.startswith('#'): line = track_file.readline() # skip header 

            while line:
                assert line.startswith('#')
                header_line = line.split() 
                element_name = header_line[5]
                element_pos = -1
                turn = -1
                number_of_turns = int(header_line[2])-1
                if 'BPM' in element_name: # BPM element, read data
                    if element_name in tracking_data:
                        element_data = tracking_data[element_name]
                    else:
                        element_data = {'S':-1, 'PARTICLES':np.zeros(number_of_turns), 'DATA':{'X':np.zeros(number_of_turns), 'Y':np.zeros(number_of_turns)}}
             
                    # get actual positions and summarize, also determine element_pos 
                    number_of_particles = int(header_line[3])
                    for _ in range(number_of_particles): 
                        data_line = track_file.readline().split()
                        if turn == -1: turn = int(data_line[1]) - 1
                        if element_data['S'] == -1: element_data['S'] = float(data_line[8])
                        element_data['DATA']['X'][turn] += float(data_line[2])
                        element_data['DATA']['Y'][turn] += float(data_line[4])
                        element_data['PARTICLES'][turn] += 1
                    tracking_data[element_name] = element_data
                else: # i.e. START element, skip
                    for _ in range(int(header_line[3])): track_file.readline()

                line = track_file.readline() # read next header line 
        return tracking_data
    
    # Define constants
    logger = logging.getLogger('job%04d' % job_id)
    logger.info('Job %04d started...' % job_id)
    madx_script_file = os.path.join(working_directory, 'job.multi_particle.madx')
    track_file_path = os.path.join(working_directory, 'trackone')
    twiss = {'alpha':(2.323750151, -2.609936877), 'beta':(122.1802439, 214.9669053), 'eps':(3.5e-9, 4.0e-9)} # alpha and beta from model twiss at S = 0 at IP3. Eps from measured values 2012.
    
    # Action 2J
    kick_values   = [   (0.53e-6, 0.33e-6),
                        (0.48e-6, 0.30e-6),
                        (0.45e-6, 0.29e-6),
                        (0.40e-6, 0.25e-6),
                        (0.37e-6, 0.23e-6),
                        (0.30e-6, 0.19e-6),
                        (0.24e-6, 0.20e-6)   ]
#     kick_strength = kick_values[0]
    kick_strength = (5.45980931564e-07, 3.81710337296e-07)
    start_time = time.time()

    # do the main work
    init_files(working_directory, number_of_particles, twiss, kick_strength)
    result = collect_data(track_file_path, number_of_turns) # adds the tracking_data of this job
    os.remove(track_file_path)
    logger.info('Job done! (overall runtime: %.3fs)', (time.time()-start_time))
    return result

def parse_args():
    usage = 'Usage: %prog -w WORKING_DIR -o OUT_FILE_PATH [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-w', '--working-dir', help='file path of the working directory', action='store', type='string', dest='working_directory', default=os.path.dirname(os.path.abspath(__file__)) )
    parser.add_option('-o', '--out-file-path', help='file path of the resulting out file', action='store', type='string', dest='out_file_path')
    parser.add_option('-p', '--particles', help='number of particles to track (per job) [default: %default]', action='store', type='int', dest='number_of_particles', default=1)
    parser.add_option('-j', '--jobs', help='number of jobs to run [default: %default]', action='store', type='int', dest='number_of_jobs', default=1)
    parser.add_option('-t', '--turns', help='number of turns to track [default: %default]', action='store', type='int', dest='number_of_turns', default=1024)
    parser.add_option('-n', '--processes', help='number of process to be executed at the same time', action='store', type='int', dest='number_of_processes', default=4)
    parser.add_option('-l', '--log-level', help='set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)', action='store', type='string', dest='log_level', default='INFO')
    
    (options, _) = parser.parse_args()
    
    # setup logging
    numeric_log_level = getattr(logging, options.log_level, None)
    if not isinstance(numeric_log_level, int): raise ValueError('Invalid log level: %s' % options.log_level)
    logging.basicConfig(level=numeric_log_level, format='%(asctime)s %(name)-7s %(levelname)-8s: %(message)s')

    if not options.working_directory:
        parser.print_help()
        logging.critical('Error: -w is necessary!')
        sys.exit(1)
    if not options.out_file_path:
        options.out_file_path = os.path.join(options.working_directory, 'results.sdds')
        logging.warning('No outfile given! Using: %s' % options.out_file_path)
    
    return options


def gather_all_data(tracking_data):
    for bpm_name in tracking_data:
        if not bpm_name in all_tracking_data:
            all_tracking_data[bpm_name] = {'S':tracking_data[bpm_name]['S'], 'PARTICLES':np.zeros(options.number_of_turns), 'DATA':{'X':np.zeros(options.number_of_turns), 'Y':np.zeros(options.number_of_turns)}} 
        for turn in range(len(tracking_data[bpm_name]['PARTICLES'])):
            all_tracking_data[bpm_name]['DATA']['X'][turn] += tracking_data[bpm_name]['DATA']['X'][turn]
            all_tracking_data[bpm_name]['DATA']['Y'][turn] += tracking_data[bpm_name]['DATA']['Y'][turn]
            all_tracking_data[bpm_name]['PARTICLES'][turn] += tracking_data[bpm_name]['PARTICLES'][turn]   

if __name__ == '__main__':
    '''
    Limits the number of processes using Pool. The jobs are called asynchroniously using apply_async. 
    It calls madx_job with the needed arguments, to the newly created directory job00xx.
    '''
    options = parse_args()
    logging.debug("start this code")

    job_pool = Pool(processes=options.number_of_processes)

    for job_id in range(1, options.number_of_jobs+1):
        #madx_job(job_id, os.path.join(options.working_directory, 'job%04d' % job_id), options.number_of_particles, options.number_of_turns) # comment this line in (and the next out) for single threading
        job_pool.apply_async(madx_job, args=(job_id, os.path.join(options.working_directory, 'job%04d' % job_id), options.number_of_particles, options.number_of_turns,), 
                             callback=gather_all_data)

        logging.debug('Submitted job %04d/%04d.', job_id, options.number_of_jobs)
    job_pool.close() # no more tasks will be submitted
    job_pool.join()

    logging.info('Calculating BPM data...')
    bpm_data = helper.calculate_BPM_data(all_tracking_data)
    
    logging.info('Writing BPM data...')
    helper.write_BPM_data(bpm_data, options.out_file_path)
    
    logging.info('Done!')
