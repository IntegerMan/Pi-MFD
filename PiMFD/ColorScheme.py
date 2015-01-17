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
    :type interlace_color: tuple RGB values indicating the alternate rows of the background or None for no interlacing.
    """

    def __init__(self, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255), interlace_color=(2, 2, 2)):
        self.background = background
        self.foreground = foreground
        self.highlight = highlight
        self.interlace_color = interlace_color
        pass

    def clone_to(self, target):
        """
        Clones values in this object to other objects
        :param target: The object to receive the values
        :return: The target with its adjusted files.
        """
        target.background = self.background
        target.foreground = self.foreground
        target.highlight = self.highlight
        target.interlace_color = self.interlace_color
        return target

    background = (0, 0, 0)
    interlace_color = (2, 2, 2)
    foreground = (0, 255, 0)
    highlight = (255, 255, 255)

    pass


class ColorSchemes(object):
    """
    A collection of available color schemes.
    """

    @staticmethod
    def get_military_color_scheme():
        """
        Gets a green based color scheme resembling military avionics displays
        :return: A green based color scheme resembling military avionics displays
        """
        return ColorScheme(background=(0, 8, 0),
                           foreground=(0, 255, 0),
                           highlight=(255, 255, 255),
                           interlace_color=(0, 32, 0))

    @staticmethod
    def get_cyan_color_scheme():
        """
        Gets a cyan based color scheme
        :return: A cyan based color scheme
        """
        return ColorScheme(background=(0, 0, 32),
                           foreground=(0, 170, 170),
                           highlight=(0, 0, 255),
                           interlace_color=(0, 0, 8))

    @staticmethod
    def get_monochrome_color_scheme():
        """
        Gets a monochrome based color scheme
        :return: A monochrome based color scheme
        """
        return ColorScheme(background=(0, 0, 0),
                           foreground=(150, 150, 150),
                           highlight=(255, 255, 255),
                           interlace_color=(24, 24, 24))


