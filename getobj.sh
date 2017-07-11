#!/bin/bash

"wasm-as" $1 -o obj
"xxd" obj > objhex
cat objhex| gawk 'BEGIN{FS=":"}{print $2}' | gawk 'BEGIN{FS="  "}{print $1}' > $1".bytecode"
rm objhex obj
