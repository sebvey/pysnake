import os

# World map to use

WORLD_PATH = os.path.join('maps', 'wagon_world.txt')


# Visual features used to render the game

SNAKE_COLOR = (255, 80, 80)
BACK_COLOR = (60, 60, 60)
BLOCK_COLOR = (255, 255, 255)
FOOD_COLOR = (204, 51, 255)

MSG_COLOR = (0, 102, 204)

BLOCK_SIZE = 15

# Speed of the game

GAME_STEP_DURATION = 35

# REWARDS
WALL_REWARD = -100  # negative reward when a wall is bumped
FOOD_REWARD = 20  # positive reward when food is eaten
