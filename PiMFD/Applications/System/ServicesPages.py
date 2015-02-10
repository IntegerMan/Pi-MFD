# coding=utf-8

"""
Lists running services on this machine using WMI
"""
import platform
from wmi import WMI, x_wmi

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt'


class ServicesPage(MFDPage):
    """
    A page containing information on running services
    """

    wmi = None
    message = "NO DATA"

    def __init__(self, controller, application):
        super(ServicesPage, self).__init__(controller, application)

        self.services = list()

        self.lbl_header = self.get_header_label('SERVICES')
        self.pnl_services = StackPanel(controller.display, self)
        self.panel.children = [self.lbl_header, self.pnl_services]

    def handle_unselected(self):
        super(ServicesPage, self).handle_unselected()

    def get_button_text(self):
        return "SRVC"

    def handle_selected(self):
        super(ServicesPage, self).handle_selected()

        self.refresh_services()

    def handle_reselected(self):
        super(ServicesPage, self).handle_reselected()

        self.refresh_services()

    def refresh_services(self):

        self.wmi = None
        self.pnl_services.children = []
        self.message = None

        try:
            self.wmi = WMI("damocles")

        except x_wmi as x:  # Py3+ except wmi.x_wmi as x:
            print "WMI Exception: {}: {}".format(x.com_error.hresult, x.com_error.strerror)
            self.message = x.com_error.strerror
            return

        num_services = 0

        for s in self.wmi.Win32_Service():

            lbl = self.get_label("{}: {}".format(s.Caption, s.State))

            # If it's not running, mark it as disabled color
            if s.State in ("Stopped", "Paused", "Unknown", "Continue Pending", "Start Pending"):
                lbl.is_enabled = False

            self.pnl_services.children.append(lbl)

            num_services += 1

        self.lbl_header.text = "{} SERVICES ({})".format(platform.node(), num_services).upper()

    def render(self):

        if len(self.pnl_services.children) <= 0 and self.message:
            self.center_text(self.message.upper(), self.display.color_scheme.highlight)
        else:
            return super(ServicesPage, self).render()

