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
        color = (85, 251, 167)
        offset = self.display.get_content_start_pos()

        available_y = self.display.res_y - (offset[1] * 2)
        size = (available_y, available_y)
        center = ((self.display.res_x / 2.0) - 10, (self.display.res_y / 2.0) - 10)

        ways = self.map.transpose_ways(size, center)

        for way in ways:
            # TODO: Use the rendering helpers
            pygame.draw.lines(
                self.display.surface,
                color,
                False,
                way,
                1
            )

            # for tag in self.map.transpose_tags((self.size, self.size), (self.size / 2, self.size / 2)):

# self.map.tags[tag[0]] = (tag[1] + self.map.position[0], tag[2] + self.map.position[1], tag[3])
