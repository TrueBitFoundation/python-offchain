[![Build Status](https://travis-ci.org/TrueBitFoundation/tb-wasm-machine-poc.svg?branch=master)](https://travis-ci.org/TrueBitFoundation/tb-wasm-machine-poc)
[![build status](https://ci.appveyor.com/api/projects/status/m47yxdfd60n5pcvb/branch/master?svg=true)](https://ci.appveyor.com/project/TruebitFoundation/tb-wasm-machine-poc/branch/master)
[![Coverage Status](https://coveralls.io/repos/github/TrueBitFoundation/tb-wasm-machine-poc/badge.svg?branch=master)](https://coveralls.io/github/TrueBitFoundation/tb-wasm-machine-poc?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

DEPRECATED in favor of [ocaml-offchain](https://github.com/TrueBitFoundation/ocaml-offchain)

# tb-wasm-machine-poc
PoC for process virtual machine to interpret WASM binaries within the context of the TB verification game and it's particular constraints

For a list of currently available tasks or questions/challenges we are facing, please take a look at `QuestionsnTasks.md`.<br/>
For a description of the files and directories along with requirements on having your pull-request reviewed, please look at `Contributions.md`.<br/>

### Building
To clone the repo you should:<br/>
```bash

git clone https://github.com/ronin010011/tb-wasm-machine-poc

```
To initialize and clone the submodules:<br/>
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

For instructions on building `TBC`, please look at the respective readme under `TBC`'s directory.<br/>

### Tools
Just what the name says:
* [binaryen](https://github.com/WebAssembly/binaryen)<br/>
* [wabt](https://github.com/WebAssembly/wabt)<br/>
* [wasmfiddle](https://wasdk.github.io/WasmFiddle/)<br/>

### Running the Sample
To be able to run the code as it is right now, you need to get the binary. I'm using [binaryen](https://github.com/WebAssembly/binaryen).<br/>
Our implementation will not run on python2.x.<br/>

To run the interpreter you should call:<br/>
```bash

python3 argparser.py --wasm ./injected.wasm

```

To see the other options available run help.<br/>
