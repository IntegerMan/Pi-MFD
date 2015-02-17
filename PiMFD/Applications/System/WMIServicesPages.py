# coding=utf-8

"""
Lists running services on this machine using WMI
"""
from threading import Thread
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


class WMIServiceLoader(Thread):
    
    def __init__(self, page, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(WMIServiceLoader, self).__init__(group, target, name, args, kwargs, verbose)
        
        self.page = page

    def run(self):
        super(WMIServiceLoader, self).run()

        self.page.pnl_services.children = []
        self.page.message = "Loading Services"

        sys_path = "127.0.0.1"

        if not WMI:
            self.page.message = "WMI NOT INSTALLED"
            return

        try:
            wmi = WMI(sys_path)
            services = wmi.Win32_Service()
            self.page.is_loading_services = False

        except x_wmi as x:  # Py3+ except wmi.x_wmi as x:
            self.page.message = x.com_error.strerror
            return
        
        self.page.message = None
        num_services = len(services)
        self.page.lbl_header.text = "SERVICES ({})".format(num_services).upper()

        for s in services:

            lbl = self.page.get_list_label("{}: {}".format(s.Caption, s.State))

            # If it's not running, mark it as disabled color
            if s.State in ("Stopped", "Paused", "Unknown", "Continue Pending", "Start Pending"):
                lbl.is_enabled = False

            self.page.pnl_services.children.append(lbl)


class WMIServicesPage(MFDPage):
    """
    A page containing information on running services using WMI
    """

    wmi = None
    message = "NO DATA"

    def __init__(self, controller, application):
        super(WMIServicesPage, self).__init__(controller, application)

        self.services = list()

        self.lbl_header = self.get_header_label('Services')
        self.pnl_services = StackPanel(controller.display, self)
        self.panel.children = [self.lbl_header, self.pnl_services]
        
        self.refresh_services()

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
        
        loader = WMIServiceLoader(self)
        loader.start()

    def render(self):

        if len(self.pnl_services.children) <= 0 and self.message:
            self.center_text(self.message.upper(), self.display.color_scheme.highlight)
        else:
            return super(WMIServicesPage, self).render()

