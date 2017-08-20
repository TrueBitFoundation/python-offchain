## Contributations

### Structure
This section introduces the various files and directories inside the repository:<br/>
* `argparser.py` holds the main body of the interpreter.<br/>
* `Contributations.md` is the current document you're viewing.<br/>
* `c-samples` holds some simple C code and its equivalent WASM text format<br/>
* `getobj.sh` was used to the hex byte-code from the object file. deprecated.<br/>
* `injected.wasm` is an object file used for testing.<br/>
* `injected.wast` is the WASM text representation of the same test file.<br/>
* `QuestionnTasks.md` holds the current tasks that need to be done and the current questions/challenges that we are facing.<br/>
* `README.md` is the readme. You should first read that.<br/>
* `TBInit.py` is the file that holds the containers for the Trueit Interpreter's internal state.<br/>
* `OpCodes.py` is the file that contains the OpCodes for the WASM instructions.<br/>
* `utils.py` is the file that holds methods and classes that are used across multiple files<br/>
* `test` holds the tests.<br/>
* `TBC` the directory holds the checker that enforces the conditions on the high-level source code that is going to run by the interpreter.<br/>

### Contribution
Below you will find requirements for adding a pull request. Submissions that don't meet the requirements will not be reviewed:<br/>
* PEP-8: use it. In case a PEP-8 guideline is irrational in a certain case, use your judgement.<br/>
* Your pull request must be accompanied by a test file. Your test file must be able to run on its own and by another python module. Inherit from `Void_Spwner`. Your test script should not break the regression test script.<br/>
* Python 2 compatibility is not a requirement.<br/>
* Don't forget to add your name to `CONTRIBUTERS.txt`. The list is kept in a chronological order.<br/>
