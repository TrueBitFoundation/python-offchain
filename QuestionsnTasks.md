## Questions and Tasks

This document contains the current questions we have and the available tasks if for anybody that wants to pick them up.<br/>

### Questions
List of the questions that need to be answered:<br/>
* Are we going to allow for sys calls inside the code that the interpreter is supposed to run?<br/>
* Are we going to write a linker, assmebler and disassembler?<br/>
* How small should we make the steps? We need to do that so that the single step that's going to be run on-chain fits in with that(we're merklizing the entire state of the machine at a specific time and sending it on-chain.).<br/>

### Tasks
List of the tasks we need done:<br/>

* **TESTS!!** I don't need to yell, I know, but we really do need to write tests. Right now we need to write WAST(web assembly text) or WASM(web assembly binary) test files.<br/>
  * The time estimation for this one is honestly as much as you can spend time on it.<br/>
1. Section decoding: We need the following sections in object files to be decoded and recorded in the memory:<br/>
2. Validation: we need to run the validation tests specified by the WASM document before running the code. For the proof of concept implementation(namely, this one right here), we will be running the validations at the same time that we will be running our parsing so we'll be doing a single pass.<br/>
5. We will need to break down some of the WASM ops into smaller steps so that the Truebit machine can see those state transitions as well. Here's what we mean:<br/>
The WASM `if` instruction pushes an entry onto the control flow stack which contains an unbound label(a label that does not have an index bound to it), the current length of the value stack(the stack where the values are put) and the block signature(think of it as a block return type) then branches if the condition is false. We can break this down into multiple steps using an implicit register machine. Step one will only include the push, and the second step deals with checking the condition and step three will either be a branch or a fall-through(the code is pseudo-ASM):<br/>

  ```ASM

  push $value_stack_length, $block_sinature_type, $unbound_label
  mov %r1, $condition
  jnz $label

  ```
  Values starting with a `$` are labels, palceholders for the real values. `%r1` is one of the registers of the implicit register machine. Do note that these registers are a part of the overall machine state so we will need to add them as leaves to the merkle tree.<br/>

  Here's a list of the actual WASM instructions that are being considered for being run in the implicit register machine:<br/>
  1. `if`
  2. `else`
  3. `end`
  4. `tee_local`
  5. `call_indirect`
  6. all the intetger arithmetic operations
  7. floating-point arithmetic operations
  8. conversion instructions
  9. extending load instructions
  10. wrapping store instructions
  11. `grow_memory`

  * The second family of tasks revolves around writing AST matchers for TBC(Truebit checker) that flag the unnecessary and unwanted features used in the high-level source code.<br/>

  This list is subject to change.<br/>
