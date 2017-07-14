# tb-wasm-machine-poc
PoC for process virtual machine to interpret WASM binaries within the context of the TB verification game and it's particular constraints

### Running the Sample
To be able to run the code as it is right now, you need to get the binary. I'm using [binaryen](https://github.com/WebAssembly/binaryen).<br/>
Our implementation will not run on python2.x.<br/>

To run the interpreter you should call:<br/>
```bash

python3 argparser.py --wasm ./injected.wasm

```
