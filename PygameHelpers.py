__author__ = 'Matt Eland'


import pygame


def build_font(size):
    return pygame.font.Font(None, size)


def init_pygame_graphics(display_settings, title):

    pygame.init()

    # Prepare the Display
    if display_settings.is_fullscreen:
        display = pygame.display.set_mode((display_settings.res_x, display_settings.res_y), pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((display_settings.res_x, display_settings.res_y))

    # Don't settle with that silly "pygame window" label
    pygame.display.set_caption(title)

    # Return the Display
    display_settings.surface = display
    return display


