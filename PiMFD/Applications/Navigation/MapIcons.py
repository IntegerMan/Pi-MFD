# coding=utf-8

"""
A file containing multiple unique procedural iconographic representations of locations
"""
from PiMFD.UI.Rendering import draw_horizontal_line, draw_vertical_line

__author__ = 'Matt Eland'


class MapIcon(object):
    """
    Represents an icon that can be rendered to the map.
    """

    def render(self, display, color, pos, half_size):
        """
        Renders the icon to the display
        :param display: The display manager
        :param color: The color
        :param pos: The center point of the shape
        :param half_size: Half the size of the shape
        """
        pass


class ChairIcon(MapIcon):
    """
    Renders a chair from side perspective.
    Used as an icon for furniture stores
    """

    def render(self, display, color, pos, half_size):
        """
        Renders the icon to the display
        :param display: The display manager
        :param color: The color
        :param pos: The center point of the shape
        :param half_size: Half the size of the shape
        """

        x = pos[0]
        y = pos[1]

        x_offset = 2
        y_offset = 3

        draw_horizontal_line(display, color, x - x_offset, x + x_offset, y)
        draw_vertical_line(display, color, x - x_offset, y + y_offset, y - y_offset)
        draw_vertical_line(display, color, x + x_offset, y + y_offset, y)

