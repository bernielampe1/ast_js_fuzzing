import sys, ast

class NodeVisitor(object):
    """Node visitor that records varDecls and funcDecls identifiers"""

    def visit(self, node, funcDecls, varDecls):
        if type(node) == ast.VarDecl:
            varDecls.append(node.identifier.value)
        elif type(node) == ast.FuncDecl:
            funcDecls.append(node.identifier.value)

        # recurse on all children
        for child in node:
            if child is not node:
                self.visit(child, funcDecls, varDecls)

def visit(node, funcDecls, varDecls):
    visitor = NodeVisitor()
    visitor.visit(node, funcDecls, varDecls)

