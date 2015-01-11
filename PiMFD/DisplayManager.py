from PiMFD import start_mfd
from PiMFD.ColorScheme import ColorSchemes

__author__ = 'Matt Eland'


class DisplayManager(object):
    """Contains information and functions related to the drawing dimensions of the application window as well as the drawing surface."""

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        pass

    def start_mfd(self, app_options):
        start_mfd(self, app_options)

    res_x = 800
    res_y = 480

    padding_x = 8
    padding_y = 8

    surface = None

    is_fullscreen = False

    frames_per_second = 30

    color_scheme = ColorSchemes.military

    font_size_normal = 24
    font_normal = None

    def get_content_start_y(self):
        return (self.padding_y * 2) + self.font_size_normal

    pass

    def render_text(self, font, text, left, top, color, background=None):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(top=top, left=left)

        if background is not None:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect

    def render_text_centered(self, font, text, left, top, color, background=None):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(left, top))

        if background is not None:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect