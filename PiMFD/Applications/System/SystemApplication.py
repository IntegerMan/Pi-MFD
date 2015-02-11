# coding=utf-8
from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage
from PiMFD.Applications.System.ServicesPages import ServicesPage

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

        self.perf_page = SimpleMessagePage(controller, self, "PERF")
        self.proc_page = SimpleMessagePage(controller, self, "PROC")
        self.disk_page = SimpleMessagePage(controller, self, "DISK")
        self.net_page = SimpleMessagePage(controller, self, "NET")
        self.services_page = ServicesPage(controller, self)

        self.pages = list([self.perf_page, self.disk_page, self.services_page, self.proc_page, self.net_page])

    def get_default_page(self):
        """
        Gets the default page for the application
        :return: The default page for the application.
        """
        return self.perf_page

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: The button text for the application
        """
        return 'SYS'


