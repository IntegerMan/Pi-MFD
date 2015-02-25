# coding=utf-8

"""
Map Contexts are used to provide contextual rendering and filtering information to the map as it is rendered
"""
from PiMFD.Applications.Navigation.MapFilters import StandardMapFilter, FoodMapFilter, GasMapFilter, \
    InfrastructureMapFilter, WifiMapFilter, WikipediaMapFilter
from PiMFD.Applications.Navigation.Tags.AmenityTagHandling import AmenityTagHandler
from PiMFD.Applications.Navigation.Tags.BarrierTagHandling import BarrierTagHandler
from PiMFD.Applications.Navigation.Tags.BuildingTagHandling import BuildingTagHandler
from PiMFD.Applications.Navigation.Tags.HighwayTagHandling import HighwayTagHandler
from PiMFD.Applications.Navigation.Tags.LeisureTagHandling import LeisureTagHandler
from PiMFD.Applications.Navigation.Tags.NaturalTagHandling import NaturalTagHandler
from PiMFD.Applications.Navigation.Tags.ShopTagHandling import ShopTagHandler
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandlerManager
from PiMFD.Applications.Navigation.Tags.TourismTagHandling import TourismTagHandler

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
    cursor_speed = 3
    allow_move = True
    target = None
    cursor_context = None

    tag_handlers = None

    def __init__(self, app, map, data_provider):
        super(MapContext, self).__init__()

        self.app = app
        self.map = map
        self.data_provider = data_provider
        self.filters = (StandardMapFilter(self),
                        GasMapFilter(self),
                        FoodMapFilter(self),
                        InfrastructureMapFilter(self),
                        WifiMapFilter(self),
                        WikipediaMapFilter(self))
        self.active_filter = self.filters[0]
        self.cursor_pos = app.display.get_content_center()

        # If we're on a small display, start out at a small zoom
        size = app.display.get_content_size()
        if min(size[0], size[1]) <= 480:
            self.map_zoom = MapZooms.neighborhood

        self.tag_handlers = TagHandlerManager(self)
        self.tag_handlers.add_handler('highway', HighwayTagHandler(self))
        self.tag_handlers.add_handler('building', BuildingTagHandler(self))
        self.tag_handlers.add_handler('barrier', BarrierTagHandler(self))
        self.tag_handlers.add_handler('leisure', LeisureTagHandler(self))
        self.tag_handlers.add_handler('amenity', AmenityTagHandler(self))
        self.tag_handlers.add_handler('natural', NaturalTagHandler(self))
        self.tag_handlers.add_handler('tourism', TourismTagHandler(self))
        self.tag_handlers.add_handler('shop', ShopTagHandler(self))

    def zoom_in(self):
        if self.map_zoom == self.zooms.large:
            self.map_zoom = self.zooms.medium
        elif self.map_zoom == self.zooms.medium:
            self.map_zoom = self.zooms.local
        elif self.map_zoom == self.zooms.local:
            self.map_zoom = self.zooms.neighborhood
        else:
            return False

        self.data_provider.get_map_data_on_current_cursor_pos()

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

        self.data_provider.get_map_data()

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

    def should_show_entity(self, entity):
        return self.active_filter.should_show_entity(entity)

    def next_map_mode(self):
        current_index = self.filters.index(self.active_filter)
        if current_index < 0 or current_index >= len(self.filters) - 1:
            self.active_filter = self.filters[0]
        else:
            self.active_filter = self.filters[current_index + 1]

    page_mode = "PAGE"
    page_modes = ["PAGE", "PAN", "CUR"]

    def get_page_mode_text(self):
        return self.page_mode

    def next_page_mode(self):
        current_index = self.page_modes.index(self.page_mode)
        if current_index < 0 or current_index >= len(self.page_modes) - 1:
            self.page_mode = self.page_modes[0]
        else:
            self.page_mode = self.page_modes[current_index + 1]

        if self.page_mode == "PAN":
            self.move_multiplier = 0.35
        else:
            self.move_multiplier = 1.0

        self.allow_move = self.page_mode in ('PAGE', 'PAN')

    # These values are used for determining quantity of overlap while moving in a direction
    x_page_multiplier = 0.8
    y_page_multiplier = 0.5
    move_multiplier = 1

    def move_up(self):
        if self.map.has_data and self.allow_move:
            bounds = self.map.bounds
            size = (bounds[3] - bounds[1]) * self.y_page_multiplier * self.move_multiplier
            self.data_provider.get_map_data([bounds[0], bounds[1] + size, bounds[2], bounds[3] + size])
        elif self.should_show_cursor():
            self.cursor_pos = self.cursor_pos[0], self.cursor_pos[1] - self.cursor_speed

    def move_right(self):
        if self.map.has_data and self.allow_move:
            bounds = self.map.bounds
            size = (bounds[2] - bounds[0]) * self.x_page_multiplier * self.move_multiplier
            self.data_provider.get_map_data([bounds[0] + size, bounds[1], bounds[2] + size, bounds[3]])
        elif self.should_show_cursor():
            self.cursor_pos = self.cursor_pos[0] + self.cursor_speed, self.cursor_pos[1]

    def move_left(self):
        if self.map.has_data and self.allow_move:
            bounds = self.map.bounds
            size = (bounds[2] - bounds[0]) * self.x_page_multiplier * self.move_multiplier
            self.data_provider.get_map_data([bounds[0] - size, bounds[1], bounds[2] - size, bounds[3]])
        elif self.should_show_cursor():
            self.cursor_pos = self.cursor_pos[0] - self.cursor_speed, self.cursor_pos[1]

    def move_down(self):
        if self.map.has_data and self.allow_move:
            bounds = self.map.bounds
            size = (bounds[3] - bounds[1]) * self.y_page_multiplier * self.move_multiplier
            self.data_provider.get_map_data([bounds[0], bounds[1] - size, bounds[2], bounds[3] - size])
        elif self.should_show_cursor():
            self.cursor_pos = self.cursor_pos[0], self.cursor_pos[1] + self.cursor_speed

    def should_show_cursor(self):
        return self.page_mode == "CUR"

    def maintain_cursor_position(self):
        x, y = self.cursor_pos
        x = max(0, min(x, self.app.display.bounds.right - 1))
        y = max(0, min(y, self.app.display.bounds.bottom - 1))
        self.cursor_pos = x, y
        return self.cursor_pos