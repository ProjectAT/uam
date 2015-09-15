Example README

The example contained within this directory provides the set up for the
unittests, solution and submissions folders, as well the directories.txt file
for the automarking of a single Java package with 3 student submissions.

In the parent directory of this directory, the deploy_example.sh shell script
will appropriately extract this example for testing, and compile the provided
unittests. The default JAM specific paths and commands provided for 'uam' in
the 'config.py' file will test the example submissions.

For reference, the JAM specific variable settings in config.py for testing this
example should be as follows:
jamsubmissionsource = "Example/src/"
jamlibs = "../../../../jam/lib/*"
jamtests = "../../../../jam/unittests/"
jamtestsuite = "Example.AllTests"

Additionally, please note that the 'directories.txt' file in the 'uam' directory
will be overwritten when this example is extracted.
