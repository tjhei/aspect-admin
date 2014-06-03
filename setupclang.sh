#!/bin/bash
#rm -rf aspect
#svn co https://svn.aspect.dealii.org/trunk/aspect
rm -rf buildclang
mkdir buildclang
cd buildclang

CXX=/ssd/apps/clang+llvm-3.4-x86_64-unknown-ubuntu12.04/bin/clang++ CC=/ssd/apps/clang+llvm-3.4-x86_64-unknown-ubuntu12.04/bin/clang cmake -DDEAL_II_DIR=/ssd/deal-trunk/installedclangas/ .. -G "Ninja" ../aspect >/dev/null 2>&1

