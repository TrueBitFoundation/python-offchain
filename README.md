[![Build Status](https://travis-ci.org/TrueBitFoundation/python-offchain.svg?branch=master)](https://travis-ci.org/TrueBitFoundation/python-offchain)
[![build status](https://ci.appveyor.com/api/projects/status/m47yxdfd60n5pcvb/branch/master?svg=true)](https://ci.appveyor.com/project/TruebitFoundation/tb-wasm-machine-poc/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/TrueBitFoundation/tb-wasm-machine-poc/badge.svg?branch=master)](https://coveralls.io/github/TrueBitFoundation/tb-wasm-machine-poc?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# PyOffchain
PyOffcahin is a Truebit custom WASM interpreter/tool. It has been written to be fairly modular and flexible(at the cost of being slower but speed is not a concern) so it can be used as a wasm python library as well.<br/>

## Status
Right now PyOffchain can:<br/>
run very simple wasm files.<br/>
pretty dump info on the wasm file.<br/>

In the future:<br/>
have a linker.<br/>
have an assembler and a disassembler.<br/>

### Getting PyOffcahin
To clone the repo you should:<br/>
```bash

git clone https://github.com/ronin010011/tb-wasm-machine-poc

```
The submodule is the WASM testsuite. If you are not planning on developing python-offchain you can leave this be otherwise run:<br/>
```bash

git submodule init
git submodule update

```
To get the wasm objects for the testsuite, run the script names `testsuiteobjectify.sh` and pass it the name of the assembler you're using:<br/>
For wabt:<br/>
```bash

./testsuiteobjectify.sh wast2wasm

```

For binaryen:<br/>
```bash
./testsuiteobjectify.sh wasm-as
```

### WASM Pretty Dumps
There are a total of four options that give you pretty dumps of a wasm file:<br/>
* `--sectiondump`: dumps the hex of a section given by its name.<br/>
* `--hexdump`: dumps the whole wasm file in hex format. Expects an integer for the number of bytes to show in each line.<br/>
* `--dbgsection`: dumps a section given by name in a human friendly format.<br/>
* `--dbg`: dumps the whole wasm file in a human friendly format.<br/>
* `--memdump`: dumps the linear memory starting from offset zero til the given address.<br/>
* `--idxspc`: dumps the index space a human friendly format.<br/>

### A Very Simple Stack Machine Interpreter
If this is the first time you are hearing about stack machines, you can check out [a very simple stack machine interpreter](https://github.com/bloodstalker/simpleInterpreter).<br/>
It is a very simple stack machine. You have been warned.<br/>

