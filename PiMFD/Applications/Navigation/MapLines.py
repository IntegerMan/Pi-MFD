# coding=utf-8

"""
Contains code relevant to rendering map lines to the map
"""
import pygame

from PiMFD.Applications.Navigation.MapEntities import MapPath
from PiMFD.Applications.Navigation.MapSymbols import MapSymbol
from PiMFD.UI.Rendering import render_text_centered


__author__ = 'Matt Eland'


class MapLine(MapSymbol, MapPath):
    """
    Renders map paths to the screen with added contextual styling support
    """

    def __init__(self, path):
        super(MapSymbol, self).__init__(path.lat, path.lng)
        super(MapPath, self).__init__(path.lat, path.lng)

        self.id = path.id
        self.tags = path.tags
        self.name = path.name

        # Points are manually copied during the transpose process

    def render(self, display):

        show_name = False

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
                show_name = True
                color = cs.map_unknown  # For Debugging

            # If it's got a bridge, we'll handle it a bit differently
            if self.has_tag_value('bridge', 'yes'):
                color = cs.white

        elif self.has_tag_value('boundary', 'administrative'):
            show_name = True
            color = cs.map_government

        elif self.has_tag_value('natural', 'water') or self.has_tag('water'):
            show_name = True
            color = cs.blueish
            width = 0

        elif self.has_tag('leisure'):

            show_name = True

            if self.has_tag_value('leisure', 'park'):
                color = cs.greenish

            elif self.has_tag_value('leisure', 'pitch'):
                # TODO: Take sport into account?
                color = cs.map_pedestrian

            elif self.has_tag_value('leisure', 'playground'):
                color = cs.map_pedestrian

        elif self.has_tag_value('landuse', 'cemetery'):

            show_name = True

            color = cs.gray

        elif building:

            show_name = True

            color = cs.map_unknown

            if shop:
                color = self.get_shop_color(cs, shop)

            elif amenity:
                color = self.get_amenity_color(cs, amenity)

            elif building in ('residential', 'terrace', 'apartment'):
                color = cs.map_residential
                width = 0  # We're not going to render anything inside of these guy so just fill them

            elif building in ('kindergarten', 'school'):
                color = cs.map_public

        elif amenity == 'parking':
            color = cs.map_automotive

        else:

            show_name = True
            color = cs.map_unknown

        # TODO: Use the rendering helpers
        if width <= 0:
            pygame.draw.polygon(display.surface, color, self.points, width)
        else:
            pygame.draw.lines(display.surface, color, False, self.points, width)

        if show_name:

            display_name = self.get_display_name()
            if display_name:
                render_text_centered(display,
                                     display.fonts.small,
                                     display_name,
                                     self.x,
                                     self.y + 13,  # May want to move this off below eventually
                                     color)


6