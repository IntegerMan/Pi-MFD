__author__ = 'Matt Eland'


import pygame


def build_font(size):
    return pygame.font.Font(None, size)


def init_pygame_graphics(res_x, res_y, title):

    pygame.init()

    # Prepare the Display
    display = pygame.display.set_mode((res_x, res_y))
    pygame.display.set_caption(title)

    # Return the Display
    return display


