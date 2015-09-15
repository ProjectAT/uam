# Andrew Petersen (andrew.petersen@utoronto.ca)
# May 8, 2014

import os
import sys
import multiprocessing
import subprocess
import argparse
import config


# Warning: Some of the exceptions in this code are new to Python 3.3.
def execute_tests(student):
    try:
        os.chdir(student)
    except OSError:
        print("%s: Directory not found" % student, file=sys.stderr)
        return

    # Note1: I considered making the preamble and postamble Python code
    # (lambdas) but decided that most operations would be file system
    # prep/cleanup best performed in the shell.

    # Note2: Neither preamble nor postamble are protected by timeouts.

    # Note3: stdout and stderr in the subprocess calls could be redirected
    # for debug support.

    if config.preamble_cmd:
        try:
            subprocess.check_call(config.preamble_cmd,
                                  stdout=None, stderr=None,
                                  shell=True)
        except subprocess.CalledProcessError as cpe:
            print("%s: Preamble terminated with exit code %d" %
                  (student, cpe.returncode), file=sys.stderr)
            return

    for cmd in config.test_cmd:
        try:
            subprocess.check_call(cmd, shell=True, timeout=config.timeout)
        except subprocess.CalledProcessError as cpe:
            print("%s: Test '%s' terminated with exit code %d" %
                  (student, cmd, cpe.returncode), file=sys.stderr)
        except subprocess.TimeoutExpired:
            config.timeout_operation()

    if config.postamble_cmd:
        try:
            subprocess.check_call(config.postamble_cmd,
                                  stdout=None, stderr=None,
                                  shell=True)
        except subprocess.CalledProcessError as cpe:
            print("%s: Postamble terminated with exit code %d" %
                  (student, cpe.returncode), file=sys.stderr)
            return


if __name__ == "__main__":
    # Arguments #
    parser = argparse.ArgumentParser(
        description='Executes unit tests on student code in each directory.')

    # For testing on a subset of student directories.
    parser.add_argument(
        "students_fname", nargs="?",
        default=config.students_fname,
        help="File containing a list of student directories to test.")

    args = parser.parse_args()

    # Configuration and setup #
    cwd = os.getcwd()
    student_dirs = \
        [os.sep.join([cwd, student])
         for student in
         open(args.students_fname).read().strip().split(os.linesep)]

    procs = multiprocessing.Pool(config.max_processes)

    # Walk directories, executing testcode in each directory #
    procs.map(execute_tests, student_dirs)
