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
    
    # Status Colors
    caution = (170, 170, 0)
    caution_bg = (40, 40, 0)
    critical = (170, 0, 0)
    critical_bg = (40, 0, 0)

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

    def __str__(self):

        if self.name:
            return self.name

        return super(ColorScheme, self).__str__()


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
        Gets a green-based color scheme
        :return: A green-based color scheme resembling military avionics displays
        """
        return ColorScheme(name='Green',
                           background=(0, 42, 0),
                           foreground=(0, 210, 0),
                           disabled=(0, 100, 0),
                           detail=(85, 251, 167),
                           highlight=(230, 230, 230))

    @staticmethod
    def get_avionics_color_scheme():
        """
        Gets a green-based color scheme resembling military avionics displays
        :return: A green-based color scheme resembling military avionics displays
        """
        return ColorScheme(name='Avoionics',
                           background=(13, 36, 11),
                           foreground=(0, 194, 0),
                           disabled=(0, 90, 0),
                           detail=(0, 123, 0),
                           highlight=(0, 250, 0))

    @staticmethod
    def get_terminal_color_scheme():
        """
        Gets a green-based color scheme resembling a terminal display
        :return: A green-based color scheme resembling military avionics displays
        """
        return ColorScheme(name='Terminal',
                           background=(1, 19, 1),
                           foreground=(0, 150, 66),
                           disabled=(0, 75, 33),
                           detail=(0, 69, 20),
                           highlight=(182, 179, 174))

    @staticmethod
    def get_cyan_color_scheme():
        """
        Gets a cyan-based color scheme
        :return: A cyan-based color scheme
        """
        return ColorScheme(name='Cyan',
                           background=(0, 32, 32),
                           foreground=(0, 170, 170),
                           disabled=(0, 80, 80),
                           detail=(128, 128, 128),
                           highlight=(0, 255, 255))

    @staticmethod
    def get_tactical_color_scheme():
        """
        Gets a tactical blue / cyan color scheme
        :return: A tactical blue / cyan color scheme
        """
        return ColorScheme(name='Tactical',
                           background=(16, 29, 44),
                           foreground=(104, 147, 152),
                           disabled=(32, 60, 68),
                           detail=(51, 98, 106),
                           highlight=(203, 203, 191))

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
                           background=(39, 38, 35),
                           foreground=(247, 241, 158),
                           disabled=(128, 116, 39),
                           detail=(164, 156, 71),
                           highlight=(249, 245, 250))

    @staticmethod
    def get_gold_color_scheme():
        """
        Gets an amber-based color scheme
        :return: A amber-based color scheme
        """
        return ColorScheme(name='Gold',
                           background=(30, 26, 4),
                           foreground=(231, 176, 75),
                           disabled=(110, 90, 35),
                           detail=(128, 128, 128),
                           highlight=(250, 255, 51))

    @classmethod
    def get_color_schemes(cls):
        """
        :rtype : list
        """
        schemes = [cls.get_green_color_scheme(),
                   cls.get_avionics_color_scheme(),
                   cls.get_terminal_color_scheme(),
                   cls.get_blue_color_scheme(),
                   cls.get_amber_color_scheme(),
                   cls.get_gold_color_scheme(),
                   cls.get_cyan_color_scheme(),
                   cls.get_tactical_color_scheme(),
                   cls.get_red_color_scheme(),
                   cls.get_white_color_scheme()]

        return schemes

