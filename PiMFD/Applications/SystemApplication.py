from PiMFD.Applications.Application import MFDApplication
from PiMFD.Button import MFDButton
from PiMFD.Pages.MFDPage import SimpleMessagePage
from PiMFD.Pages.SystemPages import SysClockPage

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):

    pages = list()
    clock_page = None
    perf_page = None
    net_page = None
    opts_page = None
    exit_page = None

    def __init__(self, controller):

        super(SysApplication, self).__init__(controller)

        self.clock_page = SysClockPage(controller)
        self.perf_page = SimpleMessagePage(controller, "PERF")
        self.net_page = SimpleMessagePage(controller, "NET")
        self.opts_page = SimpleMessagePage(controller, "OPTS")
        self.exit_page = SimpleMessagePage(controller, "EXIT")

        self.pages = list([self.clock_page, self.perf_page, self.net_page, self.opts_page, self.exit_page])

    def get_buttons(self):
        buttons = list()
        for page in self.pages:
            buttons.append(MFDButton(page.get_button_text(), selected=(self.controller.active_page is page)))

        return buttons

    def get_default_page(self):
        return self.clock_page

    def get_button_text(self):
        return 'SYS'


