# coding=utf-8
import psutil

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.System.DiskPages import DiskDrivesPage
from PiMFD.Applications.System.NetworkPages import NetworkPage
from PiMFD.Applications.System.PerformancePages import PerformancePage
from PiMFD.Applications.System.ProcessPages import ProcessPage, ProcessDetailsPage
from PiMFD.Applications.System.SystemDataProvider import SystemDataProvider
from PiMFD.Applications.System.WMIServicesPages import WMIServicesPage


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

        self.perf_page = PerformancePage(controller, self)
        self.proc_page = ProcessPage(controller, self)
        self.disk_page = DiskDrivesPage(controller, self)
        self.net_page = NetworkPage(controller, self)
        self.services_page = WMIServicesPage(controller, self)
        self.system_data_provider = SystemDataProvider("System Data Provider", self)

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

    def navigate_to_process(self, pid):
        try:
            processes = psutil.get_process_list()
        except psutil.AccessDenied:
            processes = None

        if processes:

            # Find the process from the list
            proc = None
            for p in processes:
                if p.pid == pid:
                    proc = p
                    break

            if proc:
                self.select_page(ProcessDetailsPage(self.controller, self, proc))

    def initialize(self):
        super(SysApplication, self).initialize()

        self.controller.register_data_provider(self.system_data_provider)


