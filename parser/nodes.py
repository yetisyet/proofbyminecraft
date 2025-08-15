class Node:
    
    def __init__(self):
        self.expr = ""
        self.parent: Node = None
        # str types refer to variables
        self.left: Node | str = None
        self.right: Node | str = None