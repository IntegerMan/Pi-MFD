# coding=utf-8

"""
This file contains a traffic data page
"""
from PiMFD.Applications.ANI.DataCategoriesPage import DataPage
from PiMFD.Applications.ANI.DataPageProvider import DataPageProvider
from PiMFD.UI.Button import MFDButton

__author__ = 'Matt Eland'


class TrafficDataPageProvider(DataPageProvider):
    data_provider = None

    def __init__(self, data_provider):
        super(TrafficDataPageProvider, self).__init__("Traffic Data Provider")

        self.data_provider = data_provider

    def get_data_details_page(self, controller, application, back_page=None):
        return TrafficDataPage(controller, application, back_page, self, self.data_provider)


class TrafficDataPage(DataPage):
    def __init__(self, controller, application, back_page, page_provider, data_provider, auto_scroll=True):
        super(TrafficDataPage, self).__init__(controller, application, page_provider, auto_scroll)
        
        self.back_page = back_page
        self.btn_back = MFDButton("BACK")
        self.data_provider = data_provider
        
    def arrange(self):
        return super(TrafficDataPage, self).arrange()

    def render(self):
        return super(TrafficDataPage, self).render()

    def get_button_text(self):
        return "TRFC"

    def get_lower_buttons(self):
        return [self.btn_back]

    def handle_lower_button(self, index):
        
        if index == 0 and self.back_page:
            self.application.select_page(self.back_page)
            return
        
        return super(TrafficDataPage, self).handle_lower_button(index)
