import sys

# simple class to help mateASTs function find suitable replacement nodes
class AstElementAddress:
        def __init__(self):
                self.treeIndex = -1
                self.nodeIndex = -1
                self.nodeComplexity = -1

class NodeVisitor(object):
    """Node visitor that populates dict addrs with addresses"""

    def visit(self, node, addrs, treeIndex, nodeIndex, nodeComplexity):
        # create and populate addrElem
        addrElem = AstElementAddress()
        addrElem.treeIndex = treeIndex
        addrElem.nodeIndex = nodeIndex

        # recurse on all children
        for child in node:
            if child is not node:
                nodeIndex = self.visit(child, addrs, treeIndex,
                                       nodeIndex + 1, nodeComplexity)

        # add element to array
        addrElem.nodeComplexity = nodeIndex - addrElem.nodeIndex
        addrs[str(type(node))].append(addrElem)

        # return the node index in the tree
        return nodeIndex

def visit(node, addrs, treeIndex):
    visitor = NodeVisitor()
    visitor.visit(node, addrs, treeIndex, 0, 0)

