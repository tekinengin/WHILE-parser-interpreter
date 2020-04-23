# Programming Languages - Semantic Applications - Natural Semantics (Big Step)

Author: Engin Tekin

requirements: pyinstaller for Makefile purposes

running: type ./test.sh in order to test script. This will create an executable and tests included in test file

WHILE Language - Abstract Syntax Tree - Parser - Interpreter

This script typed for CSE210A-Programming Languages - Semantic Applications

@Following tutorial has been used during preparation of this code. --- #### https://ruslanspivak.com/lsbasi-part7/ ####

There are four main classes AST, LEXER, PARSER, INTERPRETER

AST: Base Class in order to store Abstract-Syntax Tree

LEXER: This class is created to pass through input and tokenize components.

PARSER: Parser is using tokenized input in order to create Abstract-Syntax Tree (AST)

INTERPRETER: This class accepts an AST and evaluate it.

Examples:

x := 10

x := 10 < 0 ? 1 : 0

if true then { x := 10 ; y := ( 20 * 10 - -3 } else skip

while ¬ ( y - -3 = y * z ∨ n * y < 1 * 2 ) do skip 



