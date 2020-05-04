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

import config


# Warning: Some of the exceptions in this code are new to Python 3.3.
def execute_tests(student):
    try:
        os.chdir(student)
    except OSError:
        print('{}: Directory not found.'.format(student), file=sys.stderr)
        return

    # Note: I considered making the preamble and postamble Python code
    # (lambdas) but decided that most operations would be file system
    # prep/cleanup best performed in the shell.

    # Note: Neither preamble nor postamble are protected by timeouts.

    # Note: stdout and stderr in the subprocess calls could be redirected
    # for debug support.

    if config.preamble_cmd:
        try:
            subprocess.check_call(config.preamble_cmd,
                                  stdout=None, stderr=None, shell=True)
        except subprocess.CalledProcessError as cpe:
            print('{}: Preamble terminated abnormally: {}'.format(student, cpe),
                  file=sys.stderr)
            return

    # Note: Not using check_call since we need the PID in order to kill all
    # descendents of the process.
    for cmd in config.test_cmd:
        env = os.environ.copy()
        env['PYTHONPATH'] = ':'.join(sys.path)
        proc = subprocess.Popen(
            cmd, start_new_session=True, shell=True, env=env)
        try:
            proc.communicate(timeout=config.timeout)
        except subprocess.TimeoutExpired:
            config.timeout_operation()
            try:
                os.killpg(proc.pid, signal.SIGTERM)
            except os.ProcessLookupError:
                pass  # the process terminated after the timeout was generated
        if proc.returncode != 0:
            print('{}: Test terminated abnormally'.format(student),
                  file=sys.stderr)

    if config.postamble_cmd:
        try:
            subprocess.check_call(config.postamble_cmd,
                                  stdout=None, stderr=None, shell=True)
        except subprocess.CalledProcessError as cpe:
            print('{}: Postamble terminated abnormally'.format(
                student), file=sys.stderr)
            return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Executes unit tests on student code in each directory.')

    # For testing on a subset of student directories.
    parser.add_argument(
        'students_fname', nargs='?',
        default=config.students_fname,
        help='File containing a list of student directories to test.')

    args = parser.parse_args()

    # Configuration and setup
    cwd = os.getcwd()
    student_dirs = [
        os.sep.join([cwd, student])
        for student in open(args.students_fname).read().strip().split(os.linesep)]

    procs = multiprocessing.Pool(config.max_processes)

    # Walk directories, executing testcode in each directory.
    procs.map(execute_tests, student_dirs)
