from parser import FOLe
from nodes import Node, Operation
from worldgen import*
from arranger import Arranger
from command import *

def ValidInput(expr) -> bool:
    if len(expr) < 3:
        return False
    
    var_count = 0
    op_count = 0
    bk_count = 0

    for c in expr:
        if c in ['(',')']:
            bk_count += 1
        elif c.isalpha():
            var_count += 1
        elif c in ['^','v']:
            op_count += 1
    
    if op_count == var_count - 1 and bk_count%2 == 0:
        return True
    else: 
        return False

def process_input(expr) -> str:
    """This function processes the text passed to it and returns command
    for gui shit."""

    try:
        root = FOLe.CreateGraph(expr.strip())
        nodes = Arranger.ArrangeGates(root)
        circuit = Circuit(nodes, (root.position[0], root.position[1]-2), Arranger.ArrangeRedstone(nodes))
        out = circuit.get_command()
    except Exception as e:
        return f'processing error: {e}'

    return out
