from parser import *
import level


if __name__ == "__main__":
    print(f"test2: {test2}")
    root = FOLe.CreateGraph(test2)
    
    nodes = level.PostT(root)

    # Populate all level values
    for i in range(len(nodes)):
        nodes[i].level = level.GetLevel(nodes[i])

    # Set positions for level 0 (variables)
    for i in range(len(nodes)):
        if nodes[i].level == 0:
            nodes[i].position = (4*i + 1, 0)

    # Set positions for level 1
    for i in range(len(nodes)):
        if nodes[i].level != 1:
            continue
        isNot = nodes[i].type == Operation.NOT
        nodes[i].append((nodes[i].left.position[0] + (0 if isNot else 1), -(3 + 4*(1-1)), nodes[i].type))
    
    # Set positions for level 2
    for i in range(len(nodes)):
        if nodes[i].level != 2:
            continue
        isNot = nodes[i].type == Operation.NOT
        nodes[i].append((nodes[i].left.position[0] + (0 if isNot else 1), -(3 + 4*(2-1)), nodes[i].type))
    
    # Set positions for level 3
    for i in range(len(nodes)):
        if nodes[i].level != 3:
            continue
        isNot = nodes[i].type == Operation.NOT
        nodes[i].append((nodes[i].left.position[0] + (0 if isNot else 1), -(3 + 4*(3-1)), nodes[i].type))
    
    # Set positions for level 4
    for i in range(len(nodes)):
        if nodes[i].level != 4:
            continue
        isNot = nodes[i].type == Operation.NOT
        nodes[i].append((nodes[i].left.position[0] + (0 if isNot else 1), -(3 + 4*(4-1)), nodes[i].type))



