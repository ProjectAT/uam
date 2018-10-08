#!/usr/bin/env bash
# Compiles the JAM source code and creates jam.jar

JAMDIR=$(pwd)
COMPILE_CP="-cp .:$JAMDIR/src:$JAMDIR/lib/junit-4.12.jar:$JAMDIR/lib/hamcrest-core-1.3.jar:$JAMDIR/lib/gson-2.3.1.jar"

echo $JAMDIR
echo $COMPILE_CP

javac $COMPILE_CP $(find src | grep ".java")
pushd src
jar cf ../lib/jam.jar `find . | grep .class | grep -v "jam.tests"`
popd
