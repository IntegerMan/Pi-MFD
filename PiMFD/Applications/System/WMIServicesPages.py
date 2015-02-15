# coding=utf-8

"""
Lists running services on this machine using WMI
"""
import traceback

try:
    # Note: This is not working on Unix. I likely need to find a wrapper that does work before I invest more in WMI.
    from wmi import WMI, x_wmi
except ImportError:
    error_message = "Unhandled error importing WMI {0}\n".format(str(traceback.format_exc()))
    print(error_message)
    WMI = None
    x_wmi = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt'


class WMIServicesPage(MFDPage):
    """
    A page containing information on running services using WMI
    """

    wmi = None
    message = "NO DATA"

    def __init__(self, controller, application):
        super(WMIServicesPage, self).__init__(controller, application)

        self.services = list()

        self.lbl_header = self.get_header_label('SERVICES')
        self.pnl_services = StackPanel(controller.display, self)
        self.panel.children = [self.lbl_header, self.pnl_services]

    def handle_unselected(self):
        super(WMIServicesPage, self).handle_unselected()

    def get_button_text(self):
        return "SRVC"

    def handle_selected(self):
        super(WMIServicesPage, self).handle_selected()

        self.refresh_services()

    def handle_reselected(self):
        super(WMIServicesPage, self).handle_reselected()

        self.refresh_services()

    def refresh_services(self):

        self.wmi = None
        self.pnl_services.children = []
        self.message = None

        sys_path = "127.0.0.1"
        sys_name = None

        if not WMI:
            self.message = "WMI NOT INSTALLED"
            return

        try:
            self.wmi = WMI(sys_path)

        except x_wmi as x:  # Py3+ except wmi.x_wmi as x:
            print "WMI Exception: {}: {}".format(x.com_error.hresult, x.com_error.strerror)
            self.message = x.com_error.strerror
            return

        num_services = 0

        for s in self.wmi.Win32_Service():

            if not sys_name:
                sys_name = s.SystemName

            lbl = self.get_label("{}: {}".format(s.Caption, s.State))
            lbl.font = self.display.fonts.list

            # If it's not running, mark it as disabled color
            if s.State in ("Stopped", "Paused", "Unknown", "Continue Pending", "Start Pending"):
                lbl.is_enabled = False

            self.pnl_services.children.append(lbl)

            num_services += 1

        # Default to path if we need to
        if not sys_name:
            sys_name = sys_path

        self.lbl_header.text = "{} SERVICES ({})".format(sys_name, num_services).upper()

    def render(self):

        if len(self.pnl_services.children) <= 0 and self.message:
            self.center_text(self.message.upper(), self.display.color_scheme.highlight)
        else:
            return super(WMIServicesPage, self).render()

