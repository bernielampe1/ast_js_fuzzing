#!/usr/bin/python

import os, sys
import parser
from visitors import printNodeVisitor

# check args
if len(sys.argv) != 2:
    print 'printJSast.py <file.js>'
    sys.exit(1)

# read a js file
jsfile = open(sys.argv[1], 'r')
jslines = jsfile.read()
jsfile.close()

# parse the file with slimit
jsparser = parser.Parser()
tree = jsparser.parse(jslines)

# walk the tree nodes with print visitor
print '\n* AST from JS program file: ' + sys.argv[1]
print '=' * 80
printNodeVisitor.visit(tree)

# walk the tree with ecma visitor
print '\n* Emitted code from JS program file: ' + sys.argv[1]
print '=' * 80
print tree.to_ecma()

sys.exit(0)

