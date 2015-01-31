# coding=utf-8
from datetime import datetime
from time import strftime

from PiMFD.Applications.Navigation.MapEntities import MapEntity
from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


__author__ = 'Matt Eland'

class MapRenderer(object):  # TODO: Maybe this should be a UIWidget?
    """
    A class used to render a Map object
    """

    def __init__(self, map, display, map_context, size=(200, 200)):
        self.map = map
        self.display = display
        self.center = ((display.res_x / 2.0), (display.res_y / 2.0))
        self.size = size
        self.map_context = map_context
        self.osm_shapes = None
        self.last_translate = None

    def render(self):

        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        max_available = max(self.display.res_x, self.display.res_y)

        # Only recompute the expensive stuff if the resolution has changed or the data fetch time has changed
        if max_available != self.size[0] or \
                not self.last_translate or \
                        self.map.last_data_received > self.last_translate:

            # Recompute our dimensions
            self.size = (max_available, max_available)
            self.center = ((self.display.res_x / 2.0), (self.display.res_y / 2.0))

            # Translate the various curves, etc. into their appropraite screen positions
            self.osm_shapes = self.map.transpose(self.size, self.center)

            self.last_translate = datetime.now()

        map_context = self.map_context

        # Render the open street map data
        if self.osm_shapes:
            for shape in self.osm_shapes:
                shape.render(self.display, map_context)

        # Render custom annotations over everything - these should always be recomputed
        if self.map.annotations:
            for annotation in self.map.annotations:
                pos = self.map.set_screen_position(annotation, self.size, self.center)
                sym = MapSymbol(pos[0], pos[1], annotation)
                sym.add_tag('incident', annotation.incident_type)
                if annotation.end:
                    sym.add_tag('end_date', strftime('%m/%d/%Y', annotation.end))
                if annotation.start:
                    sym.add_tag('start_date', strftime('%m/%d/%Y', annotation.start))
                sym.add_tag('note', annotation.description)
                sym.add_tag('severity', annotation.severity)
                sym.render(self.display, map_context)

        # Add ourself to the map - TODO: Add this to the annotation layer
        sym = self.build_symbol(self.display.options.lat, self.display.options.lng)
        sym.name = 'ME'
        sym.add_tag('actor', 'self')
        sym.render(self.display, map_context)

        # Draw the cursor as needed
        if self.map_context.should_show_cursor():
            self.map_context.render_cursor(self.display)

    def build_symbol(self, lat, lng):
        x, y = self.map.gps_to_screen(lat, lng, self.size, self.center)
        me = MapEntity(lat, lng)
        return MapSymbol(x, y, me)
