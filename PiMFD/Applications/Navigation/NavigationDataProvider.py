# coding=utf-8

"""
This file contains a data provider for navigation-related items.
"""
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class NavigationDataProvider(DataProvider):
    """
    A DataProvider for the NavigationApplication.
    :param name: The name of the data provider
    """

    def __init__(self, name="Navigation Data Provider"):
        super(NavigationDataProvider, self).__init__(name)

    def update(self, now):
        super(NavigationDataProvider, self).update(now)

    def get_dashboard_widgets(self, display, page):
        super(NavigationDataProvider, self).get_dashboard_widgets(display, page)

