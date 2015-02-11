# coding=utf-8
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.Core.CorePages import SysClockPage, SysExitPage, SettingsPage
from PiMFD.Applications.Core.SystemInfoPage import SysInfoPage

__author__ = 'Matt Eland'


class CoreApplication(MFDApplication):
    """
    The system application.
    """
    services_page = None
    opts_page = None
    exit_page = None

    def __init__(self, controller):
        """
        :type controller: PiMFD.Controller.MFDController
        """
        super(CoreApplication, self).__init__(controller)

        self.sys_info_page = SysInfoPage(controller, self)
        self.clock_page = SysClockPage(controller, self)
        self.opts_page = SettingsPage(controller, self)
        self.exit_page = SysExitPage(controller, self)

        self.pages = list([self.sys_info_page, self.clock_page, self.opts_page, self.exit_page])

    def get_default_page(self):
        """
        Gets the default page for the application
        :return: The default page for the application.
        """
        return self.sys_info_page

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: The button text for the application
        """
        return 'CORE'


