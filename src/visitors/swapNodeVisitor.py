import sys, random
from visitors import addressNodeVisitor
from visitors import getNodeVisitor
from collections import defaultdict

def checkBlackList(nodeStr, blackList):
    for i in blackList:
        if i.lower() in nodeStr.lower():
            return True
    return False

class NodeVisitor(object):
    """Node visitor that randomly swaps nodes between asts"""

    def visit(self, node, density, addrs, asts, blackList):
        # check black list, ensure that are other nodes and flip a coin
        typeStr = str(type(node))
        if (not checkBlackList(typeStr, blackList) and
            len(addrs[typeStr]) > 1 and random.random() < density):

            # choose a node from the list randomly
            address = random.choice(addrs[typeStr])
            treeIndex = address.treeIndex
            nodeIndex = address.nodeIndex

            # swap a node
            nodeIndex, tmpNode = getNodeVisitor.visit(asts[treeIndex],nodeIndex)
            if tmpNode is not None and node is not tmpNode:
                # swap the node contents and children lists
                if type(node) == list:
                    node, tmpNode = tmpNode, node
                else: # AST object
                    node.swap(tmpNode)

                # recompute addresses
                arrayIndex = 0
                addrs.clear() # WARNING: must be a clear (do not change address)
                for a in asts:
                    addressNodeVisitor.visit(a, addrs, arrayIndex)
                    arrayIndex += 1

        # recurse on all children
        for child in node:
            if child is not node:
                self.visit(child, density, addrs, asts, blackList)

def visit(node, density, addrs, asts, blackList):
    visitor = NodeVisitor()
    visitor.visit(node, density, addrs, asts, blackList)

