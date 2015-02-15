# coding=utf-8

"""
Contains chart-related widgets
"""
from pygame.rect import Rect

from PiMFD.UI.Rendering import draw_horizontal_line, draw_vertical_line, render_rectangle
from PiMFD.UI.WidgetBase import UIWidget


__author__ = 'Matt Eland'


class BoxChart(UIWidget):

    """
    A widget that renders a box chart indicating a range of values.
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.MFDPage.MFDPage
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

    def arrange(self):
        self.desired_size = self.width, self.height

        return super(BoxChart, self).arrange()

    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """

        # Standardize our dimensions
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.set_dimensions_from_rect(self.rect)

        color = self.display.color_scheme.foreground

        if self.is_highlighted:
            highlight = self.display.color_scheme.highlight
        else:
            highlight = color

        # Draw the basic skeleton of the control
        draw_vertical_line(self.display, color, self.left, self.top, self.bottom)
        draw_vertical_line(self.display, color, self.right, self.top, self.bottom)
        draw_horizontal_line(self.display, color, self.left, self.right, self.top + 4)

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
        render_rectangle(self.display, highlight, chart_rect, width=0)

        # Return our dimensions
        return self.rect


class BarChart(UIWidget):
    """
    A widget that renders a bar chart indicating a single point value in a predicted range.
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.MFDPage.MFDPage
    """
    range_low = 0
    range_high = 100
    value = 0

    width = 100
    height = 8

    def __init__(self, display, page, value=0, range_low=0, range_high=100, width=100, height=8):
        super(BarChart, self).__init__(display, page)

        self.ticks = list()
        self.value = value
        self.range_low = range_low
        self.range_high = range_high
        self.width = width
        self.height = height

    def arrange(self):
        self.desired_size = self.width, self.height

        return super(BarChart, self).arrange()

    def render(self):
        """
        Renders the widget to the screen
        :return: The rect of the control as it was rendered
        """

        # Standardize our dimensions
        self.rect = Rect(self.pos[0], self.pos[1], self.width, self.height)
        self.set_dimensions_from_rect(self.rect)

        color = self.display.color_scheme.foreground

        if self.is_highlighted:
            color = self.display.color_scheme.highlight

        # Draw the basic skeleton of the control
        render_rectangle(self.display, color, self.rect)

        # We need to do a bit of math to figure out how to position items
        range_increment = self.width / float(self.range_high - self.range_low)

        # Draw the box of the control - unless we're below or at min-val
        if self.value > self.range_low:
            x = (min(self.value, self.range_high) - self.range_low) * range_increment
            chart_rect = Rect(self.left, self.top, x, self.height)
            render_rectangle(self.display, color, chart_rect, width=0)

        # Return our dimensions
        return self.rect

