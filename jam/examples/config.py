import os

##### TIMEOUT #####

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs. To make sense, this should be >>
# your individual test timeouts.
timeout = 10
timeout_operation = lambda : open('timedout', 'w').close()

##### STUDENT PROCESSING #####

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname ='jam/examples/directories.txt'

# Where is uam on your machine?
#uam_dir = '/YOUR_PATH_TO_UAM'
uam_dir = '/home/anya/at/uam'

# path to jam
jam_dir = os.path.join(uam_dir, 'jam')

# Where are the Jam tests?
test_dir = os.path.join(jam_dir, 'examples', 'tests')

# JAM libraries portion of the Java path
jam_libs = (':'.join(os.path.join(jam_dir, 'lib', lib)
                     for lib in ('jam.jar', 'junit-4.12.jar',
                                 'hamcrest-core-1.3.jar', 'gson-2.3.1.jar')))

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = None

test_cmd = ['javac e2soln/*.java',
            'java -cp .:%s:%s org.junit.runner.JAMCore e2tester.AllTests' % (jam_libs, test_dir)]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = 'ln -s result.json ../../../result.json'

# where are the templates?
template_dir = 'templates'

