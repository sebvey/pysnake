import os

# World Configuration

WORLD_PATH = os.path.join('maps', 'wagon_world.txt')
INIT_FOOD_NUMBER = 3

# Visual features used to render the game

SNAKE_COLOR = (255, 80, 80)
BACK_COLOR = (60, 60, 60)
BLOCK_COLOR = (255, 255, 255)
FOOD_COLOR = (204, 51, 255)

MSG_COLOR = (84, 139, 161)
GO_COLOR = (224, 150, 45)  # Game Over

BLOCK_SIZE = 15

# Speed of the game
GAME_FRAMERATE = 14 # framerate (step/s)

# REWARDS
WALL_REWARD = -100  # negative reward when a wall is bumped
FOOD_REWARD = 20  # positive reward when food is eaten
