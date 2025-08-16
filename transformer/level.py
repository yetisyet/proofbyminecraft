from parser.nodes import *
from parser.parser import *

#assigns every gate level number

# class Node:
#     def __init__(self):
#         self.parent: Node = None
#         # str types refer to variables
#         self.left: Node | str = None
#         self.right: Node | str = None
#         self.type: Operation = None
#         self.depth = 0


def GetLevel(node):

    """should returns the level of the node

        0 level is furthest left and then higher level means more right

        Level
        -------------------->
        _______________
        0 | 1 | 2 | ...
        a | ^ | v |
        b | ^ |   |
        a |   |   |
        c |   |   |
        ---------------


        level(node) = 1 + max(level(childs))

         (a^b)v(a^c)
         L=2    v
              /   |
         L=1 ^     ^
            / |   / |
      L=0  a  b  a   c
    """

    child_level = [] #levels of the children
    if node is None: #base case?
        return 0

    if node.type == Operation.VAR: #if it variable then return 0
        return 0
    if node.left:
        child_level.append(GetLevel(node.left)) # get level left child
    if node.right:
        child_level.append(GetLevel(node.right)) # get level right child

    node.level = 1 + max(child_level)
    return node.level




