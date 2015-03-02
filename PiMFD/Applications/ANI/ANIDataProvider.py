# coding=utf-8

"""
This file contains the data provider for the ANI application
"""
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class ANIDataProvider(DataProvider):
    """
    The data provider for the ANI application.
    """
    
    def __init__(self, name):
        super(ANIDataProvider, self).__init__(name)

    def get_dashboard_widgets(self, display, page):
        return None

    def update(self, now):
        super(ANIDataProvider, self).update(now)