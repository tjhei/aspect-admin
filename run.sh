#!/bin/bash

echo "welcome to the auto/aspect-git script"

cd aspect
LASTREV=`git log -1 --format=format:%H`
echo "LASTREV: $LASTREV"

git checkout master -q
git pull -q

REV=$LASTREV
while :
do 

    git checkout master -q
    REV=`git log --format=format:%H | grep $REV -B 1 | head -1 | grep -v $REV`
    if [ -z $REV ]
    then
	break
    fi 
    git checkout $REV -q
    echo "we are now looking at $REV"
    cd ..


    #clang:
    ./setupclang.sh
    cd buildclang
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10
    cd ..

    #g++:
    ./setup.sh
    cd build
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10
    cd ..    

    #g++ & petsc:
    ./setuppetsc.sh
    cd buildpetsc
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10
    cd ..

    cd aspect
done


echo "exiting."