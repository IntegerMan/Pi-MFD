# coding=utf-8
"""
The navigation application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.MFDPage import SimpleMessagePage
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapPages import MapPage
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic

__author__ = 'Matt Eland'


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
    map_context = None
    traffic = None

    # These values are used for determining quantity of overlap while moving in a direction
    x_page_multiplier = 0.8
    y_page_multiplier = 0.5

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.map = Maps()
        self.map_context = MapContext(self)
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

            if self.map.bounds:
                lat = ((self.map.bounds[3] - self.map.bounds[1]) / 2.0) + self.map.bounds[1]
                lng = ((self.map.bounds[2] - self.map.bounds[0]) / 2.0) + self.map.bounds[0]
            else:
                lat = self.controller.options.lat
                lng = self.controller.options.lng

            self.map.fetch_by_coordinate(lat, lng, self.map_context.map_zoom)
            bounds = self.map.bounds

        self.map.annotations = self.traffic.get_traffic(bounds)
        self.initialized = True

    def zoom_in(self):

        if self.map_context.zoom_in():
            self.get_map_data()

    def zoom_out(self):

        if self.map_context.zoom_out():
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
