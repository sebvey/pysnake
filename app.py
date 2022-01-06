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

display_width = world_width * feat.BLOCK_SIZE
display_height = world_height * feat.BLOCK_SIZE

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game by sve')


## MAIN LOOP
# Catches events
# - updates the world and the snake
# - leaves the loop when a wall is collided (or game exited)

while not game_over:

    for event in pygame.event.get():

        # Break on QUIT event (closed window)
        if event.type == pygame.QUIT:
            game_over = True

        # Updates the snake movement depending on the KEY pressed
        if event.type == pygame.KEYDOWN:
            if event.key   == pygame.K_LEFT  : dX = [-1, 0]
            elif event.key == pygame.K_RIGHT : dX = [1 , 0]
            elif event.key == pygame.K_UP    : dX = [0 ,-1]
            elif event.key == pygame.K_DOWN  : dX = [0 , 1]

    # Moves the snake
    building.move_snake(snake, snake_growing, dX)

    # Detects if snake eats food and updates the world and states
    if world[snake[-1][1]][snake[-1][0]] == 'F':
        world[snake[-1][1]][snake[-1][0]] = ' '   # Deletes food on world
        snake_growing = True                      # asks to grow the snake
        reward = food_reward                      # updates the award
        reward_alpha = 255                        # for display fading

        building.add_food(world,snake)            # Adds new food

    else :
        snake_growing = False

    # Detects Snake Head-to-Wall collision
    if world[snake[-1][1]][snake[-1][0]] == 'X':
        game_over = True

    # Drawing
    drawing.draw_world(display,world)
    drawing.draw_snake(display,snake)
    drawing.draw_reward(display,reward,reward_alpha)

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

drawing.draw_world(display,world)
drawing.draw_snake(display,snake)
drawing.draw_reward(display,reward,reward_alpha)
drawing.draw_end(display,display_width,display_height)


pygame.display.update()
time.sleep(4)

# Quits
pygame.quit()
