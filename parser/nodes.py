from enum import Enum

class Node:
    def __init__(self):
        self.expr = ""
        self.parent: Node = None
        # str types refer to variables
        self.left: Node | str = None
        self.right: Node | str = None
        self.type: Operation = None

class Operation(Enum):
    NOT = 0
    AND = 1
    OR = 2
