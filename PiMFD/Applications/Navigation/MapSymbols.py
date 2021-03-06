# coding=utf-8

"""
Code organized around rendering locations to the map
"""
from pygame.rect import Rect

from PiMFD.Applications.Navigation.MapEntities import MapEntity
from PiMFD.Applications.Navigation.MapIcons import ChairIcon, FoodIcon, WeatherIcon, EyeIcon, PillIcon
from PiMFD.UI.Rendering import render_text, render_circle, render_rectangle, render_text_centered, render_diamond, \
    render_triangle_up, draw_vertical_line, draw_horizontal_line


__author__ = 'Matt Eland'


class SymbolBackShape(object):
    """
    The backing of a symbol
    """

    none = 0
    square = 1
    circle = 2
    diamond = 3
    triangle = 4
    dot = 5
    square_top_triangle = 6
    bullseye = 7
    traffic_stop = 8
    double_circle = 9
    cursor = 10


class MapSymbol(MapEntity):
    """
    Renders a map symbol to the screen
    """

    def __init__(self, lat, lng):
        super(MapSymbol, self).__init__(lat, lng)

    def copy_values_from(self, location):

        self.tags = location.tags

        if hasattr(location, 'name'):
            self.name = location.name

        if hasattr(location, 'id'):
            self.id = location.id

    def get_font_text_and_color(self, display):
        """
        Returns the font to use to display, the text to render, and the color to use
        :param display: The DisplayManager
        :return: the font to use to display, the text to render, and the color to use
        """

        return display.fonts.small, self.name.upper(), display.color_scheme.highlight

    def render(self, display, map_context):
        """
        Renders the symbol to the screen.
        :param display: The display manager
        """

        # In general symbols will be composed of the following components
        #
        # Main Shape
        # Square - Amenities
        # Circle - Government / Services / Public
        #   Diamond - Shops
        #   Square w. Diamond Top - Residential
        #
        # Text
        # Right Text - Specialization
        #   Bottom Text - Name
        #   Inner Text - Symbol Code
        #   Left Text - Augmented Data for current map mode

        shape_width = 1
        shape_size = 20

        # Set shape. Python 2.7 doesn't have enum support so I'm using a placeholder class for that.
        shape = SymbolBackShape()
        style = shape.circle

        shape_shop = shape.diamond
        shape_service = shape.square
        shape_public = shape.circle

        icons = list()

        font = display.fonts.small

        pos = (int(self.x), int(self.y))

        # Grab name, preferring short_name if present, otherwise abbreviating
        display_name = self.get_display_name()

        app_data = None
        extra_data = None
        inner_text = None

        if map_context.cursor_context is self:
            app_data = 'CUR'

        if map_context.target is self:
            app_data = 'TGT'

        shop = self.get_tag_value('shop')
        amenity = self.get_tag_value('amenity')

        hide_shape_if_has_building = True

        # Modify our display parameters based on what our context is

        if self.has_tag('highway'):

            # Don't display names for roads at the moment
            display_name = None

            highway = self.get_tag_value('highway')
            if highway == 'traffic_signals':
                style = shape.traffic_stop
                hide_shape_if_has_building = False

            elif highway == 'street_lamp':
                style = shape.circle
                shape_width = 0
                shape_size = 1
                hide_shape_if_has_building = False

            elif highway == 'motorway_junction':
                style = shape.diamond
                hide_shape_if_has_building = False

            elif highway == 'crossing':
                style = shape.diamond
                hide_shape_if_has_building = False
                shape_width = 0
                shape_size = 6

        elif amenity:

            style = shape_shop

            if amenity == 'pharmacy':
                style = shape.none
                icons.append(PillIcon())

            elif amenity == 'fuel':
                inner_text = 'GAS'

            elif amenity == 'school':
                style = shape_public  # Though this could be service if private school
                inner_text = 'EDU'

            elif amenity == 'veterinary':
                style = shape_service
                inner_text = 'VET'

            elif amenity == 'place_of_worship':

                # Plug in the denomination or religion
                extra_data = self.get_tag_value('denomination')
                if extra_data is None:
                    extra_data = self.get_tag_value('religion')

                style = shape_service
                inner_text = 'REL'

            elif amenity in ('restaurant', 'pub'):

                # Plug in the cuisine
                extra_data = self.get_tag_value('cuisine')

                style = shape_service  # Service since we eat in

                icons.append(FoodIcon())  # TODO: Render by cuisine

            elif amenity in ('fast_food', 'food_court'):

                # Plug in the cuisine
                extra_data = self.get_tag_value('cuisine')

                icons.append(FoodIcon())  # TODO: Render by cuisine

            elif amenity == 'cafe':
                inner_text = 'caf'

            elif amenity == 'bbq':
                inner_text = 'bbq'

            elif amenity in ('biergarten', 'bar'):
                inner_text = 'bar'

            elif amenity == 'drinking_water':
                inner_text = 'H2O'

            elif amenity == 'ice_cream':
                inner_text = 'ice'  # Icon should come here - this one isn't intuitive on abbrv.

            elif amenity in ('college', 'university'):
                inner_text = 'EDU'

            elif amenity == 'kindergarten':
                inner_text = 'pre'

            elif amenity == 'library':
                inner_text = 'lib'

            elif amenity == 'school':
                inner_text = 'sch'

            elif amenity == 'public_bookcase':
                inner_text = 'cas'

            elif amenity in ('bicycle_parking', 'bicycle_repair_station', 'bicycle_rental'):
                inner_text = 'bik'

            elif amenity == 'boat_sharing':
                inner_text = 'boa'

            elif amenity == 'bus_station':
                inner_text = 'bus'

        elif shop:

            style = shape_shop

            if shop == 'car_repair':
                style = shape_service
                inner_text = 'CAR'

            elif shop == 'furniture':
                icons.append(ChairIcon())

            elif shop == 'sports':
                inner_text = 'ATH'

            elif shop == 'free_flying':
                inner_text = 'FLY'

            elif shop == 'shoes':
                inner_text = 'WLK'

            elif shop == 'supermarket':
                icons.append(FoodIcon())

            elif shop == 'optician':
                style = shape.none
                icons.append(EyeIcon())

            elif shop == 'beauty':
                style = shape_service
                inner_text = 'SPA'

        elif self.has_tag('tourism'):

            # No added styling needed so far
            pass

        elif self.has_tag('building'):

            # No added styling needed so far
            pass

        elif self.has_tag('leisure'):

            # No added styling needed so far
            pass

        elif self.has_tag('power'):

            power = self.get_tag_value('power')

            if power == 'tower':
                style = shape.triangle
                shape_size = 6

            elif power == 'pole':
                style = shape.circle
                shape_size = 3

        elif self.has_tag('barrier'):
            shape_size = 3

        elif self.has_tag_value('footway', 'crossing'):
            style = shape.diamond
            shape_width = 0
            shape_size = 6

        elif self.has_tag('surveillance'):
            style = shape.none
            icons.append(EyeIcon())

        elif self.has_tag('weather'):
            style = shape.none
            icons.append(WeatherIcon(self.get_tag_value('weather')))

            if self.has_tag('wind:speed') and self.has_tag('wind:direction_cardinal'):
                extra_data = self.get_tag_value('wind:speed') + ' ' + self.get_tag_value('wind:direction_cardinal')

            display_name = self.get_tag_value('temperature') + "'F"

        elif self.has_tag('man_made'):

            man_made = self.get_tag_value('man_made')

            if man_made == 'tower':
                style = shape.triangle

            elif man_made == 'surveillance':
                style = shape.none
                icons.append(EyeIcon())

        elif self.has_tag('actor'):

            actor = self.get_tag_value('actor')

            if actor == 'cursor':
                style = shape.cursor
                shape_width = 3
                extra_data = self.get_tag_value('owner')
                display_name = '{}, {}'.format(self.lat, self.lng)
                if map_context.cursor_context:
                    app_data = map_context.cursor_context.name
            else:
                style = shape.double_circle

        elif self.has_tag('incident'):
            style = shape.diamond

            end = self.get_tag_value('end_date')
            extra_data = end

            shape_width = 2
            
        elif self.has_tag('location'):
            style = shape.bullseye
            shape_width = 5

        half_size = shape_size / 2

        right_text = extra_data
        left_text = app_data
        bottom_text = display_name

        color = self.get_color(display.color_scheme, map_context)

        # Render the shape of the item
        if (not hide_shape_if_has_building or not self.has_lines) and map_context.should_show_shapes(self):

            if style == shape.circle:
                render_circle(display, color, pos, half_size + 2, shape_width)

            elif style == shape.square:
                render_rectangle(display, color, Rect(self.x - half_size, self.y - half_size, shape_size, shape_size),
                                 shape_width)

            elif style == shape.diamond:
                render_diamond(display, color, pos, half_size + 2, shape_width)

            elif style == shape.triangle:
                render_triangle_up(display, color, pos, half_size + 2, shape_width)

            elif style == shape.bullseye:
                render_circle(display, color, pos, half_size * 2, 1)
                render_circle(display, color, pos, half_size, 1)
                draw_horizontal_line(display, color, pos[0] - (half_size * 3), pos[0] + (half_size * 3), pos[1])
                draw_vertical_line(display, color, pos[0], pos[1] - (half_size * 3), pos[1] + (half_size * 3))

            elif style == shape.double_circle:
                render_circle(display, color, pos, half_size + 2, shape_width)
                render_circle(display, color, pos, half_size, shape_width)

            elif style == shape.traffic_stop:
                render_circle(display, display.color_scheme.red, pos, 4, 0)
                render_circle(display, display.color_scheme.yellow, pos, 3, 0)
                render_circle(display, display.color_scheme.green, pos, 1, 0)

            elif style == shape.cursor:
                draw_vertical_line(display, display.color_scheme.highlight, pos[0], pos[1] - shape_width,
                                   pos[1] + shape_width)
                draw_horizontal_line(display, display.color_scheme.highlight, pos[0] - shape_width,
                                     pos[0] + shape_width, pos[1])

        # Render adornment icons
        if map_context.should_show_icons(self):
            for icon in icons:
                icon.render(display, color, pos, half_size)

        # Render text labels
        if inner_text and map_context.should_show_shapes(self):
            render_text_centered(display,
                                 font,
                                 inner_text.upper(),
                                 self.x,
                                 self.y - (font.measure(inner_text)[1] / 2.0),
                                 color)

        if right_text and map_context.should_show_right_text(self):
            render_text(display,
                        font,
                        right_text.upper(),
                        self.x + half_size + 3,
                        self.y - (font.measure(right_text)[1] / 2.0),
                        color)

        if left_text and map_context.should_show_left_text(self):
            render_text(display,
                        font,
                        left_text.upper(),
                        self.x - font.measure(left_text)[0] - 12,
                        self.y - (font.measure(left_text)[1] / 2.0),
                        display.color_scheme.highlight)

        if bottom_text and map_context.should_show_bottom_text(self):
            render_text_centered(display,
                                 font,
                                 bottom_text.upper(),
                                 self.x,
                                 self.y + half_size + 3,
                                 color)

