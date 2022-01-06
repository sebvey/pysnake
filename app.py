import time

import pygame

from pysnake import features as feat
from pysnake import drawing, building


# GAME INITIALISATION

# Builds the world and the initial snake from the world txt file
world, snake = building.build_world_and_snake(feat.WORLD_PATH)


dX = [1, 0]  # Snake mouvement (initially moving to the right)
snake_growing = False  # Defines if the snake has eaten food and has to be grown
game_over = False  # Game State

# Rewards given for the move
wall_reward = -100 # negative reward when a wall is bumped
food_reward = 20 # positive reward when food is eaten
reward = 0 # last recorded reward
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


# MAIN LOOP

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

    building.move_snake(snake, snake_growing, dX)

    # Food Detection
    if world[snake[-1][1]][snake[-1][0]] == 'F':

        world[snake[-1][1]][snake[-1][0]] = ' '   # Deletes food on world
        snake_growing = True                      # asks to grow the snake
        reward = food_reward
        reward_alpha = 255

        building.add_food(world,snake)

    else :
        snake_growing = False

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

    clock.tick(20)  # Time delta between two steps

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
time.sleep(4)

# Quits
pygame.quit()
