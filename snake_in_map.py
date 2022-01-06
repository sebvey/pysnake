import os
import time
import random
from collections import deque

import pygame

from pysnake import game_features as feat
from pysnake import drawing


# WORLD BUILDING

# loads the world from the txt file

world_path = os.path.join('maps','wagon_world.txt')
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

# Snake initial mouvement
dX = [1, 0] # moving to the right

# Defines if the snake has eaten food and have to be grown
growing_snake = False

# Game state initialisation
game_over = False

# Player Score and rewards
wall_reward = -100
food_reward = 20
reward = 0
reward_alpha = 0

## PYGAME INIT

pygame.init()
clock = pygame.time.Clock()

world_width = max([ len(l) for l in world ])
world_height = len(world)

dis_width = world_width * feat.BLOCK_SIZE
dis_height = world_height * feat.BLOCK_SIZE

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by sve')


## USEFULL FUNCTIONS

def add_food():

    food_X = (
        random.randrange(0, world_width),
        random.randrange(0, world_height)
    )

    food_unreachable = world[food_X[1]][food_X[0]] != ' '
    food_on_snake = [food_X[0],food_X[1]] in snake


    # Regenerate the food as long as unreachable or on the snake
    while food_unreachable or food_on_snake :

        food_X = (
            random.randrange(0, world_width),
            random.randrange(0, world_height)
        )

        food_unreachable = world[food_X[1]][food_X[0]] != ' '
        food_on_snake = [food_X[0], food_X[1]] in snake

    world[food_X[1]][food_X[0]] = 'F'

def move_snake(growing):

    new_head = [ snake[-1][0] + dX[0], snake[-1][1] + dX[1] ]
    snake.append(new_head)

    if not growing:  # When snake is not growing, pop the tail
        snake.popleft()

add_food()

while not game_over:

    for event in pygame.event.get():

        # Break on QUIT event
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dX = [-1, 0]
            elif event.key == pygame.K_RIGHT:
                dX = [1, 0]
            elif event.key == pygame.K_UP:
                dX = [0,-1]
            elif event.key == pygame.K_DOWN:
                dX = [0,1]

    move_snake(growing_snake)

    # Food Detection
    if world[snake[-1][1]][snake[-1][0]] == 'F':

        world[snake[-1][1]][snake[-1][0]] = ' '   # Delete food on world
        growing_snake = True                      # Will grow the snake
        reward = food_reward
        reward_alpha = 255

        add_food()

    else :
        growing_snake = False

    # Head-Wall Collision detection
    if world[snake[-1][1]][snake[-1][0]] == 'X':
        game_over = True

    # TODO : Head-Body Collision

    # Drawing
    dis.fill(feat.BACK_COLOR)
    drawing.draw_world(dis,world)
    drawing.draw_snake(dis,snake)
    drawing.draw_reward(dis,reward,reward_alpha)

    pygame.display.update()

    # Time delta between two steps
    clock.tick(20)

    # Reward fade
    if reward_alpha > 15 :
        reward_alpha -= 15
    else :
        reward_alpha = 0


# WALL COLLISION 😠
reward = wall_reward
reward_alpha = 255

drawing.draw_world(dis,world)
drawing.draw_snake(dis,snake)
drawing.draw_reward(dis,reward,reward_alpha)
drawing.draw_end(dis,dis_width,dis_height)


pygame.display.update()
time.sleep(5)

# Quits
pygame.quit()
quit()
