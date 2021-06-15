#!/usr/bin/python

import os, sys, glob, string, random, optparse, textwrap, parser, badData, ast
from collections import defaultdict
from visitors import swapNodeVisitor
from visitors import printNodeVisitor
from visitors import addressNodeVisitor
from visitors import mutateNodeVisitor
from visitors import getDeclsVisitor
from visitors import nameFizerVisitor
from visitors.scopevisitor import ScopeTreeVisitor
from visitors.scopevisitor import fill_scope_references
from scope import SymbolTable

# verbose mode is global param
VERBOSE = False

# black list of node types not to swap/mate (case insensitive)
blackList = [ r'program', r'identifier' ]

# simple exception class
class globalError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# global default parameters
class globalConfig(object):
    def __init__(self):
        self.inDir = '.'
        self.outDir = '.'
        self.prefix = '_fuzzed_'
        self.popSize = 5
        self.numIters = 2
        self.density = 0.05
        self.mutate = False

def uniquify(l):
    return list(set(l))

# return a randomly selected subset of fully qualified names of files
def getPopulationFiles(config):
    # message
    if VERBOSE:
        print '* Getting population files...'
        print '=' * 80

    rtn = []

    # check the directory exists
    direct = config.inDir
    if not os.path.isdir(direct):
        raise globalError('could not find file directory')

    # get just .js files from directory
    fileNames = glob.glob(os.path.join(direct, '*.js'))
    if len(fileNames) <= 0:
        raise globalError('could not find files in directory')

    # select a number of files with replacment
    i = 0
    while i < config.popSize:
        rtn.append(fileNames[random.randint(0, len(fileNames) - 1)])
        i += 1

    # message
    if VERBOSE:
        print '    - Found %d files' % len(rtn)
        for f in rtn:
            print '        %s' % f

    return rtn

# build ASTs and symbol tables then return an array of root nodes
def buildASTs(fileNames):
    # message
    if VERBOSE:
        print '* building ASTs...'
        print '=' * 80

    # instantiate jsparser
    jsparser = parser.Parser()

    # loop over files and build AST for each
    asts = []
    for i in fileNames:
        if not os.path.isfile(i):
            raise globalError('.js file is not a file')
        else:
            # read file
            jsfile = open(i, 'r')
            jslines = jsfile.read()
            jsfile.close()

            # create AST and add to array
            asts.append(jsparser.parse(jslines))
    return asts

def mateASTs(config, asts):
    # message
    if VERBOSE:
        print '* mating ASTs...'
        print '=' * 80

    # build a dict of arrays of address objects
    arrayIndex = 0
    addrs = defaultdict(list)
    for a in asts:
        addressNodeVisitor.visit(a, addrs, arrayIndex)
        arrayIndex += 1

    # walk asts and construct new trees based on density level
    treeIndex = 0
    for a in asts:
        swapNodeVisitor.visit(a, config.density, addrs, asts, blackList)
        treeIndex += 1

# mutate the asts by cross-pollenation
def mutateASTs(config, asts, density, badStrings, badNums):
    # message
    if VERBOSE:
        print '* mutating ASTs...'
        print '=' * 80

    # walk asts and replace strings and nums with bad values at density
    for a in asts:
        mutateNodeVisitor.visit(a, density, badStrings, badNums)

# fix the semantics by adding symbols were necessary
def fixSemantics(asts):
    # message
    if VERBOSE:
        print '* fizzing semantics of ASTs...'
        print '=' * 80

    # get the dicts of function function and variable declarations
    varDecls = []
    funcDecls = []
    for a in asts:
        getDeclsVisitor.visit(a, funcDecls, varDecls)

    # walk the asts and resolve symbols and fill in where necessary
    for a in asts:
        # fill the symbol tables
        symTable = SymbolTable()
        visitor = ScopeTreeVisitor(symTable)
        visitor.visit(a)

        # fiz up the symbols so they all resolve (add idents, funcs, etc.)
        uvarDecls = []
        ufuncDecls = []
        nameFizerVisitor.visit(a, funcDecls, varDecls, ufuncDecls, uvarDecls)
        ufuncDecls = uniquify(ufuncDecls)
        uvarDecls = uniquify(uvarDecls)

        # add varDecls that didn't resolve to global scope
        for u in ufuncDecls:
            a.addChildNodeFirst(ast.FuncDecl(ast.Identifier(u), None, None))

        # add funcDecls that didn't resolve to global scope
        for u in uvarDecls:
            varStat = ast.VarStatement() # add variable decl statment
            varStat.addChildNode(ast.VarDecl(ast.Identifier(u)))
            a.addChildNodeFirst(varStat)

