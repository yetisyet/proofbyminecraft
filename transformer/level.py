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


def GetLevel(Node):

    """should returns the level of the node

        level(node) = 1 + max(level(childs))

         L=2    ^
              /   |
         L=1 v     v
            / \   / |
      L=0  a  b  a   c
    """

    child_levels = [] #levels of the children
    if Node.left == str:
        child_levels.append(0)
    elif Node.right == str:
        child_levels. append(0)
    else:
        child_levels.append(GetLevel(Node.left))
        child_levels.append(GetLevel(Node.right))

    Node.level = 1 + max(child_levels)
    return Node.level




