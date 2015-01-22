# coding=utf-8

"""
Contains chart-related widgets
"""
from pygame.rect import Rect

from PiMFD.UI.Rendering import draw_horizontal_line, draw_vertical_line, draw_rectangle
from PiMFD.UI.WidgetBase import UIWidget


__author__ = 'Matt Eland'


class BoxChart(UIWidget):
    """
    A widget that renders a box chart indicating a range of values.
    """

    range_low = 0
    range_high = 100
    value_low = 0
    value_high = 0

    width = 100
    height = 8

    ticks = None

    def __init__(self, display, page):
        super(BoxChart, self).__init__(display, page)

        self.ticks = list()

    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """

        # Standardize our dimensions
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.set_dimensions_from_rect(self.rect)

        color = self.display.color_scheme.foreground
        highlight = self.display.color_scheme.highlight

        # Draw the basic skeleton of the control
        draw_vertical_line(self.display, color, self.left, self.top, self.bottom)
        draw_vertical_line(self.display, color, self.right, self.top, self.bottom)
        draw_horizontal_line(self.display, color, self.left, self.right, self.top + 4)

        # TODO: a lot of this math should probably be hardened to protect against bad values

        # We need to do a bit of math to figure out how to position items
        range_increment = self.width / float(self.range_high - self.range_low)

        # Draw any tick marks present
        for tick in self.ticks:
            tick_offset = (tick - self.range_low) * range_increment
            draw_vertical_line(self.display, color, self.left + tick_offset, self.top, self.bottom)

        # Draw the box of the control
        low_x = (self.value_low - self.range_low) * range_increment
        high_x = (self.value_high - self.range_low) * range_increment
        chart_rect = Rect(self.left + low_x, self.top + 2, high_x - low_x, self.height - 3)
        draw_rectangle(self.display, highlight, chart_rect, width=0)

        # Return our dimensions
        return self.rect


