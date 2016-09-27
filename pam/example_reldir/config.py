import os
import __main__

# ---- TIMEOUT ---- #

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
# Make sure this is >> than the individual test timeouts
#   (see pam.py and utils/defaults.py).
timeout = 100
timeout_operation = lambda: open('timedout', 'w').close()


# ---- STUDENT PROCESSING ---- #

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the directory
#     that contains test_runner.py.
students_fname = os.path.join('directories.txt')

# Auto-detect absolute path to uam.
path_to_uam = os.path.abspath(os.path.dirname(__main__.__file__))

# Auto-detect absolute path to current directory.
grading_dir = os.path.abspath(os.curdir)

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
# -- Notice the use of absolute paths here.
preamble_cmd = ('''cp %s .; cp %s .; cp %s .''' %
                (os.path.join(grading_dir, 'test_asst.py'),
                 os.path.join(grading_dir, 'test_2_asst.py'),
                 os.path.join(grading_dir, 'pep8.py')))

# List of shell commands that execute the tests in a student's
#    submission directory.
# Warning: Some versions of shell don't like the >& redirect, so it's safer
# to redirect stdout and then use 2>&1
# See pam.py for more documentation.
test_cmd = [('%s result.json test_asst.py test_2_asst.py' %
             os.path.join(path_to_uam, 'pam', 'pam.py'))]

# Shell command to be performed after executing tests in a student's submission
#   directory or None.
postamble_cmd = 'rm -rf __pycache__ test_asst.py test_2_asst.py pep8.py'


# ---- AGGREGATION AND TEMPLATING ---- #

# where are the templates? absolute path.
template_dir = os.path.join(path_to_uam, 'templates')
