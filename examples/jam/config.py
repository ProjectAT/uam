##### TIMEOUT #####

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
timeout = 10
timeout_operation = lambda : open("timedout", "w").close()


##### STUDENT PROCESSING #####

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname = "demojam/directories.txt"

# where are the templates?
template_dir = "templates"

##########
# JAM path variables
##########
# Path to the UAM install directory
uamdirectory = "/u/anya/at/uam/"

# Path to the JAM install directory
jamdirectory = "/u/anya/at/uam/jam/"

# Path from submission directory to '/src/' directory containing the packages
# being tested
jamsubmissionsource = "E2soln/src/"

# Path to exception explanations XML file
exceptionexplanations = jamdirectory + "exceptionExplanations.xml"

# Path to jam/lib directory files
jamlibs = jamdirectory + "lib/*"

# Path to JUnit test "root" directory
jamtests = uamdirectory + "demojam/unittests/"

# Path from JUnit test "root" directory to the test suite to be run
jamtestsuite = "E2.e2tester.AllTests"

# Path to runlog.txt logfile
jampathtolog = uamdirectory + "runlog.txt"


# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = None


# List of shell commands that execute the tests in a single directory.
# Warning: Some versions of shell don't like the >& redirect, so it's safer
# to redirect stdout and then use 2>&1
#test_cmd = ["python3 tester.py 2 > 2.results 2>&1", "python3 tester.py 3 > 3.results 2>&1"]
test_cmd = ["cd " + jamsubmissionsource +
            " && javac `find -L . | grep -v '\.svn' | grep '\.java'` > error.txt 2>&1; " + 
            "java -cp " + jamlibs + ":" + jamtests + ":. org.junit.runner.JAMCore " + 
            jamtestsuite + " " + exceptionexplanations + " >> " + jampathtolog + " 2>&1", 
            "cd " + jamsubmissionsource + 
            " && echo \"`date`\nContents of error.txt in `pwd`:\n`cat error.txt`\n\" >> " + 
            jampathtolog]


# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = ("mv " + jamsubmissionsource + "result.json .")
