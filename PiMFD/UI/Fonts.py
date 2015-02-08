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
    weather = None
    map1 = None
    map2 = None
    map3 = None
    map4 = None
    nato_equip = None

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

        self.normal = FontInfo(self.options.font_name, scale_factor * 3)
        self.weather = FontInfo('Fonts/WeatherIcons.ttf', scale_factor * 4)
        self.small = FontInfo(self.options.font_name, small_font_size)
        self.map1 = FontInfo('Fonts/mapz01.ttf', scale_factor * 3)
        self.map2 = FontInfo('Fonts/mapz02.ttf', scale_factor * 3)
        self.map3 = FontInfo('Fonts/mapz03.ttf', scale_factor * 3)
        self.map4 = FontInfo('Fonts/mapz04.ttf', scale_factor * 3)
        self.nato_equip = FontInfo('Fonts/app6a13.ttf', scale_factor * 3)


