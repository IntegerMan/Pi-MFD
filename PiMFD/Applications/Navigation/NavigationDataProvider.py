# coding=utf-8

"""
This file contains a data provider for navigation-related items.
"""
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class NavigationDataProvider(DataProvider):
    """
    A DataProvider for the NavigationApplication.
    :param name: The name of the data provider
    """

    def __init__(self, application, name="Navigation Data Provider"):
        super(NavigationDataProvider, self).__init__(name)

        self.application = application
        self.options = application.controller.options

        self.map = Maps(self)
        self.map.output_file = self.options.map_output_file

        self.map_context = MapContext(self.application, self.map, self)

        self.initialized = False

    def update(self, now):
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