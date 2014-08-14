#!/bin/bash
DIR=build-gcc
rm -rf $DIR
mkdir $DIR
cd $DIR
cmake -G "Ninja" ../aspect >/dev/null 2>&1

