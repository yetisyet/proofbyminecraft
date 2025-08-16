from enum import Enum

class Node:
    def __init__(self):
        self.expr = ""
        self.parent: Node = None
        # str types refer to variables
        self.left: Node | str = None
        self.right: Node | str = None
        self.type: Operation = None
        self.depth = 0

    def get_level(self):
        if self.left == None and self.right == None:
            return 0
        else:
            return 1 + max(self.get_level(self.left), self.get_level(self.right))



class Operation(Enum):
    VAR = 0
    NOT = 1
    AND = 2
    OR = 3
