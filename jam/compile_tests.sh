# Compiles a JUnit test suite with JAM included in the class path
# Usage: ./compile_tests.sh unittestdirectory solutiondirectorywithpackages
# TODO: Document me.

if [ $# -ne 2 ]; then
    echo Usage: $0 unittestdir solutionwithpackagesdir
    exit 1
fi


UNITTEST_DIR=$1
SOLUTION_DIR=$2
JAMDIR=$(pwd)
COMPILE_CP="-cp .:$JAMDIR/lib/jam.jar:$JAMDIR/lib/junit-4.12.jar:$JAMDIR/lib/hamcrest-core-1.3.jar:$JAMDIR/lib/gson-2.3.1.jar:$UNITTESTDIR:$SOLUTION_DIR"

cd $1
javac -Xlint:unchecked $COMPILE_CP *.java
