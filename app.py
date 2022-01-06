import pygame

import itertools

from pysnake import features as feat
from pysnake import drawing, building


### GAME INITIALISATION --------------------------------------------------------

# Builds the world and the initial snake from the world txt file
world, snake = building.build_world_and_snake(feat.WORLD_PATH)

dX = [1, 0]  # Snake mouvement (initially moving to the right)
snake_growing = False  # Defines if the snake has eaten food and has to be grown

# Rewards given for the move
reward = 0 # last recorded reward
reward_alpha = 0


## PYGAME INIT -----------------------------------------------------------------

pygame.init()
clock = pygame.time.Clock()

world_width = max([ len(l) for l in world ])
world_height = len(world)

display_width = world_width * feat.BLOCK_SIZE
display_height = world_height * feat.BLOCK_SIZE

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snake Game by sve')


### MAIN LOOP ------------------------------------------------------------------

while True :

    # Treats pygame events (arrow keys and quit event)
    for event in pygame.event.get():

        # Break on QUIT event (closed window)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Updates the snake movement depending on the KEY pressed
        if event.type == pygame.KEYDOWN:
            if event.key   == pygame.K_LEFT  : dX = [-1, 0]
            elif event.key == pygame.K_RIGHT : dX = [1 , 0]
            elif event.key == pygame.K_UP    : dX = [0 ,-1]
            elif event.key == pygame.K_DOWN  : dX = [0 , 1]

    # Moves the snake
    building.move_snake(snake, snake_growing, dX)

    # Detects if snake eats food and updates the world and states
    snake_growing = False
    if world[snake[-1][1]][snake[-1][0]] == 'F':
        world[snake[-1][1]][snake[-1][0]] = ' '   # Deletes food on world
        snake_growing = True                      # asks to grow the snake
        reward = feat.FOOD_REWARD                 # updates the award
        reward_alpha = 255                        # for display fading

        building.add_food(world,snake)            # Adds new food

    # Detects Snake Head-to-Tail collision
    snake_head = snake[-1]
    snake_tail = list(itertools.islice(snake,0,len(snake)-1))
    if snake_head in snake_tail :
        drawing.draw_collision_end_and_quit(display,world,snake)


    # Detects Snake Head-to-Wall collision
    if world[snake[-1][1]][snake[-1][0]] == 'X':
        drawing.draw_collision_end_and_quit(display,world,snake)

    # Draws the game with pygame
    drawing.draw_all(display,world,snake,reward,reward_alpha)

    # Wait still next step
    clock.tick(feat.GAME_FRAMERATE)

    # Updates the alpha of the display (for fading purpose)
    if reward_alpha > 15 : reward_alpha -= 15
    else : reward_alpha = 0
