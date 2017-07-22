## Questions and Tasks

This document contains the current questions we have and the available tasks if for anybody that wants to pick them up.<br/>

### Questions
List of the questions that need to be answered:<br/>
* Where are we getting our wasm(Web Assembly Object) files from? different sources can use different encodings to cut down code-size or execution time.<br/>
* `binaryen` encodes `varuint32` values to one byte when need be, but when the size is bigger, it uses more than one byte. How can the interpreter know that?<br/>
* For the validation checks, why would we want to run a "naive" parser first(to just run the validations) in contrast to running the tests at the same time as parsing the object file? In other words why single-pass versus multi-pass?<br/>

### Tasks
List of the tasks we need done:<br/>

* **TESTS!!** I don't need to yell, I know, but we really do need to write tests. Right now we need to write WAST(web assembly text) or WASM(web assembly binary) test files.<br/>
  * The time estimation for this one is honestly as much as you can spend time on it.<br/>
* Section decoding: We need the following sections in object files to be decoded and recorded in the memory:<br/>
  * Type Section
  * Import Section
  * Function Section
  * Table
  * Memory Section
  * Global Section
  * Export Section
  * Start Section
  * Element Section
  * Data Section
  * The time estimation for this one is one day per section.<br/>
* Validation: we need to run the validation tests specified by the WASM document before running the code. For the proof of concept implementation(namely, this one right here), we will be running the validations at the same time that we will be running our parsing so we'll be doing a single pass.<br/>
* A signed LEB128 encoder. Time estimation is a couple of hours.<br/>
* An unsigned LEB128 encoder. Time estimation is a couple of hours.<br/>
* We will need to break down some of the WASM ops into smaller steps so that the Truebit machine can see those state transitions as well. Here's what we mean:<br/>
The WASM `if` instruction pushes an entry onto the control flow stack which contains an unbound label, the current length of the value stack and the block signature then branches if the condition is false. We can break this down into multiple steps using an implicit register machine. Step one will only include the push, and the second step deals with checking the condition and step three will either be a branch or a fall-through:<br/>

  ```

  push $value_stack_length, $block_sinature_type, $unbound_label
  move %r1, $condition
  jnz $label

  ```
  Values starting with a `$` are labels, palceholders for the real values. `%r1` is one of the registers of the implicit register machine. Do note that these registers are a part of the overall machine state so we will need to add them as leaves to the merkle tree.<br/>
