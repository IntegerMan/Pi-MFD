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

        if self.has_tag('railway'):
            color = (128, 128, 128)
        else:
            color = default_color

        # TODO: Use the rendering helpers
        pygame.draw.lines(display.surface, color, False, self.points, 1)


6