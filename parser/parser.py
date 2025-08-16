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

print(FOLe.CreateGraph(test1))

