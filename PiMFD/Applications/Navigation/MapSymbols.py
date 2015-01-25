# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from pygame.rect import Rect

from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.Applications.Navigation.MapIcons import ChairIcon
from PiMFD.UI.Rendering import render_text, render_circle, render_rectangle, render_text_centered, render_diamond


__author__ = 'Matt Eland'


class SymbolBackShape(object):
    """
    The backing of a symbol
    """

    none = 0
    square = 1
    circle = 2
    diamond = 3
    triangle = 4
    dot = 5
    square_top_triangle = 6
    bullseye = 7
    traffic_stop = 8
    double_circle = 9


class MapSymbol(MapLocation):
    """
    Renders a map symbol to the screen
    """

    def __init__(self, lat, lng, location):
        super(MapSymbol, self).__init__(lat, lng)

        self.tags = location.tags
        self.name = location.name
        self.id = location.id

    def get_font_text_and_color(self, display):
        """
        Returns the font to use to display, the text to render, and the color to use
        :param display: The DisplayManager
        :return: the font to use to display, the text to render, and the color to use
        """

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
        # Circle - Government / Services / Public
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

        shape_width = 1
        shape_size = 20

        # Set shape. Python 2.7 doesn't have enum support so I'm using a placeholder class for that.
        shape = SymbolBackShape()
        style = shape.circle

        shape_shop = shape.diamond
        shape_service = shape.square
        shape_public = shape.circle
        shape_food = shape.circle

        icon_renderer = None

        font = display.fonts.small

        pos = (int(self.lat), int(self.lng))

        # Colors
        cs = display.color_scheme
        highlight = cs.highlight
        foreground = cs.foreground
        color = highlight
        text_color = color

        left_text = None
        right_text = self.abbreviate(self.name)
        bottom_text = None
        inner_text = None

        # Modify our display parameters based on what our context is

        if self.has_tag_value('highway', 'traffic_signals'):
            style = shape.traffic_stop
            right_text = None
        elif self.has_tag_value('amenity', 'pharmacy'):
            style = shape_shop
            color = cs.map_health
            inner_text = 'RX'
        elif self.has_tag_value('shop', 'beauty'):
            style = shape_service
            color = cs.map_commercial
            inner_text = 'SPA'
        elif self.has_tag_value('amenity', 'fuel'):
            style = shape_shop
            color = cs.map_commercial
            inner_text = 'GAS'
        elif self.has_tag_value('amenity', 'school'):
            style = shape_public  # Though this could be service if private school
            color = cs.map_public
            inner_text = 'EDU'
        elif self.has_tag_value('shop', 'furniture'):
            style = shape_shop
            color = cs.map_commercial
            icon_renderer = ChairIcon()
        elif self.has_tag_value('shop', 'sports'):
            style = shape_shop
            color = cs.map_public
            inner_text = 'ATH'
        elif self.has_tag_value('amenity', 'place_of_worship'):
            # TODO: Handle religion / denomination
            style = shape_service
            color = cs.map_private
            inner_text = 'REL'
        elif self.has_tag_value('amenity', 'restaurant'):
            # TODO: Handle cuisine
            style = shape_food
            color = cs.map_commercial
            inner_text = 'EAT'
        elif self.has_tag_value('amenity', 'fast_food'):
            # TODO: Handle cuisine
            style = shape_food
            color = cs.map_commercial
            inner_text = 'FF'

        half_size = shape_size / 2

        if style == shape.circle:
            render_circle(display, color, pos, half_size + 2, shape_width)

        elif style == shape.square:
            render_rectangle(display, color, Rect(self.lat - half_size, self.lng - half_size, shape_size, shape_size),
                             shape_width)

        elif style == shape.diamond:
            render_diamond(display, color, pos, half_size + 2, shape_width)

        elif style == shape.double_circle:
            render_circle(display, color, pos, half_size + 2, shape_width)
            render_circle(display, color, pos, half_size, shape_width)

        elif style == shape.traffic_stop:
            render_circle(display, cs.red, pos, 4, 0)
            render_circle(display, cs.yellow, pos, 3, 0)
            render_circle(display, cs.green, pos, 1, 0)

        if icon_renderer:
            icon_renderer.render(display, color, pos, half_size)

        if inner_text:
            render_text_centered(display,
                                 font,
                                 inner_text,
                                 self.lat,
                                 self.lng - (font.measure(inner_text)[1] / 2.0),
                                 color)

        if right_text:
            render_text(display,
                        font,
                        right_text,
                        self.lat + half_size + 3,
                        self.lng - (font.measure(right_text)[1] / 2.0),
                        text_color)

        if bottom_text:
            render_text_centered(display,
                                 font,
                                 bottom_text,
                                 self.lat,
                                 self.lng + half_size + 3,  # + (font.measure(bottom_text)[1] / 2.0),
                                 color)

