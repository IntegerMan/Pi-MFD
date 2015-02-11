# coding=utf-8
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage
from PiMFD.Applications.System.ServicesPages import ServicesPage
from PiMFD.Applications.System.SystemInfoPage import SysInfoPage

__author__ = 'Matt Eland'


class SysApplication(MFDApplication):
    """
    The system application.
    """
    perf_page = None
    services_page = None
    sys_info_page = None

    def __init__(self, controller):
        """
        :type controller: PiMFD.Controller.MFDController
        """
        super(SysApplication, self).__init__(controller)

        self.sys_info_page = SysInfoPage(controller, self)
        self.perf_page = SimpleMessagePage(controller, self, "PERF")
        self.services_page = ServicesPage(controller, self)

        self.pages = list([self.sys_info_page, self.perf_page, self.services_page])

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
        return 'SYS'


