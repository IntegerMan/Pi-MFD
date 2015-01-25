# coding=utf-8

"""
Contains code relevant to rendering map lines to the map
"""
import pygame

from PiMFD.Applications.Navigation.MapEntities import MapPath


__author__ = 'Matt Eland'


class MapLine(MapPath):
    """
    Renders map paths to the screen with added contextual styling support
    """

    def __init__(self, path):
        super(MapLine, self).__init__(path.lat, path.lng)

        self.id = path.id
        self.tags = path.tags

        # Points are manually copied during the transpose process

    def render(self, display):

        cs = display.color_scheme
        default_color = cs.detail

        width = 1

        if self.has_tag('railway'):
            color = cs.gray

        elif self.has_tag('highway'):

            value = self.get_tag_value('highway')

            color = default_color

            if value == 'motoray':
                width = 5
            elif value == 'trunk':
                width = 4
            elif value == 'primary':
                width = 3
            elif value == 'secondary':
                width = 2
            elif value == 'unclassified':
                width = 1
            elif value == 'residential':
                width = 1
            elif value == 'path':
                width = 1
                color = cs.brown
            elif value == 'service':
                width = 1
                color = cs.map_private

            # If it's got a bridge, we'll handle it a bit differently
            if self.has_tag_value('bridge', 'yes'):
                color = cs.white

        elif self.has_tag_value('boundary', 'administrative'):
            color = cs.purple  # Purple
        elif self.has_tag_value('natural', 'water') or self.has_tag('water'):
            color = cs.blueish
            width = 0
        elif self.has_tag_value('leisure', 'park'):
            color = cs.greenish
            width = 1  # I can't close this because that can hide things inside like playgrounds
        elif self.has_tag_value('leisure', 'pitch'):
            # TODO: Take sport into account?
            color = cs.greenish
            width = 0
        elif self.has_tag_value('leisure', 'playground'):
            color = cs.brown
            width = 0
        else:
            color = cs.red

        # TODO: Use the rendering helpers
        if width <= 0:
            pygame.draw.polygon(display.surface, color, self.points, width)
        else:
            pygame.draw.lines(display.surface, color, False, self.points, width)


6