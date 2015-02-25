# coding=utf-8
from datetime import datetime
import math

from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


__author__ = 'Matt Eland'

class MapRenderer(object):  # TODO: Maybe this should be a UIWidget?
    """
    A class used to render a Map object
    """

    def __init__(self, display, data_provider, size=(200, 200)):
        self.map = data_provider.map
        self.display = display
        self.center = display.get_content_center()
        self.size = size
        self.data_provider = data_provider
        self.map_context = data_provider.map_context
        self.osm_shapes = None
        self.last_translate = None
        self.weather = None

    def calculate_distance(self, pos_1, pos_2):
        x_squared = math.pow(pos_1[0] - pos_2[0], 2)
        y_squared = math.pow(pos_1[1] - pos_2[1], 2)
        return math.sqrt(x_squared + y_squared)

    def find_nearest_targetable_object(self, pos):

        best_distance = None
        target = None

        candidates = []

        if self.osm_shapes:
            candidates += self.osm_shapes

        if self.map.annotations:
            candidates += self.map.annotations

        if self.weather:
            candidates.append(self.weather)

        for shape in candidates:

            if not shape or not self.map_context.should_show_entity(shape):
                continue

            distance = self.calculate_distance(pos, (shape.x, shape.y))

            if best_distance is None or best_distance > distance:
                best_distance = distance
                target = shape

        return target

    def render(self):

        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        max_available = max(self.display.bounds.width, self.display.bounds.height)

        # Only recompute the expensive stuff if the resolution has changed or the data fetch time has changed
        if max_available != self.size[0] or \
                not self.last_translate or \
                not self.map.last_data_received or \
                self.map.last_data_received > self.last_translate:

            # Recompute our dimensions
            self.size = (max_available, max_available)
            self.center = self.display.get_content_center()

            # Translate the various curves, etc. into their appropraite screen positions
            self.osm_shapes = self.map.translate_shapes(self.size, self.center)

            self.last_translate = datetime.now()

        map_context = self.map_context

        # Draw Weather Data if Present
        weather_data = self.map.weather_data
        if weather_data:
            self.weather = self.build_symbol(weather_data.gps[0], weather_data.gps[1])
            self.weather.set_pos((self.display.bounds.right - 45, 50))
            self.weather.name = "{} Weather".format(weather_data.city)
            self.weather.tags = weather_data.get_tags()
            self.map_context.weather_data = weather_data

        # Update the cursor and figure out what we're targeting - if cursor is active
        if self.map_context.should_show_cursor():
            pos = self.map_context.maintain_cursor_position()
            context = self.find_nearest_targetable_object(pos)
            map_context.cursor_context = context

        # Render the open street map data
        if self.osm_shapes:
            for shape in self.osm_shapes:
                shape.render(self.display, map_context)

        # Render locations
        for loc in self.map_context.app.locations:
            sym = self.build_symbol(float(loc.lat), float(loc.lng))
            sym.name = loc.name
            pos = self.map.set_screen_position(sym, self.size, self.center)
            sym.x, sym.y = pos
            sym.tags = {'location': 'bookmark', 'iff': 'self'}
            sym.render(self.display, map_context)

        # Render custom annotations over everything - these should always be recomputed
        if self.map.annotations:
            for sym in self.map.annotations:
                pos = self.map.set_screen_position(sym, self.size, self.center)
                sym.x, sym.y = pos
                sym.render(self.display, map_context)

        if self.weather:
            self.weather.render(self.display, map_context)

        # Draw the cursor as needed
        if self.map_context.should_show_cursor():
            cur = self.build_symbol(0, 0)
            cur.set_pos(self.map_context.cursor_pos)
            cur.add_tag('actor', 'cursor')
            cur.add_tag('iff', 'self')
            cur.lat, cur.lng = self.map.translate_x_y_to_lat_lng(cur.x, cur.y,
                                                                 self.map.get_dimension_coefficients(self.size),
                                                                 self.center)
            cur.render(self.display, map_context)

    def build_symbol(self, lat, lng):
        sym = MapSymbol(lat, lng)
        sym.x, sym.y = self.map.gps_to_screen(lat, lng, self.size, self.center)
        return sym
