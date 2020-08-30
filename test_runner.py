'''Heart of uam.'''

# Andrew Petersen (andrew.petersen@utoronto.ca) 2014
# Anya Tafliovich 2019

# Warning: Heavy use of os means this is probably a linux/unix only solution.
# Note: I considered making the preamble and postamble Python code
# (lambdas) but decided that most operations would be file system
# prep/cleanup best performed in the shell.

# Note: Neither preamble nor postamble are protected by timeouts.

# Note: stdout and stderr in the subprocess calls could be redirected
# for debug support.

import argparse
import importlib
import os
import signal
import sys
import multiprocessing
import subprocess


def execute_tests(student, config):
    '''Run tests for one student.'''

    try:
        os.chdir(student)
    except OSError:
        print('{}: Directory not found.'.format(student), file=sys.stderr)
        return

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

        #env['PYTHONPATH'] = ':'.join(sys.path)
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
    PARSER = argparse.ArgumentParser(
        description='Executes unit tests on student code in each directory.')

    PARSER.add_argument('config', help='Full path of configuration file.')

    ARGS = PARSER.parse_args()

    HEAD, TAIL = os.path.split(ARGS.config)
    sys.path.append(HEAD)
    CONFIG = importlib.import_module(TAIL.split('.')[0])

    def execute(student):
        '''Execute tests for student with ARGS.config as config file.'''

        execute_tests(student, CONFIG)

    with open(CONFIG.students_fname) as fname:

        STUDENT_DIRS = [
            os.sep.join([os.getcwd(), student])
            for student in fname.read().strip().split(os.linesep)]

        PROCS = multiprocessing.Pool(CONFIG.max_processes)

        # Walk directories, executing testcode in each directory.
        PROCS.map(execute, STUDENT_DIRS)
