from parser import *
import level
import command

class Arranger:
    def Arrange(root: Node) -> list[Node]:
        """
        Return a list of nodes with all their position values populated
        for use with Circuit class.
        """
        nodes = level.PostT(root)

        max_level = 0

        # Populate all level values
        for i in range(len(nodes)):
            nodes[i].level = level.GetLevel(nodes[i])
            if nodes[i].level > max_level:
                max_level = nodes[i].level

        # Set positions for level 0 (variables)
        node_indices = [i for i in range(len(nodes)) if nodes[i].level == 0]
        for i in range(len(node_indices)):
            nodes[node_indices[i]].position = (4*i + 1, 0)

        # Set positions for level i in [1, max_level]
        for i in range(1, max_level+1):
            node_indices = [j for j in range(len(nodes)) if nodes[j].level == i]
            for j in range(len(node_indices)):
                isNot = nodes[node_indices[j]].type == Operation.NOT
                nodes[node_indices[j]].position = (nodes[node_indices[j]].left.position[0] + (0 if isNot else 1), -(3 + 4*(i-1)))

        return nodes 

if __name__ == "__main__":
    print(f"test2: {test2}")
    root = FOLe.CreateGraph(test2)
    
    nodes = Arranger.Arrange(root)
    
    circuit = command.Circuit(nodes, (root.position[0], root.position[1]-2))
    circuit.get_command()
    