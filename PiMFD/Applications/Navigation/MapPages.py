# coding=utf-8

"""
This file will hold map pages
"""
from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt Eland'


class MapPage(MFDPage):
    lbl_loading = None

    def __init__(self, controller, application):
        super(MapPage, self).__init__(controller, application)

        self.lbl_loading = self.get_label("{}")

        self.panel.children = (self.lbl_loading,)

    def get_button_text(self):
        return "MAP"

    def render(self):
        self.lbl_loading.text_data = self.application.map.status_text

        self.center_text('NO DATA')

        return super(MapPage, self).render()



