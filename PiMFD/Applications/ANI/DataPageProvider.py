# coding=utf-8

"""
This file contains logic
"""
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage

__author__ = 'Matt Eland'


class DataPageProvider(object):
    
    def __init__(self, name):
        super(DataPageProvider, self).__init__()

        self.name = name

    def get_data_details_page(self, controller, application, back_page=None):
        return SimpleMessagePage(controller, application, 'DATA', 'No Data for ' + self.name)