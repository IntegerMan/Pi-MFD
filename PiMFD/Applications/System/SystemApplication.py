# coding=utf-8
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.MFDPage import SimpleMessagePage
from PiMFD.Applications.System.SystemPages import SysRootPage, SysClockPage, SysExitPage, SettingsPage

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):
    """
    The system application.
    :type controller: PiMFD.Controller.MFDController The controller
    """
    root_page = None
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
        self.opts_page = SettingsPage(controller, self)
        self.exit_page = SysExitPage(controller, self)

        self.pages = list([self.clock_page, self.perf_page, self.net_page, self.opts_page, self.exit_page])

    def get_default_page(self):
        """
        Gets the default page for the application
        :return: The default page for the application.
        """
        return self.root_page

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: The button text for the application
        """
        return 'SYS'


