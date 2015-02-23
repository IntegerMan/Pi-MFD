# coding=utf-8

"""
This file contains a data provider for system data
"""
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class SystemDataProvider(DataProvider):
    def __init__(self, name, application):
        super(SystemDataProvider, self).__init__(name)
        self.application = application

    def get_dashboard_widgets(self, display, page):
        return []

    def update(self):
        super(SystemDataProvider, self).update()