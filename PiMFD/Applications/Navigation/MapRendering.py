# coding=utf-8
import pygame

__author__ = 'Matt Eland'


class MapRenderer(object):  # TODO: Maybe this should be a UIWidget?
    """
    A class used to render a Map object
    """

    def __init__(self, map, display, size=200):
        self.map = map
        self.display = display
        self.size = size

    def render(self):
        color = self.display.color_scheme.detail
        offset = self.display.get_content_start_pos()

        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        available_x = self.display.res_x - (offset[0] * 2)
        available_y = self.display.res_y - (offset[1] * 2)
        max_available = max(available_y, available_x)
        size = (max_available, max_available)

        center = ((self.display.res_x / 2.0) - 10, (self.display.res_y / 2.0) - 10)

        # Translate the various curves, etc. into their appropraite screen positions
        ways = self.map.transpose_ways(size, center)

        for way in ways:
            # TODO: Use the rendering helpers
            # TODO: Render to a seperate surface so I can clip easily
            pygame.draw.lines(self.display.surface, color, False, way, 1)

            # for tag in self.map.transpose_tags((self.size, self.size), (self.size / 2, self.size / 2)):
            # self.map.tags[tag[0]] = (tag[1] + self.map.position[0], tag[2] + self.map.position[1], tag[3])
