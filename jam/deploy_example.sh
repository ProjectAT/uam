# Extracts the example tests and submissions for JAM
# then compiles the tests for use

# NOTE1 : This will overwrite your directories.txt file
# NOTE2 : config.py settings need to be manually adjusted to run the tests:
#         uamdirectory and jamdirectory should be absolute paths to your
#         UAM and JAM installation directories respectively, and in addition
#         the following changes need to be make to JAM specific variables:
#         jamsubmissionsource = "Example/src/"
#         exceptionexplanations = jamdirectory + "exceptionExplanations.xml"
#         jamlibs = jamdirectory + "lib/*"
#         jamtests = jamdirectory + "unittests/"
#         jamtestsuite = "Example.AllTests"
#         jampathtolog = uamdirectory + "runlog.txt"
#
#         See the README for more details.


cp -r example/unittests .
cp -r example/submissions ../
cp example/directories.txt ../directories.txt

./compile_tests.sh unittests/Example example/solution
