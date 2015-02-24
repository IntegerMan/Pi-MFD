# coding=utf-8

"""
This file contains a data provider for system data
"""
import psutil

from PiMFD.Applications.System.CpuDashboardWidget import CpuDashboardWidget
from PiMFD.Applications.System.DiskPages import DiskDrive

from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, BarChartDashboardWidget


__author__ = 'Matt Eland'


class SystemDataProvider(DataProvider):
    
    last_proc_update = None
    last_perf_update = None
    last_drive_update = None
    last_conn_update = None
    
    process_update_interval = 60
    perf_update_interval = 1
    drives_update_interval = 10
    conn_update_interval = 60

    cpu_widget = None
    drive_widgets = None

    def __init__(self, name, application):
        super(SystemDataProvider, self).__init__(name)

        self.application = application
        self.processes = []
        self.percentages = []
        self.virt_mem = None
        self.swap_mem = None
        self.partitions = []
        self.drives = []
        self.disk_counters = None
        self.connections = []

        if psutil:
            self.has_psutil = True
        else:
            self.has_psutil = False

    def get_dashboard_widgets(self, display, page):

        widgets = []

        # Instantiate CPU Widget as needed
        if not self.cpu_widget and self.percentages and len(self.percentages) > 0:
            self.cpu_widget = CpuDashboardWidget(display, page)

        # Populate / refresh the CPU widget
        if self.cpu_widget:
            self.cpu_widget.values = self.percentages
            widgets.append(self.cpu_widget)
            
        # Instantiate Drive Widgets as Needed
        if (not self.drive_widgets or len(self.drive_widgets) <= 0) and self.drives:
            self.drive_widgets = []
            for drive in self.drives:
                if drive and drive.can_get_usage():
                    widget = BarChartDashboardWidget(display, page, drive.device, value=drive.usage_percent)
                    widget.data_context = drive
                    self.drive_widgets.append(widget)

        # Update Disk Drives
        if self.drive_widgets:
            for drive_widget in self.drive_widgets:
                drive = drive_widget.data_context
                drive_widget.value = drive.usage_percent
                # drive_widget.title = "{} ({} %)".format(drive.device, drive.usage_percent)
                drive_widget.status = drive.get_dashboard_status()
                widgets.append(drive_widget)

        return widgets

    def update(self, now):

        if psutil:

            # Update Perf Data as needed
            if not self.last_perf_update or (now - self.last_perf_update).seconds >= self.perf_update_interval:
                self.percentages = psutil.cpu_percent(percpu=True)
                
                self.last_perf_update = now

            # Update Processes as needed
            if not self.last_proc_update or (now - self.last_proc_update).seconds >= self.process_update_interval:
                self.processes = psutil.get_process_list()
                self.virt_mem = psutil.virtual_memory()
                self.swap_mem = psutil.swap_memory()
                
                self.last_proc_update = now

            # Update Disk Drives
            if not self.last_drive_update or (now - self.last_drive_update).seconds >= self.drives_update_interval:
                self.partitions = psutil.disk_partitions()
                
                # Build a list of drives
                self.drives = []
                if self.partitions:
                    for partition in self.partitions:
                        drive = DiskDrive(partition)
                        self.drives.append(drive)

                # Grab Disk IO over the course of a second
                self.disk_counters = psutil.disk_io_counters(perdisk=True)
                self.disk_counters = psutil.disk_io_counters(perdisk=True)
                self.drive_widgets = None

                self.last_drive_update = now
                
            # Connections
            if not self.last_conn_update or (now - self.last_conn_update).seconds >= self.conn_update_interval:
                try:
                    self.connections = psutil.net_connections(kind='all')
                except psutil.AccessDenied:
                    self.connections = []
                    
                self.last_conn_update = now

        super(SystemDataProvider, self).update(now)