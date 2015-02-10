# coding=utf-8

"""
Lists running services on this machine using WMI
"""
from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt'


class ServicesPage(MFDPage):
    def __init__(self, controller, application):
        super(ServicesPage, self).__init__(controller, application)

    def handle_unselected(self):
        super(ServicesPage, self).handle_unselected()

    def get_button_text(self):
        return "SRVC"

    def handle_selected(self):
        super(ServicesPage, self).handle_selected()

    def render(self):
        self.center_text("NO DATA", self.display.color_scheme.highlight)

        return super(ServicesPage, self).render()

