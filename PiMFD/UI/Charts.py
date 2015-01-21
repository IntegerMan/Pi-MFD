# coding=utf-8

"""
Contains chart-related widgets
"""
from pygame.rect import Rect

from PiMFD.UI.Rendering import draw_horizontal_line, draw_vertical_line
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

    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """

        # Standardize our dimensions
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.set_dimensions_from_rect(self.rect)

        color = self.display.color_scheme.foreground

        # Draw the basic skeleton of the control
        draw_vertical_line(self.display, color, self.left, self.top, self.bottom)
        draw_vertical_line(self.display, color, self.right, self.top, self.bottom)
        draw_horizontal_line(self.display, color, self.left, self.right, self.top + 4)

        # TODO: Draw the box of the control

        # Return our dimensions
        return self.rect


