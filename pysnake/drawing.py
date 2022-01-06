import pygame
import time

from pysnake import features as feat


def draw_world(pygame_display,world):
    """Function drawing the world with pygame.

    - pygame_display is the pygame display object

    - The input world list is structured as follow :
        * Each element is a line
        * Each line is a list of characters"""

    # Fill the background
    pygame_display.fill(feat.BACK_COLOR)

    # For each block of the world, draws the corresponding element
    for j, line in enumerate(world):
        for i, element in enumerate(line):

            # Blocks
            if element == 'X':

                pygame.draw.rect(pygame_display, feat.BLOCK_COLOR, [
                    i * feat.BLOCK_SIZE, j * feat.BLOCK_SIZE, feat.BLOCK_SIZE,
                    feat.BLOCK_SIZE
                ])

            # Food
            if element == 'F':

                pygame.draw.rect(pygame_display, feat.FOOD_COLOR, [
                    i * feat.BLOCK_SIZE, j * feat.BLOCK_SIZE, feat.BLOCK_SIZE,
                    feat.BLOCK_SIZE
                ])


def draw_snake(pygame_display,snake):
    """Function drawing the snake with pysnake

   - pygame_display : pygame display object
   - snake : snake blocks position (deque object)
    """

    for block in snake:

        pygame.draw.rect(
            pygame_display,
            feat.SNAKE_COLOR,
            [ block[0] * feat.BLOCK_SIZE, block[1] * feat.BLOCK_SIZE,
            feat.BLOCK_SIZE, feat.BLOCK_SIZE ]
        )


def draw_reward(pygame_display,reward, reward_alpha):
    """ Function drawing the reward information with pygame.

    - pygame_display : the pygame display object
    - reward : int
    - reward_alpha : alpha transparency of the font
    """

    reward_font = pygame.font.SysFont(None, 35)

    txt_surface = reward_font.render("REWARD", True, feat.MSG_COLOR)
    pygame_display.blit(txt_surface, [50, 50])

    reward_surface = reward_font.render(str(reward), True, feat.MSG_COLOR)
    reward_surface.set_alpha(reward_alpha)
    pygame_display.blit(reward_surface, [50, 80])


def draw_collision_end_and_quit(pygame_display,world,snake):
    """ Function drawing the end message when the game is over

    - pygame_display : the pygame display object
    - display_witdh / display_height : size in pixel of the display
    """

    draw_world(pygame_display,world)
    draw_snake(pygame_display,snake)
    draw_reward(pygame_display,feat.WALL_REWARD,255)

    # Ends message

    world_width = max([ len(l) for l in world ])
    world_height = len(world)

    display_width = world_width * feat.BLOCK_SIZE
    display_height = world_height * feat.BLOCK_SIZE

    font_style = pygame.font.SysFont(None, 50)
    msg = font_style.render('LEARN AGAIN...', True, feat.MSG_COLOR)
    pygame_display.blit(msg, [display_width / 2 - 130, display_height - 100])

    # Quits
    time.sleep(4)
    pygame.quit()


def draw_all(pygame_display,world,snake,reward,reward_alpha):

    draw_world(pygame_display,world)
    draw_snake(pygame_display, snake)
    draw_reward(pygame_display, reward, reward_alpha)
    pygame.display.update()

    pygame.display.update()

    # Quits
    time.sleep(4)
    pygame.quit()
