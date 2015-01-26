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
        color = cs.map_unknown

        width = 1

        building = self.get_tag_value('building')
        shop = self.get_tag_value('shop')
        amenity = self.get_tag_value('amenity')

        if self.has_tag('railway'):
            color = cs.gray

        elif self.has_tag('highway'):

            value = self.get_tag_value('highway')

            color = default_color

            if value in ('motoway', 'motorway'):
                width = 5
            elif value in ('trunk', 'motorway_link'):
                width = 4
            elif value == 'primary':
                width = 3
            elif value == 'secondary':
                width = 2
            elif value == 'tertiary':
                width = 1
            elif value == ('unclassified', 'road'):
                color = cs.map_unknown
                width = 1
            elif value in ('residential', 'living_street'):
                color = cs.map_residential
                width = 1
            elif value in ('path', 'footway'):
                width = 1
                color = cs.map_pedestrian
            elif value == 'cycleway':
                width = 1
                color = cs.map_automotive
            elif value == 'service':
                width = 1
                color = cs.map_service
            elif value == 'proposed':
                width = 1
                color = cs.map_emergency
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
            color = cs.map_water
            width = 0

        elif self.has_tag_value('natural', 'wood') or self.has_tag('wood'):
            show_name = True
            color = cs.map_vegitation
            width = 0

        elif self.has_tag('waterway'):
            color = cs.map_water
            width = 3

        elif self.has_tag('leisure'):

            show_name = True

            leisure = self.get_tag_value('leisure')

            if leisure in ('pitch', 'park', 'golf_course'):
                color = cs.map_recreation

            elif leisure in ('playground', 'track'):
                color = cs.map_pedestrian

            elif leisure == 'swimming_pool':
                color = cs.map_water

        elif self.has_tag('landuse'):

            show_name = True
            landuse = self.get_tag_value('landuse')

            if landuse in ('cemetery', 'cemetery'):
                color = cs.gray

            elif landuse == 'grass':
                color = cs.map_recreation

        elif building:

            show_name = True

            if shop:
                color = self.get_shop_color(cs, shop)

            elif amenity:
                color = self.get_amenity_color(cs, amenity)

            else:
                color = self.get_building_color(cs, building)

            if building in ('residential', 'terrace', 'apartment'):
                width = 0  # We're not going to render anything inside of these guy so just fill them

        elif amenity:

            show_name = True

            color = self.get_amenity_color(cs, amenity)

        elif self.has_tag('man_made'):

            show_name = True

            man_made = self.get_tag_value('man_made')

            if man_made == 'water_tower':
                color = cs.map_infrastructure

        elif self.has_tag('power'):
            color = cs.map_infrastructure

        elif self.has_tag('barrier'):
            color = cs.map_private

        elif self.has_tag('traffic_sign'):
            color = cs.map_government

        else:

            show_name = True

        # TODO: Use the rendering helpers
        if len(self.points) > 0:
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