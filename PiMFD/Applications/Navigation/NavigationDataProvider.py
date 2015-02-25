# coding=utf-8

"""
This file contains a data provider for navigation-related items.
"""
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class NavigationDataProvider(DataProvider):
    """
    A DataProvider for the NavigationApplication.
    :param name: The name of the data provider
    """

    def __init__(self, application, map, name="Navigation Data Provider"):
        super(NavigationDataProvider, self).__init__(name)

        self.map = map
        self.application = application

        self.map_context = MapContext(self.application, self.map)

    def update(self, now):
        super(NavigationDataProvider, self).update(now)

    def get_dashboard_widgets(self, display, page):
        super(NavigationDataProvider, self).get_dashboard_widgets(display, page)

