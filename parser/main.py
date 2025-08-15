from __future__ import annotations
from nodes import *

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

    def CreateNode() -> Node:
        pass

    def BracketNots(expr: str) -> str:
        """
        Ensure each not operation is bracketed
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
        
        return out





    def CreateGraph(expr) -> Node:
        """
        Return the top level node from the FOL expression <expr>.
        """
        
        # TODO: consider the edge case of not
        # TODO: Add method to order ambiguity with order of precedence
        #       and bracketing
        bracket_count = 0

        for i in range(len(expr)):
            if expr[i] == "(":
                bracket_count += 1
            elif expr[i] == ")":
                bracket_count -= 1
            
            # bracket_count must not be negative implies more ) than (
            assert bracket_count >= 0


test1 = "(a^b)v(a^c)"
test2 = "(av(bvc))^~(a^(bvc))"
edge1 = "a v b"

# print(f"test1: {FOLe.BracketBlock(test1)}, test2: {FOLe.BracketBlock(test2)}")
# print([test1[i[0]:i[1]] for i in FOLe.BracketBlock(test1)])

