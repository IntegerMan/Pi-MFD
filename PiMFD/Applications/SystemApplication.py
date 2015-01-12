from PiMFD.Applications.Application import MFDApplication
from PiMFD.Pages.MFDPage import SimpleMessagePage
from PiMFD.Pages.SystemPages import SysClockPage, SysRootPage

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):

    root_page = None
    active_page = None
    clock_page = None
    perf_page = None
    net_page = None
    opts_page = None
    exit_page = None

    def __init__(self, controller):

        super(SysApplication, self).__init__(controller)

        self.root_page = SysRootPage(controller, self)

        self.clock_page = SysClockPage(controller, self)
        self.perf_page = SimpleMessagePage(controller, self, "PERF")
        self.net_page = SimpleMessagePage(controller, self, "NET")
        self.opts_page = SimpleMessagePage(controller, self, "OPTS")
        self.exit_page = SimpleMessagePage(controller, self, "EXIT")

        self.pages = list([self.clock_page, self.perf_page, self.net_page, self.opts_page, self.exit_page])

    def get_default_page(self):
        return self.root_page

    def get_button_text(self):
        return 'SYS'


