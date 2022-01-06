import pygame

import itertools

from pysnake import features as feat
from pysnake import drawing, building


### GAME INITIALISATION --------------------------------------------------------

def init_game() :
    # Builds the world and the initial snake from the world txt file
    world, snake = building.build_world_and_snake(feat.WORLD_PATH)

    dX = [1, 0]  # Snake mouvement (initially moving to the right)
    snake_growing = False  # Defines if the snake has eaten food and has to be grown

    # Score
    score = 0

    return world,snake,dX,score,snake_growing

## PYGAME INIT -----------------------------------------------------------------

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

world, snake, dX, score, snake_growing = init_game()
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

    # Moves the snake
    building.move_snake(snake, snake_growing, dX)

    # Detects if snake eats food and updates the world and states
    snake_growing = False
    if world[snake[-1][1]][snake[-1][0]] == 'F':
        world[snake[-1][1]][snake[-1][0]] = ' '   # Deletes food on world
        snake_growing = True                      # asks to grow the snake
        score += feat.FOOD_REWARD                 # updates the award

        building.add_food(world,snake)            # Adds new food

    # Detects Snake Head-to-Tail collision
    snake_head = snake[-1]
    snake_tail = list(itertools.islice(snake,0,len(snake)-1))
    if snake_head in snake_tail :
        drawing.draw_collision_end_and_quit(display,world,snake,score)


    # Detects Snake Head-to-Wall collision
    if world[snake[-1][1]][snake[-1][0]] == 'X':
        drawing.draw_collision_end_and_quit(display,world,snake,score)

    # Draws the game with pygame
    drawing.draw_all(display,world,snake,score)

    # Wait still next step
    clock.tick(feat.GAME_FRAMERATE)
