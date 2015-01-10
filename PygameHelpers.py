__author__ = 'Matt Eland'


import pygame


def build_font(size):
    return pygame.font.Font(None, size)


def init_pygame_graphics(displaySettings, title):

    pygame.init()

    # Prepare the Display
    display = pygame.display.set_mode((displaySettings.res_x, displaySettings.res_y))
    pygame.display.set_caption(title)

    # Return the Display
    displaySettings.surface = display
    return display


