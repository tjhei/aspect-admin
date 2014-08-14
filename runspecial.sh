#!/bin/bash

USERBRANCH=$1

if [ -z "$USERBRANCH" ];
then
 python runner.py pullrequests
 echo "RUN WITH: ./runspecial.sh user/repo:branch"
 exit 0
fi

echo "checking $USERBRANCH"

lockdir=`pwd`/.lockdir
mkdir $lockdir >/dev/null 2>&1
if [ $? -ne 0 ];
then
  echo "Lock is active. Exiting."
  exit 42
fi

python runner.py test $USERBRANCH


rmdir $lockdir >/dev/null 2>&1
