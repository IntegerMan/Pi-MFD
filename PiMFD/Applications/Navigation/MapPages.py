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

        self.lbl_loading = self.get_label("Loading Map Data...")

        self.panel.children = (self.lbl_loading,)

    def get_button_text(self):
        return "MAP"

