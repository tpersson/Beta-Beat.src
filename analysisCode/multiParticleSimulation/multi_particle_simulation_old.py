'''This script will create, run and process a multi particle madx simulation.

First a madx script gets created with the given number_of_particles, which is then executed.
After execution the needed output is collected and then transformed into bpm_data and written out.'''

import logging, subprocess, os, sys, time
from optparse import OptionParser
from multiprocessing import Manager, Pool
import numpy as np

import helperrobert

# has to be done here, otherwise we will have to pass the manager.dict() object to the processes which is not possible due to a current bug in the manager proxy calls
# See: http://stackoverflow.com/questions/8640367/python-manager-dict-in-multiprocessing
manager = Manager()
tracking_data = manager.dict()

def madx_job(job_id, working_directory, number_of_particles, number_of_turns):
    def init_files(working_directory, number_of_particles, twiss, kick_strength):
        if not os.path.exists(working_directory): os.makedirs(working_directory)
        
        '''Create the needed madx script including the static model part and the generated tracking code.'''
        tracking_code = helper.madx_script_parts['tracking_prefix']
        time_seed = int(time.time())
        np.random.seed(time_seed*job_id)
        x, px, y, py = helper.get_initial_particle_position_and_momentum(twiss['alpha'], twiss['beta'], twiss['eps'], number_of_particles=number_of_particles)
        
        # kick particles with sqrt(Action*beta)
        # x += np.sqrt(kick_strength[0]*twiss['beta'][0]) # amplitude of kick (about 8sig8sig)
        # y += np.sqrt(kick_strength[1]*twiss['beta'][1])
        x += 3e-3
        y += 3e-3
        # x = [0.,0.]
        # y = [0.,0.]
        # px = [-1.e-7,-1.e-7]
        # py = [-1.e-7,-1.e-7]

        for i in range(number_of_particles):
            tracking_code += helper.madx_script_parts['tracking_script'] % (x[i], px[i], y[i], py[i])
        tracking_code += helper.madx_script_parts['tracking_suffix'] % number_of_turns

        with open(madx_script_file, 'w') as madx_script:
            madx_script.write(helper.madx_script_parts['model'])
            madx_script.write(tracking_code)
        logger.debug('Wrote tracking script to: "%s"', madx_script_file)
        
        
        '''Creates all the other needed static files for the madx job.'''
        for file_name in helper.static_file_contents:
            file_path = os.path.join(working_directory, file_name)
            with open(file_path, 'w') as static_file:
                static_file.write(helper.static_file_contents[file_name])
            logger.debug('Wrote static file: "%s"', file_path)

    def simulate(working_directory, madx_script_file):
        '''Execute the created madx script to calculate the particle tracks.'''
        logger.debug('Executing madx...')
        t0 = time.time()
        with open(os.path.join(working_directory, 'madx.log'), 'w') as log_file:
            subprocess.call('madx %s' % madx_script_file, shell=True, cwd=working_directory, stdout=log_file)
        logger.info('Simulation done (%.3fs)...', (time.time()-t0))

    def collect_data(track_file_path, number_of_turns):
        logger.debug('Gathering tracking data...')

        with open(track_file_path) as track_file: 
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
                    for _ in range(int(header_line[3])): 
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
               
    # Define constants
    logger = logging.getLogger('job%04d' % job_id)
    logger.info('Job %04d started...' % job_id)
    madx_script_file = os.path.join(working_directory, 'job.multi_particle.madx')
    track_file_path = os.path.join(working_directory, 'trackone')
    twiss = {'alpha':(2.323750151, -2.609936877), 'beta':(122.1802439, 214.9669053), 'eps':(3.5e-9, 4.0e-9)} # alpha and beta from model twiss at S = 0 at IP3. Eps from measured values 2012.
   
    # Action 2J
    kick_strength = (0.53e-6, 0.33e-6)
    start_time = time.time()

    # do the main work
    init_files(working_directory, number_of_particles, twiss, kick_strength)
    simulate(working_directory, madx_script_file)
    collect_data(track_file_path, number_of_turns) # adds the tracking_data of this job

    logger.info('Job done! (overall runtime: %.3fs)', (time.time()-start_time))

def parse_args():
    usage = 'Usage: %prog -w WORKING_DIR -o OUT_FILE_PATH [options]'
    parser = OptionParser(usage=usage)
    parser.add_option('-w', '--working-dir', help='file path of the working directory', action='store', type='string', dest='working_directory')
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

if __name__ == '__main__':
    '''
    Limits the number of processes using Pool. The jobs are called asynchroniously using apply_async. 
    It calls madx_job with the needed arguments, to the newly created directory job00xx.
    '''
    options = parse_args()
 
    job_pool = Pool(processes=options.number_of_processes)
   
    for job_id in range(1, options.number_of_jobs+1):
        #madx_job(job_id, os.path.join(options.working_directory, 'job%04d' % job_id), options.number_of_particles, options.number_of_turns) # comment this line in (and the next out) for single threading
        job_pool.apply_async(madx_job, args=(job_id, os.path.join(options.working_directory, 'job%04d' % job_id), options.number_of_particles, options.number_of_turns,))
        logging.debug('Submitted job %04d/%04d.', job_id, options.number_of_jobs)
    job_pool.close() # no more tasks will be submitted

    job_pool.join()
    
    new_thing = {}
    for name in tracking_data.keys():
        new_thing[name] = tracking_data[name]

    print "Result: ", tracking_data['BPM.12L3.B2'] 
    logging.info('Calculating BPM data...')
    bpm_data = helper.calculate_BPM_data(new_thing)
    print "BPM_data:  ", bpm_data['BPM.12L3.B2']
    logging.info('Writing BPM data...')
    helper.write_BPM_data(bpm_data, options.out_file_path)
    
    logging.info('Done!')
