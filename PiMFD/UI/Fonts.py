# coding=utf-8

"""
A class for managing multiple fonts
"""
import pygame

__author__ = 'Matt Eland'


class FontInfo(object):
    """
    A wrapper around Font that lets us put size next to it for convenience
    """

    font = None
    size = None
    name = None

    def __init__(self, font_name, size):
        super(FontInfo, self).__init__()

        self.font = pygame.font.Font(font_name, size)
        self.name = font_name
        self.size = size

    def render(self, text, antialias, color, background=None):
        """
        Passthrough to the font for rendering for convenience / readability
        """
        # Explicitly specifying background when none caused issues on some machines
        if background:
            return self.font.render(text, antialias, color, background)
        else:
            return self.font.render(text, antialias, color)

    def measure(self, text):
        return self.font.size(text)


class FontManager(object):
    """
    Contains information on multiple fonts
    """

    options = None

    normal = None
    small = None
    list = None
    weather = None

    def __init__(self, options):
        """

        :type options: PiMFD.Options.MFDAppOptions
        """
        super(FontManager, self).__init__()

        self.options = options

    def load_fonts(self):
        """
        Loads fonts into the object
        """

        scale_factor = self.options.font_scaling
        small_font_size = max(scale_factor, self.options.min_font_size)
        list_font_size = scale_factor * 2

        self.normal = FontInfo(self.options.font_name, scale_factor * 3)
        self.small = FontInfo(self.options.font_name, small_font_size)
        self.list = FontInfo(self.options.font_name, list_font_size)
        
        self.weather = FontInfo('Fonts/WeatherIcons.ttf', scale_factor * 4)

