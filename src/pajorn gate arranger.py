from parser import *
import level
import command


if __name__ == "__main__":
    print(f"test2: {test2}")
    root = FOLe.CreateGraph(test2)
    
    nodes = level.PostT(root)

    # Populate all level values
    for i in range(len(nodes)):
        nodes[i].level = level.GetLevel(nodes[i])

    # Set positions for level 0 (variables)
    node_indices = [i for i in range(len(nodes)) if nodes[i].level == 0]
    for i in range(len(node_indices)):
        nodes[node_indices[i]].position = (4*i + 1, 0)

    # Set positions for level 1
    node_indices = [i for i in range(len(nodes)) if nodes[i].level == 1]
    for i in range(len(node_indices)):
        isNot = nodes[node_indices[i]].type == Operation.NOT
        nodes[node_indices[i]].position = (nodes[node_indices[i]].left.position[0] + (0 if isNot else 1), -(3 + 4*(1-1)), nodes[node_indices[i]].type)
    
    # Set positions for level 2
    node_indices = [i for i in range(len(nodes)) if nodes[i].level == 2]
    for i in range(len(node_indices)):
        isNot = nodes[node_indices[i]].type == Operation.NOT
        nodes[node_indices[i]].position = (nodes[node_indices[i]].left.position[0] + (0 if isNot else 1), -(3 + 4*(2-1)), nodes[node_indices[i]].type)
    
    # Set positions for level 3
    node_indices = [i for i in range(len(nodes)) if nodes[i].level == 3]
    for i in range(len(node_indices)):
        isNot = nodes[node_indices[i]].type == Operation.NOT
        nodes[node_indices[i]].position = (nodes[node_indices[i]].left.position[0] + (0 if isNot else 1), -(3 + 4*(3-1)), nodes[node_indices[i]].type)
    
    # Set positions for level 4
    node_indices = [i for i in range(len(nodes)) if nodes[i].level == 4]
    for i in range(len(node_indices)):
        isNot = nodes[node_indices[i]].type == Operation.NOT
        nodes[node_indices[i]].position = (nodes[node_indices[i]].left.position[0] + (0 if isNot else 1), -(3 + 4*(4-1)), nodes[node_indices[i]].type)
    
    circuit = command.Circuit(nodes, (root.position[0], root.position[1]-2))
    circuit.get_command()

    for i in range(len(nodes)):
        print(f"{nodes[i].position[0]}, {nodes[i].position[1]}: {nodes[i]}, level: {nodes[i].level}")