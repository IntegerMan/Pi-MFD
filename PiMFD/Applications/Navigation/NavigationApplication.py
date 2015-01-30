# coding=utf-8
"""
The navigation application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapPages import MapPage
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic
from PiMFD.UI.Button import MFDButton

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
    btn_map = None
    btn_page = None

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.map = Maps()
        self.map_context = MapContext(self, self.map)
        self.traffic = MapTraffic(controller.options)

        self.map.output_file = controller.options.map_output_file

        self.map_page = MapPage(controller, self)
        self.always_render_background = True

        self.pages = list([self.map_page])
        self.btn_map = MFDButton(None, selected=True)
        self.btn_page = MFDButton(self.map_context.get_page_mode_text())

    def get_buttons(self):

        self.btn_map.text = self.map_page.get_button_text()
        self.btn_page.text = self.map_context.get_page_mode_text()

        return [self.btn_map, self.btn_page]

    def select_page_by_index(self, index):

        if (index == 0):
            self.map_context.next_map_mode()
        elif (index == 1):
            self.map_context.next_page_mode()

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
        super(NavigationApp, self).page_reselected(page)

    def handle_reselected(self):
        self.get_map_data()
        super(NavigationApp, self).handle_reselected()

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

    def next_map_mode(self):
        self.map_context.next_map_mode()
