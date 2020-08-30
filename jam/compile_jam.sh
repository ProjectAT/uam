#!/usr/bin/env bash
# Compiles the JAM source code and creates jam.jar

JAMDIR=$(pwd)
COMPILE_CP="-cp .:$JAMDIR/src:$JAMDIR/lib/junit-4.12.jar:$JAMDIR/lib/hamcrest-core-1.3.jar:$JAMDIR/lib/gson-2.8.5.jar:$JAMDIR/lib/commons-cli-1.4.jar"

echo $JAMDIR
echo $COMPILE_CP

javac $COMPILE_CP $(find src | grep ".java")
pushd src
jar cf ../lib/jam.jar `find . | grep .class | grep -v "jam.tests"`
popd
