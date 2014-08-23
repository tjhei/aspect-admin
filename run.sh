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

echo "now pull requests"

python runner.py do-pullrequests

echo "copying data"
cp -r logs/* ~/public_html/aspect-logs/
chmod -R a+rX ~/public_html/aspect-logs/

echo "exiting."
rmdir $lockdir >/dev/null 2>&1
