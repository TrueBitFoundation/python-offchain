## TBC - Truebit Checker

The current implementation will only flag unwanted and unnecessary high-level contructs for the C-family of languages.<br/>

### Building
You need to have the LLVM libraries installed. TBC will use the same options that were used to build your LLVM libraries to build TBC so your `llvm-config` should exist and be in path.<br/>

If your `llvm-config` and `clang++` have a different name, e.g. `llvm-config-4.0` and `clang++-4.0`, pass the names to the makefile like this:<br/>

```bash

make CXX=clang++-4.0 LLVM-CONF=llvm-config-4.0

```
You can also use `g++` to build TBC, in which case just add `CXX=g++` after the make command.<br/>

### Running
If you have a compilation database then just pass the name of the file to TBC:<br/>
```bash

./TBC myfile.cpp

```

if you don't have a compilation database either consider getting one(either use CMake or [Bear](https://github.com/rizsotto/Bear)) or just pass all your options like this:<br/>
```bash

./TBC myfile.cpp -- -std=c++11

```
