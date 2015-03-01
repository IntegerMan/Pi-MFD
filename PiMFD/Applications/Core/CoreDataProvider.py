# coding=utf-8

"""
This file contains the core module data provider
"""
from datetime import datetime
from time import strftime

from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, DashboardStatus, BarChartDashboardWidget


__author__ = 'Matt Eland'


class CoreDataProvider(DataProvider):
    """
    A data provider for the core module. Very simple and only contains system time information.
    :param application: The application
    :type application: MFDApplication
    """
    date_time_format = '%m/%d/%Y - %H:%M:%S'
    time_format = '%H:%M:%S'
    date_format = '%m/%d/%Y'

    def __init__(self, application):
        super(CoreDataProvider, self).__init__("Core Data Provider")

        self.application = application
        
        self.system_time = ''
        self.time_widget = None
        self.fps_widget = None

    def update(self, now):
        super(CoreDataProvider, self).update(now)

        self.system_time = strftime(self.time_format)

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
        
        # Prepare the Frames Per Second Widget
        
        fps = display.clock.get_fps()
        
        if not self.fps_widget:
            #  Pad a bit extra on to the Max FPS since some machines seem to render (or at least record) a bit over target
            self.fps_widget = BarChartDashboardWidget(display, page, "FPS", value=fps, range_high=display.frames_per_second + 5)
        else:
            self.fps_widget.value = fps
            
        # Calculate Status of FPS. Keep in mind that we can target 30 or 60 FPS depending on platform
        if fps <= 0:
            self.fps_widget.status = DashboardStatus.Inactive
        elif fps <= (display.frames_per_second * 0.5):
            self.fps_widget.status = DashboardStatus.Critical
        elif fps <= (display.frames_per_second - 5):
            self.fps_widget.status = DashboardStatus.Caution
        else:
            self.fps_widget.status = DashboardStatus.Passive
        
        return [self.time_widget, self.fps_widget]