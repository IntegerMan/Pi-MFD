# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.UI.Rendering import render_text_centered

__author__ = 'Matt Eland'


class MapSymbol(MapLocation):
    def __init__(self, lat, lng, location):
        super(MapSymbol, self).__init__(lat, lng)

        self.tags = location.tags
        self.name = location.name

    def render(self, display):
        render_text_centered(display,
                             display.font_small,
                             self.name.upper(),
                             self.lat,
                             self.lng - (display.font_size_small / 2.0),
                             display.color_scheme.highlight)


