#!/usr/bin/env bash
# Compiles a Jam test suite with JAM included in the class path.
# Usage: ./compile_tests.sh unittestdir solutiondir
# unittestdir -- (an absolute path to) a directory that contains Jam test files (.java files)
# solutiondir -- (an absolute path to) a directory with instructor solutions/stubs
#    (a directory that contains solution packages)

if [ $# -ne 2 ]; then
    echo Usage: $0 unittestdir solutiondir
    exit 1
fi

UNITTEST_DIR=$1
SOLUTION_DIR=$2
JAMDIR=$(pwd)
COMPILE_CP="-cp .:$JAMDIR/lib/jam.jar:$JAMDIR/lib/junit-4.12.jar:$JAMDIR/lib/hamcrest-core-1.3.jar:$JAMDIR/lib/gson-2.3.1.jar:$SOLUTION_DIR"

pushd $1
javac -Xlint:unchecked $COMPILE_CP *.java
popd
