
def tokenizer(str):
    
    out = ""
    for c in str:
        if c == "^":
            out += "and "
        elif c == "v":
            out += "or "
        elif c == "~":
            out += "not "
        else:
            out += c +" "

    return out

def main():
    TEST = "(av(bvc))^~(a^(bvc))"

    print(tokenizer(TEST))

main()