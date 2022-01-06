from collections import deque
import random


def build_world_and_snake(world_path):
    """
    Buids the snake object and the world object.

    INPUT :
    - world_path : path to the .txt file representing the world

    OUTPUTS :
    - world : list, Each element is a line, each line is a list of characters
    - snake : snake blocks position (deque object)
    """

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

    # Adds three food elements
    for _ in range(3) : add_food(world,snake)

    return world, snake


def add_food(world,snake):
    """
    Adds food to the world.

    INPUTS :
    - world : list, Each element is a line, each line is a list of characters
    - snake : snake blocks position (deque object)
    """

    world_width = max([ len(l) for l in world ])
    world_height = len(world)

    food_X = (random.randrange(0,
                               world_width), random.randrange(0, world_height))

    food_unreachable = world[food_X[1]][food_X[0]] != ' '
    food_on_snake = [food_X[0], food_X[1]] in snake

    # Regenerate the food as long as unreachable or on the snake
    while food_unreachable or food_on_snake:

        food_X = (random.randrange(0, world_width),
                  random.randrange(0, world_height))

        food_unreachable = world[food_X[1]][food_X[0]] != ' '
        food_on_snake = [food_X[0], food_X[1]] in snake

    world[food_X[1]][food_X[0]] = 'F'


def move_snake(snake,snake_growing,dX):
    """
    Moves the snake (update snake (deque)

    - snake : snake blocks position (deque object)
    - snake_growing : defines if the snake has to be grown (bool)
    - dX : snake mouvement [ delta_x (int), delta_y (int) ]
    """

    new_head = [snake[-1][0] + dX[0], snake[-1][1] + dX[1]]
    snake.append(new_head)

    if not snake_growing:  # When snake is not growing, pop the tail
        snake.popleft()
