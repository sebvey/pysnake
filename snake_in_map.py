import pygame
import time
import pathlib
import random

from collections import deque


# We Build the World
world_path = 'map.txt'
with open(world_path, 'r') as file:
    world = [[*line[:-1]] for line in file.readlines()]


# Visual Features
snake_color = (0, 153, 51)
back_color = (60, 60, 60)
block_color = (255, 255, 255)
food_color = (255, 51, 153)

msg_color = (255, 20, 20)

block_size = 15

# Snake position and initial mouvement direction
snake_head = [1, 1]

for j, line in enumerate(world):
    for i, element in enumerate(line):
        if element == 'S':
            snake_head[0], snake_head[1] = i, j

snake = deque([snake_head])
dX = [1, 0]


# Player Score
wall_score = -100
food_score = 20
prox_score = 1

## PYGAME

pygame.init()

# Pygame initialisation
world_width = max([ len(l) for l in world ])
world_height = len(world)

dis_width = world_width * block_size
dis_height = world_height * block_size

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by sve')


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


def add_food():

    food_X = (
        random.randint(0, world_width),
        random.randint(0, world_height)
    )

    while world[food_X[1]][food_X[0]] != ' ':
        food_X = (
            random.randint(0, world_width),
            random.randint(0, world_height)
        )

    world[food_X[1]][food_X[0]] = 'F'


game_over = False

add_food()


clock = pygame.time.Clock()

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

    snake[-1][0] += dX[0]
    snake[-1][1] += dX[1]

    if world[snake[-1][1]][snake[-1][0]] == 'X':
        game_over = True

    dis.fill(back_color)

    # Drawing
    draw_world()
    draw_snake()

    pygame.display.update()
    clock.tick(20)

font_style = pygame.font.SysFont(None, 50)
msg = font_style.render('You lost !', True, msg_color)
dis.blit(msg, [dis_width / 2, dis_height / 2])
pygame.display.update()
time.sleep(1)

pygame.quit()
quit()