# write out the ASTs
def emitASTs(fileNames, prefix, outDir, asts):
    # message
    if VERBOSE:
        print '* emitting ASTs to files...'
        print '=' * 80

    # write scripts to files, there is prefix, directory
    arrayIndex = 0
    for a in asts:
        # make file name
        randStr = ''.join(random.choice(string.letters) for i in range(10))
        fname = os.path.join(outDir, randStr + prefix +
                             os.path.basename(fileNames[arrayIndex]))

        try:
            # write file
            f = open(fname, 'w')
            f.write(a.to_ecma())
            f.close()
            arrayIndex += 1
        except:
            print "Error: could not write fuzzed file: %s" % fname

def main():
    config = globalConfig()

    # get cmdline args
    usage = textwrap.dedent("""\
    %prog [-h][-s <int>][-n <int>][-d <density>][-f <dir>][-p <prefix>][-o <dir>][-m]
    """)
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-r', '--seed', action='store', type='int',
                          dest='seed', help="random seed")
    parser.add_option('-s', '--size', action='store', type='int',
                          dest='size', help="population size")
    parser.add_option('-n', '--num', action='store', type='int',
                          dest='num', help="number of iterations")
    parser.add_option('-f', '--files', action='store', type='string',
                          dest='direct', help="directory full of .js files")
    parser.add_option('-d', '--density', action='store', type='float',
                          dest='den', help="density of mutation")
    parser.add_option('-p', '--prefix', action='store', type='string',
                          dest='prefix', help="prefix of output")
    parser.add_option('-o', '--dest', action='store', type='string',
                          dest='dest', help="output directory")
    parser.add_option('-m', '--mutate', action='store_true', dest='mutate',
                          help="mutate strings and nums")
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                          help="verbose logging to stdout")
    (options, args) = parser.parse_args()

    # parse parameters from options and override defaults in config
    if options.size != None:
        config.popSize = options.size

    if options.num != None:
        config.numIters = options.num

    if options.den != None:
        config.density = options.den

    if options.direct != None:
        config.inDir = options.direct

    if options.dest != None:
        config.outDir = options.dest

    if options.prefix != None:
        config.prefix = options.prefix

    if options.mutate != None:
        config.mutate = True

    if options.verbose != None:
        global VERBOSE
        VERBOSE = True

    if options.seed != None:
        random.seed(options.seed)

    # get a population of files from the store
    try:
        fileNames = getPopulationFiles(config)
    except globalError as e:
        print 'Failed to get files:', e.value
        sys.exit(1)

    # build the abstract syntax trees
    try:
        asts = buildASTs(fileNames)
    except globalError as e:
        print 'Failed to build ASTs: ', e.value
        sys.exit(1)

    # mate and mutate the specified number of generations
    i = 0
    while i < config.numIters:
        i += 1

        # file mating is so romantic
        try:
            mateASTs(config, asts)
        except globalError as e:
            print 'Failed to mate ASTs: ', e.value
            sys.exit(1)

        # mutate the numbers and strings TODO: add more mutations
        try:
            if config.mutate:
                mutateASTs(config, asts, config.density,
                           badData.badStrings, badData.badNums)
        except globalError as e:
            print 'Failed to mutate ASTs: ', e.value
            sys.exit(1)

    # fix up the semantics with scope trees
    try:
        fixSemantics(asts)
    except globalError as e:
        print 'Failed to fixup ASTs: ', e.value
        sys.exit(1)

    # write out the abstract syntax trees to files
    try:
        emitASTs(fileNames, config.prefix, config.outDir, asts)
    except globalError as e:
        print 'Failed to emit ASTs: ', e.value
        sys.exit(1)

if __name__  == '__main__':
    main()

sys.exit(0)

