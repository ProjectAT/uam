"""Example configuration file for jam."""

import os

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 100


def timeout_operation(): return open("timedout", "w").close()


# file containing a list of student directories to test
students_fname = os.path.join('jam', 'examples', 'directories.txt')

# absolute path to uam
uam_dir = '/home/anya/at'  # 'YOUR_PATH_TO_UAM'

# where are the templates?
template_dir = os.path.join(uam_dir, 'templates')

# path to jam
jam_dir = os.path.join(uam_dir, 'jam')

# Where are the JAM tests?
test_dir = os.path.join(jam_dir, 'examples', 'tests')

# JAM libraries portion of the Java path
jam_libs = ':'.join(os.path.join(jam_dir, 'lib', lib)
                    for lib in ('jam.jar', 'junit-4.12.jar',
                                'hamcrest-core-1.3.jar', 'gson-2.8.5.jar'))

# Path to exception explanations XML file
exceptionexplanations = os.path.join(jam_dir, "exceptionExplanations.xml")

# Path to runlog.txt logfile
jampathtolog = os.path.join(uam_dir, "runlog.txt")

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = None

# List of shell commands that execute the tests in a single directory.
compile_cmd = 'javac -cp {}:{}:. a1tester/*.java'.format(jam_libs, test_dir)
run_cmd = 'java -cp .:{}:{} org.junit.runner.JAMCore a1tester.AllTests {}'.format(
    jam_libs, test_dir, exceptionexplanations)
test_cmd = [compile_cmd, run_cmd]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = None
