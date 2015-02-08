# coding=utf-8

"""
A file containing multiple unique procedural iconographic representations of locations
"""
from pygame.rect import Rect

from PiMFD.Applications.Scheduling.Weather.WeatherData import get_condition_icon
from PiMFD.UI.Rendering import draw_horizontal_line, draw_vertical_line, render_text_centered, render_circle, \
    draw_full_arc, draw_left_arc, draw_right_arc


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


class WeatherIcon(MapIcon):
    code = -1

    def __init__(self, code):
        super(WeatherIcon, self).__init__()
        self.code = code

    def render(self, display, color, pos, half_size):
        """
        Renders the icon to the display
        :param display: The display manager
        :param color: The color
        :param pos: The center point of the shape
        :param half_size: Half the size of the shape
        """

        icon = get_condition_icon(self.code)
        size = display.fonts.weather.measure(icon)
        render_text_centered(display, display.fonts.weather, icon, pos[0], pos[1] - (size[1] / 2.0), color)


class PillIcon(MapIcon):
    """
    Renders a medical pill icon
    Used as an icon for pharmacies
    """

    def render(self, display, color, pos, half_size):
        """
        Renders the icon to the display
        :param display: The display manager
        :param color: The color
        :param pos: The center point of the shape
        :param half_size: Half the size of the shape
        """

        y_size = 3
        x_size = 6

        # left arc of the pill
        rect = Rect(pos[0] - x_size, pos[1] - y_size, x_size, (y_size * 2))
        draw_left_arc(display, rect, color)

        # right arc of the pill
        rect = Rect(pos[0], pos[1] - y_size, x_size, (y_size * 2))
        draw_right_arc(display, rect, color)

        # Draw supports / center line for the pill
        draw_vertical_line(display, color, pos[0], pos[1] - y_size, pos[1] + y_size)
        draw_horizontal_line(display, color, pos[0] - x_size + 3, pos[0] + x_size - 3, pos[1] - y_size)
        draw_horizontal_line(display, color, pos[0] - x_size + 3, pos[0] + x_size - 3, pos[1] + y_size)


class EyeIcon(MapIcon):
    """
    Renders an open eye
    Used as an icon for surveillance and optomitrists
    """

    def render(self, display, color, pos, half_size):
        """
        Renders the icon to the display
        :param display: The display manager
        :param color: The color
        :param pos: The center point of the shape
        :param half_size: Half the size of the shape
        """

        y_size = half_size / 2.0

        rect = Rect(pos[0] - half_size, pos[1] - y_size, (half_size * 2), (y_size * 2))
        draw_full_arc(display, rect, color)

        # Finish with a filled circle
        render_circle(display, color, pos, y_size - 1)


class FoodIcon(MapIcon):
    """
    Renders a fork from a side perspective.
    Used as an icon for restaraunts
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
        y_offset = 5

        fork_x = x + 2
        knife_x = x - 3
        fork_y = y
        knife_y = y

        # Render the Fork
        draw_vertical_line(display, color, fork_x, fork_y + y_offset, fork_y - y_offset)
        draw_horizontal_line(display, color, fork_x - x_offset, fork_x + x_offset, fork_y - 2)
        draw_vertical_line(display, color, fork_x - x_offset, fork_y - y_offset, fork_y - 2)
        draw_vertical_line(display, color, fork_x + x_offset, fork_y - y_offset, fork_y - 2)

        # Render the Knife
        draw_vertical_line(display, color, knife_x, knife_y - y_offset, knife_y + y_offset)
        draw_vertical_line(display, color, knife_x - 1, knife_y - y_offset + 1, knife_y)
