world_path = 'simple_world.txt'

with open(world_path, 'r') as file:
    world = [[*line[:-1]] for line in file.readlines()]

print(*world,sep='\n')
