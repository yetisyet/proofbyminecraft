
class FOLe():

    operators = ('^','v','~') #the three logic operators

    def __init__(self, expr):
        body = expr
        pass
    
    def BracketBlock(str):
        out = []

        l_brackets = []

        for i in range(len(str)):
            if str[i] == "(":
                l_brackets.append(i)
            elif str[i] == ")":
                out.append(str[l_brackets.pop()+1:i])

        return out

    test1 = "(a^b)v(a^c)"
    test2 = "(av(bvc))^~(a^(bvc))"
    edge1 = "a v b"

    print(f"test1: {BracketBlock2(test1)}, test2: {BracketBlock2(test2)}")

