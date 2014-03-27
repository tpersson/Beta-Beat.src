'''
Created on 16 Aug 2013

@author: vimaier

This module tests the output files of SegmentBySegment. First it runs SegmentBySegment_0.33.py in the dir
to produce valid output.
Then it runs the modified version in the parent dirctory. After that it compares the output.
'''
import unittest
import os
import sys
import subprocess

CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
# Path 'x/Beta-Beat.src/SegmentBySegment/test'

import __init__  # @UnusedImport init will include paths
import Utilities.iotools
import Utilities.ndiff
import madxrunner
import pstats

_SHORT_RUN = False  # If True, SBS will only run on first dir
_NO_VALID_RUN = True  # If True, will not run valid SBS except if no valid output files are available
_SHOW_SLOWEST_CALLS = False  # If True, will show a list of the most time consuming calls in the script

_TestOutput__ARGUMENTS_FILE_NAME = "arguments.txt"  # This file is located in the input run dirs. Stores arguments for sbs


class TestOutput(unittest.TestCase):

    path_to_modified_sbs = os.path.join(CURRENT_PATH, "..", "SegmentBySegment.py")

    path_to_valid = os.path.join(CURRENT_PATH, "data", "valid")
    path_to_to_check = os.path.join(CURRENT_PATH, "data", "to_check")
    path_to_input = os.path.join(CURRENT_PATH, "data", "input")

    __have_to_run_valid_file = False
    successful = False

    def setUp(self):
        if(_SHOW_SLOWEST_CALLS):
            self.profile_file_path = os.path.join(self.path_to_input, "prof_results")
        self._check_if_valid_output_exist_and_set_attribute()
        self._delete_modified_and_if_desired_valid_output()

    def tearDown(self):
        if TestOutput.successful:
            self._delete_modified_and_if_desired_valid_output()

    def testOutput(self):
        print "Start TestOutput of SBS"
        run_dir_names = Utilities.iotools.get_all_dir_names_in_dir(TestOutput.path_to_input)
        print run_dir_names
        for dir_name in run_dir_names:
            self._run_modified_file(dir_name)
            self._compare_output_dir(dir_name)
            if self._break_after_first_run():
                break
        print "End TestOutput of SBS"

    #===============================================================================================
    # helper
    #===============================================================================================
    def _check_if_valid_output_exist_and_set_attribute(self):
        if self._no_valid_output_exists():
            print "No valid output. Have to run valid file."
            self.__have_to_run_valid_file = True

    def _no_valid_output_exists(self):
        """
        Returns true if cannot find valid output. Assuming that every subdir of path_to_valid has
        a linx and liny file(valid output).
        """
        return not self._valid_output_exists()

    def _valid_output_exists(self):
        """ True, if valid output available.
            Assuming that every subdir of path_to_valid is not empty."""
        if Utilities.iotools.not_exists_directory(TestOutput.path_to_valid):
            return False
        is_valid = False
        for item in os.listdir(TestOutput.path_to_valid):
            abs_item = os.path.join(TestOutput.path_to_valid, item)
            if os.path.isdir(abs_item):
                is_valid = Utilities.iotools.is_not_empty_dir(abs_item)
                if not is_valid:
                    return False
        return True

    def _delete_modified_and_if_desired_valid_output(self):
        ''' Deletes content in path_to_valid and path_to_to_check. '''
        Utilities.iotools.delete_content_of_dir(TestOutput.path_to_to_check)

    def _run_dir(self, path_to_out_run_dir_root, path_to_sbs, dir_name):
        arguments_list = self._prepare_and_get_arguments_list(path_to_out_run_dir_root, dir_name)
        print "    Run:", dir_name
        self._run_sbs(path_to_sbs, arguments_list)

    def _prepare_and_get_arguments_list(self, path_to_out_run_dir_root, dir_name):
        path_to_run_input = os.path.join(TestOutput.path_to_input, dir_name)
        path_to_run_output = os.path.join(path_to_out_run_dir_root, dir_name)
        Utilities.iotools.create_dirs(path_to_run_output)

        args_dict = {}
        args_dict["--mad"] = madxrunner.get_sys_dependent_path_to_mad_x()
        args_dict["--bbsource"] = Utilities.iotools.get_absolute_path_to_betabeat_root()
        args_dict["--path"] = path_to_run_input
        args_dict["--save"] = path_to_run_output
        args_dict["--twiss"] = os.path.join(path_to_run_input, "model", "twiss_elements.dat")
        # model is presumed to be in subdir model of the run directory

        args_list = []
        for key in args_dict:
            args_list.append(key + " " + args_dict[key])

        args_list.append(self._get_args_from_file_in_run_dir(path_to_run_input))

        return args_list

    def _get_args_from_file_in_run_dir(self, path_to_run_input):
        """ Reads the arguments from file __ARGUMENTS_FILE_NAME """
        arg_file = open(os.path.join(path_to_run_input, _TestOutput__ARGUMENTS_FILE_NAME))
        arg_line = arg_file.readline()  # Arguments are presumed to be in first line
        arg_file.close()
        return arg_line

    def _run_modified_file(self, dir_name):
        self._run_dir(self.path_to_to_check, self.path_to_modified_sbs, dir_name)

    def _run_sbs(self, path_to_sbs, arguments_list):
        call_command = os.path.abspath(path_to_sbs) + " " + " ".join(arguments_list)
        if(_SHOW_SLOWEST_CALLS):
            call_command = " -m cProfile -o " + self.profile_file_path + " " + call_command
        call_command = sys.executable + " " + call_command

        process = subprocess.Popen(call_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=True)

        # wait for the process to terminate
        (out_stream, err_stream) = process.communicate()

        errcode = process.returncode

        if 0 != errcode:
            print "Error running command:", call_command
            print "Printing output:-------------------------"
            print out_stream
            print >> sys.stderr, "Printing error output:-------------------"
            print >> sys.stderr, err_stream

    def _compare_output_dir(self, dir_name):
        print "  Comparing output files"
        valid_dir = os.path.join(self.path_to_valid, dir_name)
        to_check_dir = os.path.join(self.path_to_to_check, dir_name)

        self._compare_dirs_with_ndiff(valid_dir, to_check_dir)
        TestOutput.successful = True
        if(_SHOW_SLOWEST_CALLS):
            stats = pstats.Stats(self.profile_file_path)
            print "Test successful"
            print "Most time consuming calls:"
            stats.strip_dirs().sort_stats('cumulative').print_stats(10)
            Utilities.iotools.delete_item(self.profile_file_path)

    def _compare_dirs_with_ndiff(self, valid_dir, to_check_dir):
        # sbsalfax_IP2.out has additional columns and need therefore a special config file
        # The twiss files have the creation date and time in them, we need to ignore that line
        # The MAD-X files have some absolute routes that have to be ignored
        regex_to_config_files = {
                                 '^sbsalfax_IP2.out$': self._get_special_cfg_file_for_alfax_IP2(),
                                 '.*\.twiss$': self._get_special_cfg_file_for_twiss(),
                                 '.*\.dat$': self._get_special_cfg_file_for_twiss(),
                                 '.*\.madx$': self._get_special_cfg_file_for_madx(),
                                 }
        self.assertTrue(
                        Utilities.ndiff.compare_dirs_with_cfg_regex_files(valid_dir,
                                                                          to_check_dir,
                                                                          None,
                                                                          regex_to_config_files,
                                                                          self._get_master_config_file()),
                        "Directories not equal: " + valid_dir + " and " + to_check_dir
                        )

    def _get_master_config_file(self):
        path_to_cfg = os.path.join(self.path_to_input, "general_ndiff_config.cfg")
        return path_to_cfg

    def _get_special_cfg_file_for_alfax_IP2(self):
        path_to_cfg = os.path.join(self.path_to_input, "sbsalfax_IP2.out.cfg")
        return path_to_cfg

    def _get_special_cfg_file_for_twiss(self):
        path_to_cfg = os.path.join(self.path_to_input, "StartPoint.twiss.cfg")
        return path_to_cfg

    def _get_special_cfg_file_for_madx(self):
        path_to_cfg = os.path.join(self.path_to_input, "madx_files.cfg")
        return path_to_cfg

    def _break_after_first_run(self):
        return _SHORT_RUN

# END TestOutput -----------------------------------------------------------------------------------


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'TestOutput.testOutput']
    unittest.main()
