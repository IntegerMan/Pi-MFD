# coding=utf-8

"""
Contains various filtering functions designed to filter down map displays or emphasize different aspects for different
map modes.
"""
import PiMFD.Applications.Navigation.MapContexts

__author__ = 'Matt Eland'


class MapFilter(object):
    def __init__(self, context):
        super(MapFilter, self).__init__()
        self.context = context

    def should_show_entity(self, entity):
        return True

    def should_show_lines(self, entity):
        return True

    def should_show_shapes(self, entity):
        return True

    def should_show_icons(self, entity):
        return True

    def should_show_right_text(self, entity):
        return True

    def should_show_left_text(self, entity):
        return True

    def should_show_bottom_text(self, entity):
        return True

    def should_show_top_text(self, entity):
        return True


class StandardMapFilter(MapFilter):
    def get_button_text(self):
        return "MAP"

    def should_show_lines(self, entity):
        return self.should_show_entity(entity)

    def should_show_icons(self, entity):
        return self.should_show_entity(entity)

    def should_show_shapes(self, entity):
        return self.should_show_entity(entity)

    def should_show_right_text(self, entity):

        if self.should_show_entity(
                entity) and self.context.map_zoom <= PiMFD.Applications.Navigation.MapContexts.MapZooms.local:
            return True
        else:
            return False

    def should_show_left_text(self, entity):
        return self.should_show_right_text(entity)

    def should_show_bottom_text(self, entity):

        if self.should_show_entity(
                entity) and self.context.map_zoom <= PiMFD.Applications.Navigation.MapContexts.MapZooms.medium:
            return True
        else:
            return False

    def should_show_top_text(self, entity):
        return self.should_show_right_text(entity)


class FoodMapFilter(StandardMapFilter):
    def get_button_text(self):
        return "FOOD"

    def should_show_right_text(self, entity):
        return self.should_show_entity(entity)

    def should_show_bottom_text(self, entity):
        return self.should_show_entity(entity)

    def should_show_entity(self, entity):
        return entity.has_tag("highway") or \
               entity.has_tag("fast_food") or \
               entity.has_tag("cuisine") or \
               entity.get_tag_value("amenity") in ('cafe', 'fast_food', 'restaurant') or \
               entity.has_tag_value('actor', 'self')


class GasMapFilter(StandardMapFilter):
    def get_button_text(self):
        return "NAV"

    def should_show_right_text(self, entity):
        return self.should_show_entity(entity)

    def should_show_bottom_text(self, entity):
        return self.should_show_entity(entity)

    def should_show_entity(self, entity):
        return entity.has_tag("highway") or \
               entity.has_tag("incident") or \
               entity.has_tag("railway") or \
               entity.has_tag('traffic_signals') or \
               entity.get_tag_value("amenity") in ('parking', 'fuel') or \
               entity.has_tag_value('actor', 'self')