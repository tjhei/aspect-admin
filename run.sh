#!/bin/bash

lockdir=`pwd`/.lockdir
mkdir $lockdir >/dev/null 2>&1
if [ $? -ne 0 ];
then
  echo "Lock is active. Exiting."
  exit 42
fi

echo "welcome to the auto/aspect-git script"

python runner.py run-all

echo "exiting."
rmdir $lockdir >/dev/null 2>&1
