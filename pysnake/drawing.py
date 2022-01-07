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

def draw_text(pygame_display,score,game_over=False):
    """ Function drawing the text information with pygame.

    - pygame_display : the pygame display object
    - reward : int
    - reward_alpha : alpha transparency of the font
    """

    txt_font = pygame.font.SysFont(None, 28)

    # Score drawing
    txt_surface = txt_font.render("SCORE", True, feat.MSG_COLOR)
    pygame_display.blit(txt_surface, [10, 50])

    score_surface = txt_font.render(str(score), True, feat.MSG_COLOR)
    pygame_display.blit(score_surface, [10, 80])

    # Quit drawing
    quit_surface = txt_font.render("'Q' to Quit", True, feat.MSG_COLOR)
    pygame_display.blit(quit_surface, [10, 610])

    # Restart drawing
    restart_surface = txt_font.render("'Enter' to Restart", True, feat.MSG_COLOR)
    pygame_display.blit(restart_surface, [10, 580])

    if game_over :
        reward_font = pygame.font.SysFont(None, 70)

        txt_surface = reward_font.render("GAME", True, feat.GO_COLOR)
        pygame_display.blit(txt_surface, [10, 250])
        txt_surface = reward_font.render("OVER", True, feat.GO_COLOR)
        pygame_display.blit(txt_surface, [10, 300])

def draw_end(pygame_display,world,snake,reward):
    """ Function drawing the end message when the game is over

    - pygame_display : the pygame display object
    - display_witdh / display_height : size in pixel of the display
    """

    draw_world(pygame_display,world)
    draw_snake(pygame_display,snake)
    draw_text(pygame_display,reward,game_over=True)

    pygame.display.update()


def draw_all(pygame_display,world,snake,reward):


    draw_world(pygame_display,world)
    draw_snake(pygame_display, snake)
    draw_text(pygame_display, reward)
    pygame.display.update()
