# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from pygame.rect import Rect

from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.UI.Rendering import render_text, render_circle, render_rectangle, render_text_centered


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

        # In general symbols will be composed of the following components
        #
        # Main Shape
        # Square - Amenities
        #   Circle - Government / Services / Public
        #   Diamond - Shops
        #   Square w. Diamond Top - Residential
        #
        # Text
        #   Right Text - Name
        #   Bottom Text - Augmented Data for current map mode
        #   Inner Text - Symbol Code
        #   Left Text - Augmented Data for current map mode
        #
        # Color
        #   Most items will retain default
        #   Red - Health
        #   Blue - Leisure
        #   Green - Government
        #   Purple - Corporate
        #   Yellow - Utility

        draw_square = False
        draw_circle = True
        shape_width = 1
        shape_size = 20

        red = (200, 0, 0)
        purple = (100, 0, 200)

        font, text, color = self.get_font_text_and_color(display)

        text_color = color

        left_text = None
        right_text = self.name  # TODO: Use an ID here
        bottom_text = self.name
        inner_text = None

        # Modify our display parameters based on what our context is

        if self.has_tag_value('highway', 'traffic_signals'):
            shape_width = 0
            shape_size = 10
            color = red
            right_text = None
        elif self.has_tag_value('amenity', 'pharmacy'):
            color = red
            draw_square = True  # TODO: Diamond?
            draw_circle = False
            inner_text = 'RX'
        elif self.has_tag_value('shop', 'beauty'):
            draw_square = True  # TODO: Diamond?
            draw_circle = False
            inner_text = 'SPA'
        elif self.has_tag_value('amenity', 'fuel'):
            inner_text = 'GAS'
        elif self.has_tag_value('amenity', 'school'):
            inner_text = 'EDU'
        elif self.has_tag_value('shop', 'furniture'):
            draw_square = True
            draw_circle = False
            inner_text = 'FRN'
        elif self.has_tag_value('shop', 'sports'):
            draw_square = True
            draw_circle = False
            inner_text = 'ATH'
        elif self.has_tag_value('amenity', 'place_of_worship'):
            # TODO: Handle denomination / religion
            color = purple
            inner_text = 'REL'
        elif self.has_tag_value('amenity', 'restaurant'):
            # TODO: Handle cuisine
            draw_square = True
            draw_circle = False
            inner_text = 'EAT'
        elif self.has_tag_value('amenity', 'fast_food'):
            # TODO: Handle cuisine
            draw_square = True
            draw_circle = False
            inner_text = 'FFD'

        half_size = shape_size / 2

        if draw_circle:
            render_circle(display, color, (int(self.lat), int(self.lng)), half_size, shape_width)

        if draw_square:
            render_rectangle(display, color, Rect(self.lat - half_size, self.lng - half_size, shape_size, shape_size),
                             shape_width)

        if inner_text:
            render_text_centered(display,
                                 font,
                                 inner_text,
                                 self.lat,
                                 self.lng - (font.measure(text)[1] / 2.0),
                                 color)

        if right_text:
            render_text(display,
                        font,
                        right_text,
                        self.lat + half_size + 2,
                        self.lng - (font.measure(text)[1] / 2.0),
                        text_color)


