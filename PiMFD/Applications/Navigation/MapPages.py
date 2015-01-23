# coding=utf-8

"""
This file will hold map pages
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.Applications.Navigation.MapRendering import MapRenderer

__author__ = 'Matt Eland'


class MapPage(MFDPage):

    lbl_loading = None
    map_renderer = None

    def __init__(self, controller, application):
        super(MapPage, self).__init__(controller, application)

        self.map_renderer = MapRenderer(application.map, controller.display)

    def get_button_text(self):
        return "MAP"

    def render(self):

        if self.application.map.has_data:
            self.map_renderer.render()
        else:
            self.center_text('NO DATA')

        return super(MapPage, self).render()



