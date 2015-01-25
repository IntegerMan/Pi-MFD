# coding=utf-8

from PiMFD.UI.Rendering import render_text_centered


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


        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        available_x = self.display.res_x
        available_y = self.display.res_y
        max_available = max(available_y, available_x)
        size = (max_available, max_available)

        center = ((self.display.res_x / 2.0), (self.display.res_y / 2.0))

        # Translate the various curves, etc. into their appropraite screen positions
        ways = self.map.transpose_ways(size, center)
        symbols = self.map.transpose_locations(size, center)

        font_y_offset = (self.display.fonts.small.size / 2.0)

        # Render the Roads
        for way in ways:
            way.render(self.display)

        # We want to render ourselves on the map
        # TODO: Treat this as a symbol
        render_text_centered(self.display,
                             self.display.fonts.small,
                             'ME', center[0], center[1] - font_y_offset,
                             self.display.color_scheme.highlight)

        # Render the other awesome things
        for symbol in symbols:
            symbol.render(self.display)
