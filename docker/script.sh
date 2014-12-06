#!/bin/bash

echo "ASPECT testing - hello from script.sh"
if [ -f /aspect-tester/runner.py ];
then
       cd /aspect-tester; python runner.py "$@"
else
       echo "please mount /aspect-tester"
fi
