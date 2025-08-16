from enum import Enum

class Node:
    def __init__(self):
        self.parent: Node = None
        # str types refer to variables
        self.left: Node | str = None
        self.right: Node | str = None
        self.type: Operation = None
        self.var: str | None = None
        self.depth = 0 #number of parents to root

        self.level = 0 #testing maybe delete


class Operation(Enum):
    VAR = 0
    NOT = 1
    AND = 2
    OR = 3
