# coding=utf-8

"""
This file contains the core module data provider
"""
from datetime import datetime
from time import strftime, gmtime

from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class CoreDataProvider(DataProvider):
    """
    A data provider for the core module. Very simple and only contains system time information.
    :param application: The application
    :type application: MFDApplication
    """
    time_format = '%m/%d/%Y - %H:%M:%S'

    def __init__(self, application):
        super(CoreDataProvider, self).__init__("Core Data Provider")

        self.application = application
        
        self.system_time = ''
        self.gmt_time = ''
        self.time_widget = None

    def update(self):
        super(CoreDataProvider, self).update()

        self.system_time = strftime(self.time_format)
        self.gmt_time = strftime(self.time_format, gmtime())

    def get_dashboard_widgets(self, display, page):

        if not self.time_widget:
            # Build out the widget
            self.time_widget = TextDashboardWidget(display, page, "System Time", self.system_time)
        else:
            # Update with current system time
            self.time_widget.value = self.system_time
        
        # Set status based on time of day
        hour = datetime.now().hour
        if hour >= 23 or hour == 0 or hour == 6:
            status = DashboardStatus.Caution
        elif 1 <= hour <= 5:
            status = DashboardStatus.Critical
        else:
            status = DashboardStatus.Passive
            
        self.time_widget.status = status
        
        return [self.time_widget]