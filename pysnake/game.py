from collections import deque
import itertools
import random

import pygame

from pysnake import features as feat
from pysnake import drawing

class Game():
    """
    Attributes :
    - WORLD_PATH : path to the txt file discribing the initial world
    - world : list, Each element is a line, each line is a list of characters
    - snake : snake blocks position (deque object)
    - snake_growth : number of element waiting to be added to the snake
    - snake_dir : direction of the snake either :
        * 'R' (right)
        * 'L' (left)
        * 'U' (up)
        * 'D' (down)

    - game_over : bool indicating if the game is over
    - pg_display : pygame display
    - pg_clock : pygame clock
    """

    def __init__(self,WORLD_PATH=feat.WORLD_PATH):

        self.WORLD_PATH = WORLD_PATH
        self.init_game() # game state initialisation
        self.init_pygame() # pygame specific initialisation


    def add_food(self):
        """
        Adds food to the world.
        Food is represented by a 'F' character.
        """

        world_width = max([ len(l) for l in self.world ])
        world_height = len(self.world)

        food_X = (random.randrange(0,
                                world_width), random.randrange(0, world_height))

        food_unreachable = self.world[food_X[1]][food_X[0]] != ' '
        food_on_snake = [food_X[0], food_X[1]] in self.snake

        # Regenerate the food as long as unreachable or on the snake
        while food_unreachable or food_on_snake:

            food_X = (random.randrange(0, world_width),
                    random.randrange(0, world_height))

            food_unreachable = self.world[food_X[1]][food_X[0]] != ' '
            food_on_snake = [food_X[0], food_X[1]] in self.snake

        self.world[food_X[1]][food_X[0]] = 'F'

    def process_food_eating(self):
        """
        Detects if snake eats food and updates :
        - world (remove eated food, adds new one)
        - score
        - snake_growth
        """

        snake = self.snake
        world = self.world

        if world[snake[-1][1]][snake[-1][0]] == 'F':
            world[snake[-1][1]][snake[-1][0]] = ' '  # Deletes food on world
            self.add_food()

            self.snake_growth += feat.SNAKE_GROWTH  # asks to grow the snake
            self.score += feat.FOOD_REWARD  # updates the award

    def init_game(self):
        """
        Initializes attributes :
        - world, snake, snake_growth, score, game_over, snake_dir
        """

        # loads the world from the txt file
        with open(self.WORLD_PATH, 'r') as file:
            self.world = [[*line[:-1]] for line in file.readlines()]

        # Snake initial position :
        # On the world map, the starting point is located
        # with a 'S' -> look for the first and place the head
        # at this point

        snake_head = [1, 1]

        for j, line in enumerate(self.world):
            for i, element in enumerate(line):
                if element == 'S':
                    snake_head[0], snake_head[1] = i, j
                    break

        # Snake blocks position is stored in a deque
        # Adds the head to the deque
        # Adds a second block

        snake = deque([snake_head])
        snake.append([snake[-1][0] - 1, snake[-1][1]])
        self.snake = snake

        # Adds three food elements
        for _ in range(feat.INIT_FOOD_NUMBER):
            self.add_food()

        self.snake_dir = 'R'  # Snake mouvement (initially moving to the right)

        # Score
        self.score = 0

        # Snake Growth - number of block to add
        self.snake_growth = 0

        # Game State
        self.game_over = False

        return self

    def init_pygame(self):
        """Initializes pygame display and clock as attributes"""

        pygame.init()

        self.pg_clock = pygame.time.Clock()

        world_width = max([len(l) for l in self.world])
        world_height = len(self.world)

        disp_width = world_width * feat.BLOCK_SIZE
        disp_height = world_height * feat.BLOCK_SIZE

        self.pg_display = pygame.display.set_mode((disp_width, disp_height))
        pygame.display.set_caption('Snake Game by sve')

        return self

    def update_snake(self):
        """Update the snake (moves and grows it)"""

        if self.snake_dir == 'U' : dX = (0,-1)
        elif self.snake_dir == 'D' : dX = (0,1)
        elif self.snake_dir == 'R' : dX = (1,0)
        elif self.snake_dir == 'L' : dX = (-1,0)

        snake = self.snake
        new_head = [snake[-1][0] + dX[0], snake[-1][1] + dX[1]]
        snake.append(new_head)

        # When snake is not growing, pop the tail
        if not self.snake_growth:
            snake.popleft()

        # Else the snake is growing, we keep the tail
        else :
            self.snake_growth -= 1

    def collision_detected(self):
        """
        Checks the two types of collisions :
        - Snake Head to Tail
        - Snake Head to Wall

        returns True collision detected
        """

        # Snake Head to Tail collision boolean
        snake_head = self.snake[-1]
        snake_tail = list(itertools.islice(self.snake,0,len(self.snake)-1))
        tail_collision = snake_head in snake_tail

        # Snake Wall collision boolean
        wall_collision = self.world[self.snake[-1][1]][self.snake[-1][0]] == 'X'

        return tail_collision or wall_collision

    def process_pygame_events(self):
        """
        Reads pygame events, updates the move stack.
        Returns True if Quit is asked by the user
        """

        for event in pygame.event.get():

            # Break on QUIT event (closed window)
            if event.type == pygame.QUIT:
                return True

            # Updates the snake movement depending on the KEY pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.snake_dir != 'R':
                    self.snake_dir = 'L'
                elif event.key == pygame.K_RIGHT and self.snake_dir != 'L':
                    self.snake_dir = 'R'
                elif event.key == pygame.K_UP and self.snake_dir != 'D':
                    self.snake_dir = 'U'
                elif event.key == pygame.K_DOWN and self.snake_dir != 'U':
                    self.snake_dir = 'D'

                elif event.key == pygame.K_RETURN:  # Restart the game
                    self.init_game()

                elif event.key == pygame.K_q:  # quit the game
                    return True

        return False # Game still running

    def restart_asked(self):
        """Waits for a user (pygame) event to reinit the game or leave """

        while True :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN :
                    return True

                if event.key == pygame.K_q :
                    return False

    def run(self):

        while True :

            game_exit_asked = self.process_pygame_events()

            if game_exit_asked :
                pygame.quit()
                return 1

            self.update_snake()
            self.process_food_eating()

            if self.collision_detected() :

                self.game_over = True
                drawing.draw_end(self)

                if self.restart_asked() :
                    self.init_game()

                else :
                    pygame.quit()
                    return 1

            # Draws the game with pygame
            drawing.draw_all(self)

            # Wait still next step
            self.pg_clock.tick(feat.GAME_FRAMERATE)
