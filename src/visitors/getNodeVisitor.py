import sys

class NodeVisitor(object):
    """Node visitor that populates dict addrs with addresses"""

    def visit(self, node, nodeIndex, currentIndex):
        if nodeIndex == currentIndex:
            return -1, node

        # recurse on all children
        for child in node:
            if child is not node:
                currentIndex, obj = self.visit(child, nodeIndex, currentIndex+1)
                if currentIndex == -1:
                    return -1, obj

        # return the node index in the tree
        return currentIndex, None

def visit(node, nodeIndex):
    visitor = NodeVisitor()
    return visitor.visit(node, nodeIndex, 0)

