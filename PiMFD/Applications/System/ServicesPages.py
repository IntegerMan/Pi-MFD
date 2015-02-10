# coding=utf-8

"""
Lists running services on this machine using WMI
"""
from wmi import WMI

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt'


class ServicesPage(MFDPage):
    """
    A page containing information on running services
    """

    services = list()
    wmi = None

    def __init__(self, controller, application):
        super(ServicesPage, self).__init__(controller, application)

        self.services = list()

        self.wmi = WMI()

        self.lbl_header = self.get_header_label('RUNNING SERVICES')
        self.pnl_services = StackPanel(controller.display, self)
        self.panel.children = [self.lbl_header, self.pnl_services]

    def handle_unselected(self):
        super(ServicesPage, self).handle_unselected()

    def get_button_text(self):
        return "SRVC"

    def handle_selected(self):
        super(ServicesPage, self).handle_selected()

        self.refresh_services()

    def refresh_services(self):

        self.services = []
        self.pnl_services.children = []

        for s in self.wmi.Win32_Service():
            self.services.append(s)
            lbl = self.get_label("{}: {}".format(s.Caption, s.State))
            self.pnl_services.children.append(lbl)

    def render(self):

        if not self.services or len(self.services) <= 0:
            self.center_text("NO SERVICE DATA AVAILABLE", self.display.color_scheme.highlight)
        else:
            return super(ServicesPage, self).render()

