class LogicGate:
    def __init__(self, position=(0, 0)):  # position(x,z)
        self.position = position  # find the position for each logic gate before inserting them

class NOT(LogicGate):
    def __init__(self, position):
        super().__init__(position)
        self.Code = f'''{{id:command_block_minecart,Command:"/summon armor_stand ~{position[0]} ~ ~{position[1]} {{Marker:1b,CustomName:\\"NOT\\",Tags:[placer]}}"}}'''

class AND(LogicGate):
    def __init__(self, position):
        super().__init__(position)
        self.Code = f'''{{id:command_block_minecart,Command:"/summon armor_stand ~{position[0]} ~ ~{position[1]} {{Marker:1b,CustomName:\\"AND\\",Tags:[placer]}}"}}'''

class OR(LogicGate):
    def __init__(self, position):
        super().__init__(position)
        self.Code = f'''{{id:command_block_minecart,Command:"/summon armor_stand ~{position[0]} ~ ~{position[1]} {{Marker:1b,CustomName:\\"OR\\",Tags:[placer]}}"}}'''

class Circuit:  # circuit holds all its logic gates
    def __init__(self):
        self.list_gates = []

    def add_gate(self, gate):  # to add a certain logic gate to a circuit
        self.list_gates.append(gate)


    def get_command(self):
        base_start = '''summon falling_block ~ ~1 ~ {BlockState:{Name:"redstone_block"},Time:1,Passengers:[{id:"falling_block",BlockState:{Name:"activator_rail"}}'''
        base_end = '''{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 red_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 light_blue_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 orange_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~ red_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~-1 redstone_wall_torch[facing=north]"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~1 redstone_wire"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~1 ~ ~ ~-1 ~ ~ minecraft:light_blue_wool replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~ ~ ~ ~ ~ ~-1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run setblock ~-1 ~ ~1 minecraft:repeater[facing=south] replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run setblock ~1 ~ ~1 minecraft:repeater[facing=south] replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~1 ~ ~ ~-1 ~ ~ minecraft:orange_wool replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~-1 ~ ~1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~1 ~ ~1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~-1 ~1 ~ ~1 ~1 ~ minecraft:redstone_torch replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~ ~1 ~ minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~ ~ ~-1 redstone_wall_torch[facing=north]"}, {id:command_block_minecart,Command:"/kill @e[type=minecraft:armor_stand,tag=placer]"}, {id:command_block_minecart,Command:"setblock ~ ~ ~1 command_block{Command:\\"fill ~ ~-1 ~-1 ~ ~ ~ air\\"} replace"},{id:command_block_minecart,Command:"setblock ~ ~-1 ~1 redstone_block"},{id:command_block_minecart,Command:"kill @e[type=command_block_minecart,distance=0..2]"}]}'''


        command = [base_start]

        for modules in self.list_gates:
            command.append(modules.Code)

        command.append(base_end)
        command = ",".join(command)

        print(command)

new_circuit = Circuit()
not_1 = NOT((-4, 4))
And_1 = AND((5,5))
Or_1 = OR((2,-2))
new_circuit.add_gate(not_1)
new_circuit.add_gate(And_1)
new_circuit.add_gate(Or_1)
new_circuit.get_command()