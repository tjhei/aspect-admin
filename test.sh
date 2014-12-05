#!/bin/bash

#submit="OFF"
submit="ON"
sha=$1
name=$2

output() {
basepath=$1
build=$2
sha=$3
name=$4
logfile=$basepath/logs/$sha/$build
summary=$basepath/logs/$sha/summary

echo "BUILD $build:" >>$summary
cd $basepath
./setup-$build.sh
cd build-$build
nice ctest -S ../aspect/tests/run_testsuite.cmake -DDESCRIPTION="$build$name" -Dsubmit=$submit -V -j 10 >$logfile 2>&1
grep "Compiler errors" $logfile >>$summary
#grep "Compiler warnings" $logfile >>$summary
#if [ "$build" != "clang" ]
#then
  grep "tests passed" $logfile >>$summary
#fi
}

basepath=`pwd`

mkdir -p $basepath/logs/$sha
rm -f $basepath/logs/$sha/*

build="clang"
output $basepath $build $sha $name

build="gcc"
output $basepath $build $sha $name

build="gccpetsc"
output $basepath $build $sha $name

(
cd $basepath/aspect/doc/ && 
make manual.pdf >/dev/null 2>&1 &&
echo "Manual: OK" || 
echo "Manual: FAILED";
git checkout -f -q -- manual.pdf;
cp manual/manual.log $basepath/logs/$sha/manual.log
) >>$basepath/logs/$sha/summary
 

sed -i 's/\([0-9]*\)% tests passed, 0 tests failed out of \([0-9]*\)/tests: \2 passed/' $basepath/logs/$sha/summary 

sed -i 's/\([0-9]*\)% tests passed, \([0-9]*\) tests failed out of \([0-9]*\)/tests: \2 \/ \3 FAILED/' $basepath/logs/$sha/summary 

cat $basepath/logs/$sha/summary

