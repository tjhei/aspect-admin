#!/bin/bash
DIR=build-gccpetsc
rm -rf $DIR
mkdir $DIR
cd $DIR

cmake -G "Ninja" -D ASPECT_USE_PETSC=ON ../aspect >/dev/null 2>&1

