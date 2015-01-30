# coding=utf-8

"""
Map Contexts are used to provide contextual rendering and filtering information to the map as it is rendered
"""

__author__ = 'Matt Eland'


class MapZooms(object):
    """
    An enum-style collection of supported zoom levels
    """
    large = 0.02
    medium = 0.0125
    local = 0.0075
    neighborhood = 0.0025

class MapContext(object):
    app = None

    zooms = MapZooms()
    map_zoom = zooms.local

    def __init__(self, app):
        super(MapContext, self).__init__()

        self.app = app

    def zoom_in(self):
        if self.map_zoom == self.zooms.large:
            self.map_zoom = self.zooms.medium
        elif self.map_zoom == self.zooms.medium:
            self.map_zoom = self.zooms.local
        elif self.map_zoom == self.zooms.local:
            self.map_zoom = self.zooms.neighborhood
        else:
            return False

        return True

    def zoom_out(self):
        if self.map_zoom == self.zooms.neighborhood:
            self.map_zoom = self.zooms.local
        elif self.map_zoom == self.zooms.local:
            self.map_zoom = self.zooms.medium
        elif self.map_zoom == self.zooms.medium:
            self.map_zoom = self.zooms.large
        else:
            return False

        return True


    def should_show_lines(self, entity):
        return True

    def should_show_shapes(self, entity):
        return True

    def should_show_right_text(self, entity):

        if self.map_zoom <= MapZooms.local:
            return True
        else:
            return False

    def should_show_left_text(self, entity):
        return self.should_show_right_text(entity)

    def should_show_bottom_text(self, entity):

        if self.map_zoom <= MapZooms.medium:
            return True
        else:
            return False

    def should_show_top_text(self, entity):
        return self.should_show_right_text(entity)

