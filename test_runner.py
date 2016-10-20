#!/usr/bin/env python3

# Andrew Petersen (andrew.petersen@utoronto.ca)
# May 8, 2014

# Warning: Heavy use of os means this is probably a linux/unix only solution.
import os
import signal
import sys
import multiprocessing
import subprocess

import argparse

# Warning: Some of the exceptions in this code are new to Python 3.3.
def execute_tests(student):
    try:
        os.chdir(student)
    except OSError:
        print("%s: Directory not found" % student, file=sys.stderr)
        return

    # Note: I considered making the preamble and postamble Python code
    # (lambdas) but decided that most operations would be file system
    # prep/cleanup best performed in the shell. 

    # Note: Neither preamble nor postamble are protected by timeouts.

    # Note: stdout and stderr in the subprocess calls could be redirected
    # for debug support.

    if config.preamble_cmd:
        try:
            subprocess.check_call(config.preamble_cmd, stdout=None, stderr=None, shell=True)
        except subprocess.CalledProcessError as cpe:
            print("{0}: Preamble terminated abnormally".format(student), file=sys.stderr)
            return

    # Note: Not using check_call since we need the PID in order to kill all
    # descendents of the process. 
    for cmd in config.test_cmd:
        env = os.environ.copy()
        env['PYTHONPATH'] = ":".join(sys.path)
        proc = subprocess.Popen(cmd, start_new_session=True, shell=True, env=env)
        try:
            stdout_data, stderr_data = proc.communicate(timeout=config.timeout)
        except subprocess.TimeoutExpired:
            config.timeout_operation()
            try:
                os.killpg(proc.pid, signal.SIGTERM)   
            except os.ProcessLookupError:
                pass  # the process terminated after the timeout was generated
        if proc.returncode != 0:
            print("{0}: Test terminated abnormally".format(student), file=sys.stderr)
        
    if config.postamble_cmd:
        try:
            subprocess.check_call(config.postamble_cmd, stdout=None, stderr=None, shell=True)
        except subprocess.CalledProcessError as cpe:
            print("{0}: Postamble terminated abnormally".format(student), file=sys.stderr)
            return

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(
        description='Executes unit tests on student code in each directory.')

    # For testing on a subset of student directories.
    parser.add_argument(
        "students_fname", nargs="?",
        default=None,
        help="File containing a list of student directories to test.")

    parser.add_argument('--confdir', nargs='+', default='.',
                        help='Directory containing config.py.')

    args = parser.parse_args()

    # Import config file from current directory as a last resort.
    sys.path.append(args.confdir)

    # Test to see if config works; abort with error if it does not.
    try:
        import config
    except ImportError as exception:
        sys.stderr.write('Unable to import config.py.\n')
        sys.exit(1)

    # Switch to config directory so that paths in config file, if specified relatively,
    # still work.
    os.chdir(args.confdir)

    # Populate default value for list of student directories to test.
    if args.students_fname == None:
        args.students_fname = config.students_fname

    # Configuration and setup
    cwd = os.getcwd()
    student_dirs = \
        [os.sep.join([cwd, student])
         for student in
         open(args.students_fname).read().strip().split(os.linesep)]

    procs = multiprocessing.Pool(config.max_processes)

    # Walk directories, executing testcode in each directory
    procs.map(execute_tests, student_dirs)
