import os

# ---- TIMEOUT ---- #

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
# Make sure this is >> than the individual test timeouts
#   (see pam.py and utils/defaults.py).
timeout = 100


def timeout_operation(): return open('timedout', 'w').close()


# ---- STUDENT PROCESSING ---- #

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the directory
#     that contains test_runner.py.
students_fname = os.path.join('jam', 'examples', 'directories.txt')

# absolute path to uam
uam_dir = '/home/anya/at'  # 'YOUR_PATH_TO_UAM'

# path to jam
jam_dir = os.path.join(uam_dir, 'jam')

# Where are the JAM tests?
test_dir = os.path.join(jam_dir, 'examples', 'tests')

# JAM libraries portion of the Java path
jam_libs = (':'.join(os.path.join(jam_dir, 'lib', lib)
                     for lib in ('jam.jar', 'junit-4.12.jar',
                                 'hamcrest-core-1.3.jar', 'gson-2.8.5.jar')))

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
# -- Use of absolute paths here.
preamble_cmd = None

test_cmd = ['javac a1soln/*.java',
            'java -cp .:%s:%s org.junit.runner.JAMCore a1tester.AllTests' % (jam_libs, test_dir)]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = None

# ---- AGGREGATION AND TEMPLATING ---- #

# where are the templates? absolute path.
template_dir = os.path.join(uam_dir, 'templates')
