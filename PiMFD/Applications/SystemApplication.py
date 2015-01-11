from PiMFD.Applications.Application import MFDApplication
from PiMFD.Button import MFDButton
from PiMFD.Pages.MFDPage import NotImplementedPage
from PiMFD.Pages.SystemPages import SysClockPage

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):

    clock_page = None
    perf_page = None
    net_page = None
    opts_page = None
    exit_page = None

    def __init__(self, controller):
        super(SysApplication, self).__init__(controller)
        self.clock_page = SysClockPage(controller)
        self.perf_page = NotImplementedPage(controller)
        self.net_page = NotImplementedPage(controller)
        self.opts_page = NotImplementedPage(controller)
        self.exit_page = NotImplementedPage(controller)

    def get_buttons(self):
        buttons = list()
        buttons.append(MFDButton('TIME', selected=(self.controller.active_page == self.clock_page)))
        buttons.append(MFDButton('PERF', selected=(self.controller.active_page == self.perf_page)))
        buttons.append(MFDButton('NET', selected=(self.controller.active_page == self.net_page)))
        buttons.append(MFDButton('OPTS', selected=(self.controller.active_page == self.opts_page)))
        buttons.append(MFDButton('EXIT', selected=(self.controller.active_page == self.exit_page)))
        return buttons

    def get_default_page(self):
        return self.clock_page



