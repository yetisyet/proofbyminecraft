from __future__ import annotations
from nodes import Node, Operation

class FOLe:

    operators = ('^','v','~') # the three logic operators

    def __init__(self, expr):
        body = expr
        pass
    
    # def BracketBlock(str):
    #     # <str> should be fully wrapped around a single bracketing
        
    #     out = []
    #     l_brackets = []

    #     # Create substrings index tuples of each bracketing
    #     for i in range(len(str)):
    #         if str[i] == "(":
    #             l_brackets.append(i)
    #         elif str[i] == ")":
    #             out.append((l_brackets.pop()+1, i))

    #     return out
    
    # def CreateGraph(bracketings, str):
    #     for bracketing in bracketings:
    #         cur = str[bracketing[0]:bracketing[1]]

    #         if "(" not in cur and ")" not in cur:
    #             # Bracketing is bottom level

    def BracketNots(expr: str) -> str:
        """
        Ensure each not operation is bracketed, unless it is the top
        level operation
        """

        out = ""
        i = 0
        while i < len(expr):
            if expr[i] == "~" and (i == 0 or expr[i-1] != "("):
                # The not operation is not bracketed
                
                out += "("

                end = i + 2

                if expr[i+1] == "(":
                    end = len(expr)
                    bracketings = 0

                    for j in range(i+1, len(expr)):
                        if bracketings == 0 and expr[j] == "(":
                            end == j
                            break

                        if expr[j] == "(":
                            bracketings += 1
                        elif expr[j] == ")":
                            bracketings -= 1
                
                out += expr[i:end]
                out += ")"
                i = end
            else:
                out += expr[i]
                i += 1
        
        # Shitty fix - if there are no top level unbracketed operations,
        # we must be in a not so unbracket the not
        topLevelOperation = False
        bracketing = 0
        for c in expr:
            if c == "(":
                bracketing += 1
            elif c == ")":
                bracketing -= 1
            
            if bracketing == 0 and c in ["^", "v"]:
                topLevelOperation = True
                break
        
        if not topLevelOperation:
            out = out[1:-1]
    

        return out

    def _GetLocal(expr, idx):
        """helper for OrderOper

            get the indicies for the local expression around
              a top operator
        """

        local_left = 0
        local_right = 0

        #backwards find left
        inverse_b = 0
        for i in range(idx-1, 0, -1):
            if expr[i] == ")":
                inverse_b += 1
            elif expr[i] == "(":
                inverse_b -= 1

            if inverse_b == 0:
                local_left = i-1
                break

        #forwards find right
        inverse_b = 0 #lazy safety
        for i in range(idx+1, len(expr)):
            if expr[i] == "(":
                inverse_b += 1
            elif expr[i] == ")":
                inverse_b -= 1

            if inverse_b == 0:
                local_right = i+1 
                break

        return (local_left, local_right)

    def OrderOper(expr: str) -> str:
        """
        Precedence
         AND >
         OR

        ensure the LHS' become the RHS'

        avb^c = av(b^c)
        a^bvc = (a^b)vc
        (a^b)^(b)v(c) = ((a^b)^(b)) v (c)
        
        1. get list of top level op indicies
        """

        and_idx = [] #lisst of index
        or_idx = []

        b = 0
        for i, c in enumerate(expr):
            if c == "(":
                b += 1
            elif c == ")":
                b -= 1
            
            if b == 0 and c == "^":
                and_idx.append(i)
            if b == 0 and c == "v":
                or_idx.append(i)

        and_brackets_idx = []
        or_brackets_idx = []
        for i in and_idx:
            and_brackets_idx.append(FOLe._GetLocal(expr, i))
        for i in or_idx:
            or_brackets_idx.append(FOLe._GetLocal(expr, i))


        print(f"and: {and_idx}")
        print(f"and bracs: {and_brackets_idx}")
        print(f"or: {or_idx}")
        print(f"or bracs: {or_brackets_idx}")
        

    def SubstringOperation(expr: str) -> list[str]:
        """
        Return a list containing the operation and the operand(s).
        Length will either be 2 or 3 depending on operand count.
        """

        # TODO: consider the edge case of not
        # TODO: Add method to order ambiguity with order of precedence
        #       and bracketing
        bracket_count = 0

        expr = FOLe.BracketNots(expr)
        #expr = FOLe.OrderOper(expr) #implement

        for i in range(len(expr)):
            if expr[i] == "(":
                bracket_count += 1
            elif expr[i] == ")":
                bracket_count -= 1
            
            # bracket_count must not be negative implies more ) than (
            assert bracket_count >= 0

            if bracket_count == 0 and expr[i] in ["^", "v"]:
                out = []
                # Append the operator
                out.append(expr[i])

                # Append the first operand
                if expr[0] == "(" and expr[i-1] == ")":
                    out.append(expr[1:i-1])
                else:
                    out.append(expr[:i])

                # Append the second operator
                if expr[i+1] == "(" and expr[-1] == ")":
                    out.append(expr[i+2:-1])
                else:
                    out.append(expr[i+1:])
                
                return out
            elif bracket_count == 0 and expr[i] == "~":
                out = []
                # Append the operator
                out.append(expr[i])

                # Append the first (only) operand
                if expr[i+1] == "(" and expr[-1] == ")":
                    out.append(expr[i+2:-1])
                else:
                    out.append(expr[i+1:])
                
                return out

    def ContainsOperation(expr: str) -> bool:
        for operator in FOLe.operators:
            if operator in expr:
                return True
        return False

    def CreateGraph(expr: str, depth: int = 0, parent: Node = None) -> Node:
        """
        Return the top level node from the FOL expression <expr>.
        """
        node = Node()
        parts = FOLe.SubstringOperation(expr)

        node.depth = depth
        node.parent = parent

        if parts[0] == "^":
            node.type = Operation.AND
        elif parts[0] == "v":
            node.type = Operation.OR
        elif parts[0] == "~":
            node.type = Operation.NOT
        
        if FOLe.ContainsOperation(parts[1]):
            node.left = FOLe.CreateGraph(parts[1], depth+1, node)
        else:
            child = Node()
            child.type = Operation.VAR
            child.var = parts[1]

            node.left = child
        
        if len(parts) == 3:
            if FOLe.ContainsOperation(parts[2]):
                node.right = FOLe.CreateGraph(parts[2], depth+1, node)
            else:
                child = Node()
                child.type = Operation.VAR
                child.var = parts[2]

                node.right = child #this was left and im chaning it to
                                   #right because i think there is bug 
        
        return node

        
        


test1 = "(a^b)v(a^c)"
test2 = "(av(bvc))^~(a^(bvc))"
edge1 = "a v b"

# print(f"test1: {FOLe.BracketBlock(test1)}, test2: {FOLe.BracketBlock(test2)}")
# print([test1[i[0]:i[1]] for i in FOLe.BracketBlock(test1)])

