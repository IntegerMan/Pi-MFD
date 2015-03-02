# coding=utf-8

"""
This file contains a definition for the ANI application
"""
from PiMFD.Applications.ANI.ANIDataProvider import ANIDataProvider
from PiMFD.Applications.ANI.DataCategoriesPage import DataCategoriesPage
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage

__author__ = 'Matt Eland'


class ANIApplication(MFDApplication):

    data_provider = None
    
    data_page = None
    options_page = None

    def __init__(self, controller):
        super(ANIApplication, self).__init__(controller)
        
        self.data_provider = ANIDataProvider("ANI Data Provider")

        self.data_page = DataCategoriesPage(controller, self)
        self.options_page = SimpleMessagePage(controller, self, "OPTS")

    def handle_reselected(self):
        super(ANIApplication, self).handle_reselected()

    def page_reselected(self, page):
        super(ANIApplication, self).page_reselected(page)

    def get_button_text(self):
        return "ANI"

    def get_default_page(self):
        return self.data_page

    def get_buttons(self):
        return [self.data_page.get_button(), self.options_page.get_button()]

    def select_page_by_index(self, index):
        
        if index == 0:
            self.select_page(self.data_page)
        elif index == 1:
            self.select_page(self.options_page)
        
        super(ANIApplication, self).select_page_by_index(index)