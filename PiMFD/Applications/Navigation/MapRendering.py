# coding=utf-8
from PiMFD.Applications.Navigation.MapEntities import MapEntity
from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


__author__ = 'Matt Eland'


class MapRenderer(object):  # TODO: Maybe this should be a UIWidget?
    """
    A class used to render a Map object
    """

    def __init__(self, map, display, size=(200, 200)):
        self.map = map
        self.display = display
        self.size = size

    def render(self):

        # Smart scale the size to accomodate for the greatest dimension. This lets us support many aspect ratios.
        available_x = self.display.res_x
        available_y = self.display.res_y
        max_available = max(available_y, available_x)

        self.size = (max_available, max_available)
        self.center = ((self.display.res_x / 2.0), (self.display.res_y / 2.0))

        # Translate the various curves, etc. into their appropraite screen positions
        ways = self.map.transpose_ways(self.size, self.center)
        symbols = self.map.transpose_locations(self.size, self.center)

        # Render the Roads
        for way in ways:
            way.render(self.display)

        # Add ourself to the map
        sym = self.build_symbol(self.display.options.lat, self.display.options.lng)
        sym.name = 'ME'
        sym.add_tag('actor', 'self')

        if self.map.annotations:
            for annotation in self.map.annotations:
                pos = self.map.set_screen_position(annotation, self.size, self.center)
                sym = MapSymbol(pos[0], pos[1], annotation)
                sym.name = annotation.description
                sym.add_tag('incident', annotation.incident_type)
                sym.render(self.display)

        sym.render(self.display)

        # Render the other awesome things
        for symbol in symbols:
            symbol.render(self.display)

    def build_symbol(self, lat, lng):
        x, y = self.map.gps_to_screen(lat, lng, self.size, self.center)
        me = MapEntity(lat, lng)
        return MapSymbol(x, y, me)
