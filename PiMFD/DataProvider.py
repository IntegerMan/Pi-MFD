# coding=utf-8

"""
This file contains base definitions for data providers
"""
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage

__author__ = 'Matt Eland'


class DataProvider(object):
    def __init__(self, name):
        super(DataProvider, self).__init__()

        self.name = name

    def update(self, now):
        pass

    def get_dashboard_widgets(self, display, page):
        return None
    
    def get_data_details_page(self, controller, application, back_page=None):
        return SimpleMessagePage(controller, application, 'DATA', 'No Data for ' + self.name)