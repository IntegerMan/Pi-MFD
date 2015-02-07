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
    white = (200, 200, 200)
    red = (200, 0, 0)
    yellow = (200, 200, 0)
    blue = (0, 0, 200)
    slight_blue = (150, 200, 200)
    green = (0, 200, 0)
    purple = (100, 0, 200)
    gray = (128, 128, 128)
    brown = (150, 86, 64)
    salmon = (200, 100, 100)
    greenish = (0, 150, 64)
    blueish = (0, 100, 200)
    pink = (200, 0, 200)
    khaki = (189, 183, 107)

    # Keyed Colors
    background = (0, 0, 0)
    foreground = (0, 255, 0)
    disabled = (0, 120, 0)
    detail = (128, 128, 128),
    highlight = (255, 255, 255)

    # Map Colors
    map_commercial = slight_blue
    map_automotive = blueish
    map_water = blueish
    map_private = yellow
    map_service = khaki
    map_infrastructure = khaki
    map_residential = greenish
    map_recreation = greenish
    map_vegetation = green
    map_unknown = pink
    map_emergency = red
    map_health = red
    map_public = salmon
    map_major_road = (85, 251, 167)
    map_government = purple
    map_pedestrian = brown
    map_structural = gray

    def __init__(self, name, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255),
                 detail=(128, 128, 128), disabled=(0, 120, 0)):
        self.background = background
        self.foreground = foreground
        self.disabled = disabled
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
        target.disabled = self.disabled
        target.name = self.name
        return target

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
                           disabled=(0, 100, 0),
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
                           disabled=(0, 80, 80),
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
                           disabled=(0, 60, 120),
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
                           disabled=(70, 70, 70),
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
                           disabled=(80, 0, 0),
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
                           disabled=(110, 90, 35),
                           detail=(128, 128, 128),
                           highlight=(255, 201, 14))

