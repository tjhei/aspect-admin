#!/bin/bash
rm -rf build
mkdir build
cd build
cmake -G "Ninja" ../aspect >/dev/null 2>&1

