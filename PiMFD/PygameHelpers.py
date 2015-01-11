import pygame

__author__ = 'Matt Eland'

# TODO: I'd like this collection of helpers to not exist


def grab_dimensions_from_current_resolution(display_settings):
    info = pygame.display.Info()
    display_settings.res_x = info.current_w
    display_settings.res_y = info.current_h


def init_pygame_graphics(display_settings, title, font_name):

    pygame.init()

    # If we haven't configured width / height, grab them from the current resolution
    if display_settings.res_x is None or display_settings.res_x < 8 or display_settings.res_y is None or display_settings.res_y < 8:
        grab_dimensions_from_current_resolution(display_settings)

    # Prepare the Display
    if display_settings.is_fullscreen:
        display = pygame.display.set_mode((display_settings.res_x, display_settings.res_y), pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode((display_settings.res_x, display_settings.res_y))

    # Don't settle with that silly "pygame window" label
    pygame.display.set_caption(title)

    display_settings.font_normal = pygame.font.Font(font_name, display_settings.font_size_normal)

    # Return the Display
    display_settings.surface = display
    return display


