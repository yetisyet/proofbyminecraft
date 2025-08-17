
from nodes import *
from position import *

class Circuit:  # circuit holds all its logic gates
    def __init__(self, list_nodes:list[object], lamp_position: tuple[int,int], redstone_locations: list[list[tuple[int, int]]] = [[], [], []]):
        self.list_nodes = list_nodes
        self.lamp_position = lamp_position
        self.redstone_locations = redstone_locations
        different_colours = ['red', 'blue', 'green', 'orange', 'yellow', 'lightblue', 'cyan', 'lime', 'pink', 'magenta']
        self.color_assignment = {}
        indexer = 0
        for modules in self.list_nodes: #assigns colors to levers
            if modules.type == Operation.VAR:
                if modules.var not in self.color_assignment:
                    self.color_assignment[modules.var] = different_colours[indexer]
                    indexer += 1
        
    def get_command(self):
        base_start = '''summon falling_block ~ ~1 ~ {BlockState:{Name:"redstone_block"},Time:1,Passengers:[{id:"falling_block",BlockState:{Name:"activator_rail"}}'''
        base_end = '''{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 red_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 light_blue_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~1 ~-1 ~1 ~-1 ~-1 ~-1 orange_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~ red_wool replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~-1 redstone_wall_torch[facing=north]"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='NOT'] run setblock ~ ~ ~1 redstone_wire"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~1 ~ ~ ~-1 ~ ~ minecraft:light_blue_wool replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run fill ~ ~ ~ ~ ~ ~-1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run setblock ~-1 ~ ~1 minecraft:repeater[facing=south] replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='OR'] run setblock ~1 ~ ~1 minecraft:repeater[facing=south] replace"},{id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~1 ~ ~ ~-1 ~ ~ minecraft:orange_wool replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~-1 ~ ~1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~1 ~ ~1 minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run fill ~-1 ~1 ~ ~1 ~1 ~ minecraft:redstone_torch replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~ ~1 ~ minecraft:redstone_wire replace"}, {id:command_block_minecart,Command:"/execute at @e[type=minecraft:armor_stand,name='AND'] run setblock ~ ~ ~-1 redstone_wall_torch[facing=north]"}, {id:command_block_minecart,Command:"/kill @e[type=minecraft:armor_stand,tag=placer]"}, {id:command_block_minecart,Command:"setblock ~ ~ ~1 command_block{Command:\\"fill ~ ~-1 ~-1 ~ ~ ~ air\\"} replace"},{id:command_block_minecart,Command:"setblock ~ ~-1 ~1 redstone_block"},{id:command_block_minecart,Command:"kill @e[type=command_block_minecart,distance=0..2]"}]}'''
        command = [base_start]

        for modules in self.list_nodes:
            if modules.type == Operation.NOT:
                name = 'NOT'
            elif modules.type == Operation.AND:
                name = 'AND'
            elif modules.type == Operation.OR:
                name = 'OR'
            elif modules.type == Operation.VAR: #position of levers
                lever_code = f'''{{id:command_block_minecart,Command:"/setblock ~{modules.position[0]} ~-2 ~{modules.position[1]-4} lever[face=floor] replace"}}'''
                command.append(lever_code)
                lever_color_code = f'''{{id:command_block_minecart,Command:"/setblock ~{modules.position[0]} ~-3 ~{modules.position[1]-4} {self.color_assignment[modules.var]}_concrete replace"}}'''
                command.append(lever_color_code)
                continue
            else:
                continue

            code = f'''{{id:command_block_minecart,Command:"/summon armor_stand ~{modules.position[0]} ~-2 ~{modules.position[1]-4} {{Marker:1b,CustomName:\\"{name}\\",Tags:[placer]}}"}}'''
            command.append(code)
        
        lantern_code = f'''{{id:command_block_minecart,Command:"/setblock ~{self.lamp_position[0]} ~-2 ~{self.lamp_position[1]-5} redstone_lamp replace"}},{{id:command_block_minecart,Command:"/setblock ~{self.lamp_position[0]} ~-2 ~{self.lamp_position[1]-4} redstone_wire replace"}}'''
        command.append(lantern_code)
        
        # Given that the redstone wires are straight lines by design, it would
        # be optimal to replace the setblocks with fills, however, we do not
        # have time.
        for pos in self.redstone_locations[0]:
            command.append(f'''{{id:command_block_minecart,Command:"/setblock ~{pos[0]} ~-2 ~{pos[1]-4} redstone_wire replace"}}''')
        
        # Place up facing repeaters
        for pos in self.redstone_locations[1]:
            command.append(f'''{{id:command_block_minecart,Command:"/setblock ~{pos[0]} ~-2 ~{pos[1]-4} repeater[facing=south] replace"}}''')
        
        # Place left facing repeaters
        for pos in self.redstone_locations[2]:
            command.append(f'''{{id:command_block_minecart,Command:"/setblock ~{pos[0]} ~-2 ~{pos[1]-4} repeater[facing=east] replace"}}''')
            
        command.append(base_end)
        command = ",".join(command)
        
        # print(command)
        return(command)


