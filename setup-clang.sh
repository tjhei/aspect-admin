#!/bin/bash
DIR=build-clang
rm -rf $DIR
mkdir $DIR
cd $DIR

CXX=/ssd/apps/clang+llvm-3.4-x86_64-unknown-ubuntu12.04/bin/clang++ CC=/ssd/apps/clang+llvm-3.4-x86_64-unknown-ubuntu12.04/bin/clang cmake -DDEAL_II_DIR=/ssd/deal-build/installedclangas/ .. -G "Ninja" ../aspect >/dev/null 2>&1

