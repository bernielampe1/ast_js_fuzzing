* Summary
Language fuzzing is '''hard'''.  To hit the runtime effectively, language fuzzing must create complicated files that are both correct in terms of their syntax and semantics.  Mutation fuzzing doesn't work well for this and, grammar fuzzing takes lots of effort.  This project proposes to build a language fuzzer that works on the AST (abstract syntax trees) in an mutation style.  Example language will be JavaScript.  JavaScript is loosely typed and has lots of interesting uses.  There are 5 board stages envisioned.

Stage 1, parse JS files
Get corpus of input files (mozilla/webkit) and build ASTs of each.
Found a python module called slimit that provides ASTs of JavaScript.  It's not that great, but will totally work for us.

Stage 2, mate files
Swap AST elements between trees that of similar types (i.e. exprs <=> exprs, decls <=> decls, cond <=> cond).

Stage 3, mutate files
Walk new ASTs and replace strings/numbers from bad sets.

Stage 4, semantic fixup
Walk new ASTs and add global vars where missing.  Loop back to stage 1 as necessary.

Stage 5, Emit code from ASTs
Throw and instrument

* To do:
1) The AST representation is not complete.  Some JS files will not parse.
2) The semantic fixups need some work.  Sometimes get an undefined symbol during fuzzed runtime.
3) Sometimes the emit code will run into infinite recursion.

* Example
There is a simple sample program to get you started.  It will lex, parse, walk and print AST and emit code for the simple.js program in samples.  Just run:
  python ./src/printJSast.py ./samples/small.js

* Rhino example, outputs will be in ast_js_fuzzing/src/t
cd astJSFuzz/src
mkdir t
./astJSFuzz.py -s 5 -n 3 -f ../samples/jses/vanilla/ -d 0.05 -o t -m -v

* References
http://packages.python.org/slimit/

