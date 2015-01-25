# coding=utf-8
"""
Color Scheme information
"""
__author__ = 'Matt Eland'


class ColorScheme(object):
    """
    A color scheme
    :type background: tuple RGB values indicating the background
    :type foreground: tuple RGB values for most text and buttons
    :type highlight: tuple RGB values for highlighted text
    """

    # Color Constants - Shared values that aren't necessarily themed. Used for maps
    red = (200, 0, 0)
    yellow = (200, 200, 0)
    blue = (0, 0, 200)
    green = (0, 200, 0)
    purple = (100, 0, 200)
    gray = (128, 128, 128)
    brown = (150, 86, 64)
    greenish = (0, 150, 64)
    blueish = (0, 64, 150)

    def __init__(self, name, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255),
                 detail=(128, 128, 128)):
        self.background = background
        self.foreground = foreground
        self.highlight = highlight
        self.detail = detail
        self.name = name
        pass

    def clone_to(self, target):
        """
        Clones values in this object to other objects
        :param target: The object to receive the values
        :return: The target with its adjusted files.
        """
        target.background = self.background
        target.foreground = self.foreground
        target.detail = self.detail
        target.highlight = self.highlight
        target.name = self.name
        return target

    background = (0, 0, 0)
    foreground = (0, 255, 0)
    detail = (128, 128, 128),
    highlight = (255, 255, 255)
    name = None

    def get_focus_color(self, is_focused):
        """
        Gets the color to use for rendering a foreground depending on if the control is focused or not
        :param is_focused: Whether the control is focused
        :return: The color to use. This will be highlight for focused and foreground for unfocused
        """
        if is_focused:
            return self.highlight
        else:
            return self.foreground


class ColorSchemes(object):
    """
    A collection of available color schemes.
    """

    @staticmethod
    def get_green_color_scheme():
        """
        Gets a green-based color scheme resembling military avionics displays
        :return: A green-based color scheme resembling military avionics displays
        """
        return ColorScheme(name='Green',
                           background=(0, 42, 0),
                           foreground=(0, 210, 0),
                           detail=(85, 251, 167),
                           highlight=(230, 230, 230))

    @staticmethod
    def get_cyan_color_scheme():
        """
        Gets a cyan-based color scheme
        :return: A cyan-based color scheme
        """
        return ColorScheme(name='Cyan',
                           background=(0, 0, 32),
                           foreground=(0, 170, 170),
                           detail=(128, 128, 128),
                           highlight=(0, 0, 255))

    @staticmethod
    def get_blue_color_scheme():
        """
        Gets an ice-blue-based color scheme
        :return: An ice-blue-based color scheme
        """
        return ColorScheme(name='Blue',
                           background=(0, 0, 32),
                           foreground=(0, 128, 255),
                           detail=(128, 128, 128),
                           highlight=(255, 255, 255))

    @staticmethod
    def get_white_color_scheme():
        """
        Gets a white / monochrome-based color scheme
        :return: A white / monochrome-based color scheme
        """
        return ColorScheme(name='White',
                           background=(0, 0, 0),
                           foreground=(150, 150, 150),
                           detail=(128, 128, 128),
                           highlight=(255, 255, 255))

    @staticmethod
    def get_red_color_scheme():
        """
        Gets a red-based color scheme
        :return: A red-based color scheme
        """
        return ColorScheme(name='Red',
                           background=(32, 0, 0),
                           foreground=(170, 0, 0),
                           detail=(128, 128, 128),
                           highlight=(255, 0, 0))

    @staticmethod
    def get_amber_color_scheme():
        """
        Gets an amber-based color scheme
        :return: A amber-based color scheme
        """
        return ColorScheme(name='Amber',
                           background=(63, 47, 20),
                           foreground=(231, 176, 75),
                           detail=(128, 128, 128),
                           highlight=(255, 201, 14))

