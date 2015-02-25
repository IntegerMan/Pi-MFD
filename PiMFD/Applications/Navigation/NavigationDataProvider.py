# coding=utf-8

"""
This file contains a data provider for navigation-related items.
"""
import pickle
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class NavigationDataProvider(DataProvider):
    """
    A DataProvider for the NavigationApplication.
    :param name: The name of the data provider
    """

    my_locations_file = 'mylocations.pickle'

    def __init__(self, application, name="Navigation Data Provider"):
        super(NavigationDataProvider, self).__init__(name)

        self.application = application
        self.options = application.controller.options
        self.display = application.display
        
        self.traffic = MapTraffic(self.options)
        
        self.locations = None
        
        self.map = Maps(self)
        self.map.output_file = self.options.map_output_file

        self.map_context = MapContext(self.application, self.map, self)

        self.initialized = False

    def update(self, now):

        # Load locations if needed
        if not self.locations:
            self.load_locations()

        super(NavigationDataProvider, self).update(now)

    def get_dashboard_widgets(self, display, page):
        super(NavigationDataProvider, self).get_dashboard_widgets(display, page)

    def get_map_data(self, bounds=None, lat=None, lng=None):

        if bounds:
            self.map.fetch_area([bounds[0], bounds[1], bounds[2], bounds[3]])
        else:

            if not lat or not lng:
                if self.map.bounds:
                    lat = ((self.map.bounds[3] - self.map.bounds[1]) / 2.0) + self.map.bounds[1]
                    lng = ((self.map.bounds[2] - self.map.bounds[0]) / 2.0) + self.map.bounds[0]
                else:
                    lat = self.options.lat
                    lng = self.options.lng

            self.map.fetch_by_coordinate(lat, lng, self.map_context.map_zoom)

        self.initialized = True

    def next_map_mode(self):
        self.map_context.next_map_mode()

    def get_map_data_on_current_cursor_pos(self):

        # Build precursors that are needed for the map
        dim_coef = self.map.get_dimension_coefficients(
            (self.display.bounds.width, self.display.bounds.height))
        offset = self.display.get_content_center()

        # Figure out the Lat / Lng
        pos = self.map_context.cursor_pos
        lat, lng = self.map.translate_x_y_to_lat_lng(pos[0], pos[1], dim_coef=dim_coef, offset=offset)

        # Get the map data
        self.get_map_data(lat=lat, lng=lng)

        # Recenter the Cursor
        self.map_context.cursor_pos = self.display.get_content_center()

    def get_traffic(self, bounds):
        self.traffic.get_traffic(bounds, self.map)

    def add_location(self, location):
        self.locations.append(location)
        self.save_locations()

    def delete_location(self, location):
        self.locations.remove(location)
        self.save_locations()

    def save_locations(self):
        try:
            f = open(self.my_locations_file, "w")
            pickle.dump(self.locations, f)
            f.close()
        except:
            error_message = "Unhandled error saving my locations to file {0}\n".format(str(traceback.format_exc()))
            print(error_message)

    def load_locations(self):

        try:
            f = open(self.my_locations_file, "r")
            locations = pickle.load(f)
            f.close()

            if locations and len(locations) > 0:
                self.locations = locations

        except:
            error_message = "Unhandled error saving my locations to file {0}\n".format(str(traceback.format_exc()))
            print(error_message)

        # set some default values
        if not self.locations or len(self.locations) <= 0:
            default_location = MapLocation('Default Location', self.controller.options.lat, self.controller.options.lng)
            self.locations = [default_location]
