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
        return self.font.render(text, antialias, color, background)

    def measure(self, text):
        return self.font.size(text)


class FontManager(object):
    """
    Contains information on multiple fonts
    """

    options = None

    normal = None
    small = None
    weather = None
    map1 = None
    map2 = None
    map3 = None
    map4 = None

    def __init__(self, options):
        super(FontManager, self).__init__()

        self.options = options

    def load_fonts(self):
        """
        Loads fonts into the object
        """

        self.normal = FontInfo(self.options.font_name, 24)
        self.weather = FontInfo('Fonts/WeatherIcons.ttf', 32)
        self.small = FontInfo(self.options.font_name, 12)


