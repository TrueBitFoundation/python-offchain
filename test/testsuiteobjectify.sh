#!/bin/bash
cwd=$(pwd)
for file in ./testsuite/*
do
  if [[ $file == *.wast ]]; then
    if [[ $1 == wasm-as ]]; then
      $1 $file
    elif [[ $1 == *wast2wasm ]]; then
      #$1 $file -o $($file:${#file}-5:0)".wasm"
      $1 $file -o $file.wasm
    fi
  fi
done
