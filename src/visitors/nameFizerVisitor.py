import sys, ast

def checkList(l, value):
    for i in l:
        if value in i:
            return True

    return False

class NodeVisitor(object):
    """Visitor tries to resolve identifiers, if failed, return info"""

    def visit(self, node, funcDecls, varDecls, ufuncDecls, uvarDecls):
        if type(node) == ast.Identifier and hasattr(node, 'scope'):
            # try to resolve symbol in this scope chain
            symbol = node.scope.resolve(node.value)
            if symbol is None:
                # check the list of all decls
                if checkList(funcDecls, node.value):
                    ufuncDecls.append(node.value)
                elif checkList(varDecls, node.value):
                    uvarDecls.append(node.value)

        # recurse on all children
        for child in node:
            if child is not node:
                self.visit(child, funcDecls, varDecls, ufuncDecls, uvarDecls)

def visit(node, funcDecls, varDecls, ufuncDecls, uvarDecls):
    visitor = NodeVisitor()
    visitor.visit(node, funcDecls, varDecls, ufuncDecls, uvarDecls)

