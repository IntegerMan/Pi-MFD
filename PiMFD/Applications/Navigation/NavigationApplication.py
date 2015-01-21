# coding=utf-8
"""
The navigation application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.MFDPage import SimpleMessagePage
from PiMFD.Applications.Navigation.MapPages import MapPage

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

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.map_page = MapPage(controller, self)
        self.gas_page = SimpleMessagePage(controller, self, "GAS")
        self.food_page = SimpleMessagePage(controller, self, "FOOD")
        self.traffic_page = SimpleMessagePage(controller, self, "TRAF")
        self.conditions_page = SimpleMessagePage(controller, self, "COND")

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
        super(NavigationApp, self).page_reselected(page)

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """
        pass




