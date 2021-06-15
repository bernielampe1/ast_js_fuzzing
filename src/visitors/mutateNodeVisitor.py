import sys, random, ast

class NodeVisitor(object):
    """Node visitor that will replace values in nums and strings"""

    def visit(self, node, density, badStrings, badNums):
        if isinstance(node, ast.String) and random.random() < density:
            node.value = '"' + random.choice(badStrings) + '"'

        if isinstance(node, ast.Number) and random.random() < density:
            node.value = random.choice(badNums)

        for child in node:
            if child is not node:
                self.visit(child, density, badStrings, badNums)


def visit(node, density, badStrings, badNums):
    visitor = NodeVisitor()
    visitor.visit(node, density, badStrings, badNums)

