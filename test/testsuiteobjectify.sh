#!/bin/bash
cwd=$(pwd)
for file in ./testsuite/*
do
  if [[ $file == *.wast ]]; then
    $1 $file
  fi
done
