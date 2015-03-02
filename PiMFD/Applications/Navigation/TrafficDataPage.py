# coding=utf-8

"""
This file contains a traffic data page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Button import MFDButton

__author__ = 'Matt Eland'


class TrafficDataPage(MFDPage):

    def __init__(self, controller, application, back_page, auto_scroll=True):
        super(TrafficDataPage, self).__init__(controller, application, auto_scroll)
        
        self.back_page = back_page
        self.btn_back = MFDButton("BACK")
        
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
                
    
