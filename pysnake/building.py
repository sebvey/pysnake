from collections import deque


def build_world_and_snake(world_path):

    # loads the world from the txt file
    with open(world_path, 'r') as file:
        world = [[*line[:-1]] for line in file.readlines()]

    # Snake initial position :
    # On the world map, the starting point is located
    # with a 'S' -> look for the first and place the head
    # at this point

    snake_head = [1, 1]

    for j, line in enumerate(world):
        for i, element in enumerate(line):
            if element == 'S':
                snake_head[0], snake_head[1] = i, j
                break

    # Snake blocks position is stored in a deque
    # Adds the head to the deque
    # Adds a second block

    snake = deque([snake_head])
    snake.append([snake[-1][0] - 1, snake[-1][1]])

    return world, snake
