from enum import Enum

class Node:
    def __init__(self):
        self.parent: Node = None
        # str types refer to variables
        self.left: Node | str = None
        self.right: Node | str = None
        self.type: Operation = None
        self.depth = 0

        self.children = (self.left, self.right)

    def update(self):
        self.children = (self.left, self.right)

    def get_level(self):
        child_levels = [] #left to right children levels?
        for child in self.children:
            if child.type == str:
                child_levels.append(0)

        level = 1 + max(child_levels)
        return level



class Operation(Enum):
    VAR = 0
    NOT = 1
    AND = 2
    OR = 3
