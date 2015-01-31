# coding=utf-8

"""
Contains code relevant to rendering map lines to the map
"""
import pygame

from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


__author__ = 'Matt Eland'


class MapLine(MapSymbol):
    """
    Renders map paths to the screen with added contextual styling support
    """

    points = list()

    def __init__(self, lat=0, lng=0):  # We don't typically know lat / lng until we have points
        super(MapLine, self).__init__(lat, lng)

        self.points = list()
        self.screen_points = None

        # Points are manually copied during the transpose process

    def get_line_width(self):

        building = self.get_tag_value('building')

        if self.has_tag('highway'):

            value = self.get_tag_value('highway')

            if value in ('motoway', 'motorway'):
                return 5
            elif value in ('trunk', 'motorway_link'):
                return 4
            elif value == 'primary':
                return 3
            elif value == 'secondary':
                return 2

        elif self.has_tag_value('natural', 'water') or self.has_tag('water'):
            return 2

        elif self.has_tag('waterway'):
            return 3

        elif self.has_tag_value('natural', 'wood') or self.has_tag('wood'):
            return 2

        elif building:

            if building in ('residential', 'terrace', 'apartment', 'apartments'):
                return 0  # We're not going to render anything inside of these guy so just fill them

        return 1

    def render(self, display, map_context):

        # Render out the lines
        if self.screen_points and len(self.screen_points) > 1 and map_context.should_show_lines(self):

            self.has_lines = True
            color = self.get_color(display.color_scheme)
            width = self.get_line_width()

            if width <= 0:
                pygame.draw.polygon(display.surface, color, self.screen_points, width)
            else:
                pygame.draw.lines(display.surface, color, False, self.screen_points, width)

        super(MapLine, self).render(display, map_context)