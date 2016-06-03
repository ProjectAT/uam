# ---- TIMEOUT ---- #

# The maximum number of subprocesses to run at any given time.
max_processes = 5

# The maximum time any subprocess should run, in seconds, and an operation
# to be performed when a timeout occurs.
# Make sure this is >> than the individual test timeouts (see pam.py).
timeout = 10
timeout_operation = lambda: open("timedout", "w").close()


# ---- STUDENT PROCESSING ---- #

# File containing a list of student directories to test.
# -- Each directory should be on its own line.
# -- Each entry should be a relative path from the testing directory.
students_fname = "pam/examples/directories.txt"

# Shell command to be performed before executing tests in a directory or None.
# -- This command will be invoked from within the student's directory!
preamble_cmd = """
    cp '/path_to_uam/pam/examples/test_asst.py' . ;
    cp '/path_to_uam/pam/examples/test_2_asst.py' . ;
    cp '/path_to_uam/pam/examples/pep8.py' .
"""

# List of shell commands that execute the tests in a single directory.
# Warning: Some versions of shell don't like the >& redirect, so it's safer
# to redirect stdout and then use 2>&1
test_cmd = ["'/path_to_uam/pam/pam.py' result.json test_asst.py test_2_asst.py"]

# Shell command to be performed after executing tests in a directory or None.
postamble_cmd = "rm -rf __pycache__ test_asst.py test_2_asst.py pep8.py"


# ---- AGGREGATION AND TEMPLATING ---- #

# where are the templates? absolute path.
template_dir = "/path_to_uam/templates"
