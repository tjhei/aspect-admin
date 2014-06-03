#!/bin/bash

echo "welcome to the aspect test script"

USER=$1
URL="https://github.com/$USER/aspect.git"
BRANCH=$2
DESC="$USER-$BRANCH"

echo "checking $URL $BRANCH"

cd aspect
LASTREV=`git log -1 --format=format:%H`
echo "LASTREV: $LASTREV"

git fetch $URL $BRANCH -q || exit -2
git checkout FETCH_HEAD -q || exit -1
cd ..

    #clang:
    ./setupclang.sh
    cd buildclang
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10 -DDESCRIPTION="$DESC"
    cd ..

    #g++:
    ./setup.sh
    cd build
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10 -DDESCRIPTION="$DESC"
    cd ..    

    #g++ & petsc:
    ./setuppetsc.sh
    cd buildpetsc
    nice ctest -S ../aspect/tests/run_testsuite.cmake -Dsubmit=ON -V -j 10 -DDESCRIPTION="$DESC"
    cd ..

cd aspect
git checkout master -q
echo "going back to $LASTREV..."
git checkout $LASTREV

echo "exiting."