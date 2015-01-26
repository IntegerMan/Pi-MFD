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

        building = self.get_tag_value('building')
        shop = self.get_tag_value('shop')
        amenity = self.get_tag_value('amenity')

        if self.has_tag('railway'):
            color = cs.gray

        elif self.has_tag('highway'):

            value = self.get_tag_value('highway')

            color = default_color

            if value == 'motoway':
                width = 5
            elif value == 'trunk':
                width = 4
            elif value == 'primary':
                width = 3
            elif value == 'secondary':
                width = 2
            elif value == 'tertiary':
                width = 1
            elif value == 'unclassified':
                color = cs.map_unknown
                width = 1
            elif value == 'residential':
                color = cs.map_residential
                width = 1
            elif value == 'path':
                width = 1
                color = cs.map_pedestrian
            elif value == 'service':
                width = 1
                color = cs.map_private
            else:
                color = cs.map_unknown  # For Debugging

            # If it's got a bridge, we'll handle it a bit differently
            if self.has_tag_value('bridge', 'yes'):
                color = cs.white

        elif self.has_tag_value('boundary', 'administrative'):
            color = cs.map_government  # Purple

        elif self.has_tag_value('natural', 'water') or self.has_tag('water'):
            color = cs.blueish
            width = 0

        elif self.has_tag('leisure'):

            if self.has_tag_value('leisure', 'park'):
                color = cs.greenish
                width = 1  # I can't close this because that can hide things inside like playgrounds

            elif self.has_tag_value('leisure', 'pitch'):
                # TODO: Take sport into account?
                color = cs.greenish

            elif self.has_tag_value('leisure', 'playground'):
                color = cs.map_pedestrian

        elif self.has_tag_value('landuse', 'cemetery'):
            color = cs.gray

        elif building:

            color = cs.map_unknown

            if shop:
                color = self.get_shop_color(cs, shop)

            elif amenity:
                color = cs.map_commercial

            elif building in ('residential', 'terrace', 'apartment'):
                color = cs.map_residential
                width = 0  # We're not going to render anything inside of these guy so just fill them

        elif amenity == 'parking':
            color = cs.map_automotive

        else:

            color = cs.map_unknown

        # TODO: Use the rendering helpers
        if width <= 0:
            pygame.draw.polygon(display.surface, color, self.points, width)
        else:
            pygame.draw.lines(display.surface, color, False, self.points, width)


6