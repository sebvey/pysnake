import pygame

import itertools

from pygame.constants import K_q

from pysnake import features as feat
from pysnake import drawing, building


### GAME INITIALISATION --------------------------------------------------------

def init_game() :
    # Builds the world and the initial snake from the world txt file
    world, snake = building.build_world_and_snake(feat.WORLD_PATH)

    dX = [1, 0]  # Snake mouvement (initially moving to the right)

    # Score
    score = 0

    # Snake Growth - number of block to add
    snake_growth = 0

    print('init snake : ' + str(snake))
    print(f'init snake_growth : {snake_growth}')

    return world, snake, dX, score, snake_growth

## PYGAME INITIALISATION -------------------------------------------------------

def init_pygame():

    pygame.init()
    clock = pygame.time.Clock()

    world_width = max([ len(l) for l in world ])
    world_height = len(world)

    display_width = world_width * feat.BLOCK_SIZE
    display_height = world_height * feat.BLOCK_SIZE

    display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Snake Game by sve')

    return display,clock


### MAIN LOOP ------------------------------------------------------------------

world, snake, dX, score, snake_growth = init_game()
display,clock = init_pygame()

while True :

    # Treats pygame events (arrow keys and quit event)
    for event in pygame.event.get():

        # Break on QUIT event (closed window)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Updates the snake movement depending on the KEY pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and dX != [1, 0] :
                dX = [-1, 0]
            elif event.key == pygame.K_RIGHT and dX != [-1, 0] :
                dX = [1, 0]
            elif event.key == pygame.K_UP and dX != [0 ,1]  :
                dX = [0 ,-1]
            elif event.key == pygame.K_DOWN and dX != [0,-1] :
                dX = [0 , 1]

            elif event.key == pygame.K_RETURN : # Restart the game
                world, snake, dX, score, snake_growth = init_game()
                print('standard enter')

            elif event.key == pygame.K_q:  # quit the game
                pygame.quit()
                quit()

    # Detects if snake eats food and updates the world and states
    if world[snake[-1][1]][snake[-1][0]] == 'F':
        world[snake[-1][1]][snake[-1][0]] = ' '   # Deletes food on world
        snake_growth += feat.SNAKE_GROWTH        # asks to grow the snake
        score += feat.FOOD_REWARD                 # updates the award

        building.add_food(world,snake)            # Adds new food

    # Snake Tail collision boolean
    snake_head = snake[-1]
    snake_tail = list(itertools.islice(snake,0,len(snake)-1))
    tail_collision = snake_head in snake_tail

    # Snake Wall collision boolean
    wall_collision = world[snake[-1][1]][snake[-1][0]] == 'X'

    # If collision detected, draw_end and wait for a key event
    waiting = False
    if tail_collision or wall_collision :
        drawing.draw_end(display,world,snake,score)
        waiting = True

    while waiting :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN : # Restart the game
                    waiting = False
                    world, snake, dX, score, snake_growth = init_game()

                elif event.key == pygame.K_q:  # quit the game
                    pygame.quit()
                    quit()

    # Moves the snake
    snake_growth = building.update_snake(snake, snake_growth, dX)

    # Draws the game with pygame
    drawing.draw_all(display,world,snake,score)

    # Wait still next step
    clock.tick(feat.GAME_FRAMERATE)
