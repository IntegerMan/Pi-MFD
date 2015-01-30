# coding=utf-8

"""
Map Contexts are used to provide contextual rendering and filtering information to the map as it is rendered
"""
from PiMFD.Applications.Navigation.MapFilters import StandardMapFilter, FoodMapFilter, GasMapFilter

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
    active_filter = None
    filters = None

    def __init__(self, app):
        super(MapContext, self).__init__()

        self.app = app
        self.filters = (StandardMapFilter(self), GasMapFilter(self), FoodMapFilter(self))
        self.active_filter = self.filters[0]

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
        return self.active_filter.should_show_lines(entity)

    def should_show_shapes(self, entity):
        return self.active_filter.should_show_shapes(entity)

    def should_show_icons(self, entity):
        return self.active_filter.should_show_icons(entity)

    def should_show_right_text(self, entity):
        return self.active_filter.should_show_right_text(entity)

    def should_show_left_text(self, entity):
        return self.active_filter.should_show_left_text(entity)

    def should_show_bottom_text(self, entity):
        return self.active_filter.should_show_bottom_text(entity)

    def should_show_top_text(self, entity):
        return self.active_filter.should_show_right_text(entity)

    def next_map_mode(self):
        current_index = self.filters.index(self.active_filter)
        if current_index < 0 or current_index >= len(self.filters) - 1:
            self.active_filter = self.filters[0]
        else:
            self.active_filter = self.filters[current_index + 1]

