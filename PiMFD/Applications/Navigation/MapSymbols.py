# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from pygame.rect import Rect

from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.UI.Rendering import render_text, render_circle, render_rectangle


__author__ = 'Matt Eland'


class MapSymbol(MapLocation):
    """
    Renders a map symbol to the screen
    """

    def __init__(self, lat, lng, location):
        super(MapSymbol, self).__init__(lat, lng)

        self.tags = location.tags
        self.name = location.name

    def get_tags(self, name):

        for tag in self.tags:
            if tag[0] == name:
                yield tag

    def has_tag_value(self, name, value):

        for tag in self.get_tags(name):
            if tag[1] == value:
                return True

        return False

    def get_font_text_and_color(self, display):
        """
        Returns the font to use to display, the text to render, and the color to use
        :param display: The DisplayManager
        :return: the font to use to display, the text to render, and the color to use
        """

        highlight = display.color_scheme.highlight
        foreground = display.color_scheme.highlight

        return display.fonts.small, self.name.upper(), display.color_scheme.highlight

    def render(self, display):
        """
        Renders the symbol to the screen.
        :param display: The display manager
        """

        draw_square = False
        draw_circle = True
        shape_width = 1
        shape_size = 10

        red = (150, 0, 0)

        font, text, color = self.get_font_text_and_color(display)

        # Modify our display parameters based on what our context is

        if self.has_tag_value('highway', 'traffic_signals'):
            draw_circle = False
            draw_square = True
            shape_width = 0
            shape_size = 8
            color = red
            text = None
        elif self.has_tag_value('amenity', 'pharmacy'):
            color = red

        half_size = shape_size / 2

        if draw_circle:
            render_circle(display, color, (int(self.lat), int(self.lng)), half_size, shape_width)

        if draw_square:
            render_rectangle(display, color, Rect(self.lat - half_size, self.lng - half_size, shape_size, shape_size),
                             shape_width)

        if text:
            render_text(display,
                        font,
                        text,
                        self.lat + 8,
                        self.lng - (font.measure(text)[1] / 2.0),
                        color)


