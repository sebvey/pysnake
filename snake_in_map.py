import pygame
import time
import pathlib
import random

from collections import deque


# We Build the World
world_path = 'wagon_world.txt'
with open(world_path, 'r') as file:
    world = [[*line[:-1]] for line in file.readlines()]


# Visual Features
snake_color = (255, 80, 80)
back_color = (60, 60, 60)
block_color = (255, 255, 255)
food_color = (204, 51, 255)

msg_color = (0, 102, 204)

block_size = 15

# Snake position and initial movement direction
snake_head = [1, 1]

for j, line in enumerate(world):
    for i, element in enumerate(line):
        if element == 'S':
            snake_head[0], snake_head[1] = i, j


snake = deque([snake_head]) # Adds Head to the snake
snake_body1 = [ snake[-1][0] - 1, snake[-1][1] ]
snake.append(snake_body1)
dX = [1, 0]
growing_snake = False # Passed to True when snake has to grow

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

dis_width = world_width * block_size
dis_height = world_height * block_size

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by sve')


## USEFULL FUNCTIONS

def draw_world():

    for j, line in enumerate(world):
        for i, element in enumerate(line):

            # Blocks
            if element == 'X':

                pygame.draw.rect(
                    dis,
                    block_color,
                    [i*block_size, j*block_size, block_size, block_size]
                )

            # Food
            if element == 'F':

                pygame.draw.rect(
                    dis,
                    food_color,
                    [i*block_size, j*block_size, block_size, block_size]
                )

def draw_snake():

    # Snake drawing

    for block in snake :

        pygame.draw.rect(
            dis, snake_color,
            [block[0] * block_size, block[1] * block_size, block_size, block_size]
        )

def draw_reward():

    reward_font = pygame.font.SysFont(None, 35)

    txt_surface = reward_font.render("REWARD", True,msg_color)
    dis.blit(txt_surface, [50, 50])

    reward_surface = reward_font.render(str(reward), True,msg_color)
    reward_surface.set_alpha(reward_alpha)
    dis.blit(reward_surface, [50, 80])

def draw_end():
    font_style = pygame.font.SysFont(None, 50)
    msg = font_style.render('LEARN AGAIN !', True, msg_color)
    dis.blit(msg, [dis_width / 2 - 130, dis_height - 100])

def draw_all_and_pause():
    # Draw and pause, for vidéo capture
    dis.fill(back_color)
    draw_world()
    draw_snake()
    draw_reward()
    pygame.display.update()
    time.sleep(10)

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

# draw_all_and_pause() # Just the time to capture the screen ;-)

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
    dis.fill(back_color)
    draw_world()
    draw_snake()
    draw_reward()

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

draw_world()
draw_snake()
draw_reward()
draw_end()


pygame.display.update()
time.sleep(5)

# Quits
pygame.quit()
quit()
