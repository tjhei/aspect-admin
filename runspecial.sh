#!/bin/bash

USER=$1
URL="https://github.com/$USER/aspect.git"
BRANCH=$2
DESC="$USER-$BRANCH"

if [ -z "$USER" -o -z "$BRANCH" ];
then
 echo "usage: ./runspecial.sh <github-username> <branchname>"
 exit 1
fi

mkdir .lockdir >/dev/null 2>&1
if [ $? -ne 0 ];
then
  echo "Lock is active. Exiting."
  exit 42
fi

echo "welcome to the aspect test script"
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
rmdir .lockdir >/dev/null 2>&1
