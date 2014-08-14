#!/bin/bash

submit="OFF"
submit="ON"
sha=$1
name=$2

output() {
basepath=$1
build=$2
sha=$3
name=$4
logfile=$1/logs/$3.$2
rm -f $logfile

echo "BUILD $build:"
cd $basepath
./setup-$build.sh
cd build-$build
nice ctest -S ../aspect/tests/run_testsuite.cmake -DDESCRIPTION="$build$name" -Dsubmit=$submit -V -j 10 >$logfile 2>&1
grep "Compiler errors" $logfile
grep "Compiler warnings" $logfile
grep "tests passed" $logfile
}

basepath=`pwd`

build="clang"
output $basepath $build $sha $name

build="gcc"
output $basepath $build $sha $name

build="gccpetsc"
output $basepath $build $sha $name


