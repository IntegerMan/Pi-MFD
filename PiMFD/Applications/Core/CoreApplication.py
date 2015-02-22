# coding=utf-8
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.Core.CorePages import SysExitPage, DashboardPage
from PiMFD.Applications.Core.SettingsPage import SettingsPage
from PiMFD.Applications.Core.SystemInfoPage import SysInfoPage

__author__ = 'Matt Eland'


class CoreApplication(MFDApplication):
    """
    The system application.
    """
    services_page = None
    opts_page = None
    exit_page = None
    data_provider = None

    def __init__(self, controller):
        """
        :type controller: PiMFD.Controller.MFDController
        """
        super(CoreApplication, self).__init__(controller)

        self.dash_page = DashboardPage(controller, self)
        self.sys_info_page = SysInfoPage(controller, self)
        self.opts_page = SettingsPage(controller, self)
        self.exit_page = SysExitPage(controller, self)

        self.pages = list([self.dash_page, self.sys_info_page, self.opts_page, self.exit_page])

    def get_default_page(self):
        """
        Gets the default page for the application
        :return: The default page for the application.
        """
        return self.dash_page

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: The button text for the application
        """
        return 'CORE'

    def initialize(self):
        super(CoreApplication, self).initialize()

        self.controller.register_data_provider(self.data_provider)

    

