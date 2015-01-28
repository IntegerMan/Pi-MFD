# coding=utf-8
"""
The navigation application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.MFDPage import SimpleMessagePage
from PiMFD.Applications.Navigation.MapPages import MapPage
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.TrafficLoading import MapTraffic

__author__ = 'Matt Eland'


class MapZooms(object):
    """
    An enum-style collection of supported zoom levels
    """
    large = 0.02
    medium = 0.0125
    local = 0.0075
    neighborhood = 0.0025

class NavigationApp(MFDApplication):
    """
    The scheduling application. Contains pages related to scheduling and coordinates web-service communication.
    :type controller: PiMFD.Controller.MFDController The controller.
    """
    map_page = None
    gas_page = None
    food_page = None
    traffic_page = None
    conditions_page = None
    initialized = False

    map = None
    traffic = None
    zooms = MapZooms()
    map_zoom = zooms.local

    # These values are used for determining quantity of overlap while moving in a direction
    x_page_multiplier = 0.8
    y_page_multiplier = 0.5

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.map = Maps()
        self.traffic = MapTraffic(controller.options)

        self.map.output_file = controller.options.map_output_file

        self.map_page = MapPage(controller, self)
        self.gas_page = SimpleMessagePage(controller, self, "GAS")
        self.food_page = SimpleMessagePage(controller, self, "FOOD")
        self.traffic_page = SimpleMessagePage(controller, self, "TRAF")
        self.conditions_page = SimpleMessagePage(controller, self, "COND")
        self.always_render_background = True

        self.pages = list([self.map_page, self.gas_page, self.food_page, self.traffic_page, self.conditions_page])

    def get_default_page(self):
        """
        Gets the default page within the application.
        :return: the default page within the application.
        """
        return self.map_page

    def get_button_text(self):
        """
        Gets text for the button representing this page.
        :return: the button text for the application button.
        """
        return 'NAV'

    def page_reselected(self, page):
        """
        Handles the page reselected event for this application.
        :param page: The page that was reselected.
        """
        self.get_map_data()
        super(NavigationApp, self).page_reselected(page)

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """
        if not self.initialized:
            # TODO: This should be in another thread so the UI can keep rendering
            self.get_map_data()

    def get_map_data(self, bounds=None):

        if bounds:
            self.map.fetch_area([bounds[0], bounds[1], bounds[2], bounds[3]])
        else:
            self.map.fetch_by_coordinate(self.controller.options.lat, self.controller.options.lng, self.map_zoom)
            bounds = self.map.bounds

        self.map.annotations = self.traffic.get_traffic(bounds)
        self.initialized = True

    def zoom_in(self):

        if self.map_zoom == self.zooms.large:
            self.map_zoom = self.zooms.medium
        elif self.map_zoom == self.zooms.medium:
            self.map_zoom = self.zooms.local
        elif self.map_zoom == self.zooms.local:
            self.map_zoom = self.zooms.neighborhood
        else:
            return

        self.get_map_data()

    def zoom_out(self):

        if self.map_zoom == self.zooms.neighborhood:
            self.map_zoom = self.zooms.local
        elif self.map_zoom == self.zooms.local:
            self.map_zoom = self.zooms.medium
        elif self.map_zoom == self.zooms.medium:
            self.map_zoom = self.zooms.large
        else:
            return

        self.get_map_data()

    def move_up(self):
        if self.map.has_data:
            bounds = self.map.bounds
            size = (bounds[3] - bounds[1]) * self.y_page_multiplier
            self.get_map_data([bounds[0], bounds[1] + size, bounds[2], bounds[3] + size])

    def move_right(self):
        if self.map.has_data:
            bounds = self.map.bounds
            size = (bounds[2] - bounds[0]) * self.x_page_multiplier
            self.get_map_data([bounds[0] + size, bounds[1], bounds[2] + size, bounds[3]])

    def move_left(self):
        if self.map.has_data:
            bounds = self.map.bounds
            size = (bounds[2] - bounds[0]) * self.x_page_multiplier
            self.get_map_data([bounds[0] - size, bounds[1], bounds[2] - size, bounds[3]])

    def move_down(self):
        if self.map.has_data:
            bounds = self.map.bounds
            size = (bounds[3] - bounds[1]) * self.y_page_multiplier
            self.get_map_data([bounds[0], bounds[1] - size, bounds[2], bounds[3] - size])
