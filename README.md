# tb-wasm-machine-poc
PoC for process virtual machine to interpret WASM binaries within the context of the TB verification game and it's particular constraints

For a list of currently available tasks or questions/challenges we are facing, please take a look at `QuestionsnTasks.md`.<br/>
For a description of the files and directories along with requirements on having your pull-request reviewed, please look at `Contributions.md`.<br/>


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
