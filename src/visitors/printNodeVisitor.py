import sys

class NodeVisitor(object):
    """Simple node visitor with level annotation."""

    def visit(self, node, level):
        print "  " * level + "level: %d, %s" % (level, str(node))
        for child in node:
            if child is not node:
                self.visit(child, level+1)


def visit(node):
    visitor = NodeVisitor()
    visitor.visit(node, 0)

