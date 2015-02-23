# coding=utf-8

"""
This file contains a data provider for system data
"""
import psutil

from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import DashboardStatus, BarChartDashboardWidget


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

    cpu_widgets = None

    def __init__(self, name, application):
        super(SystemDataProvider, self).__init__(name)

        self.application = application
        self.processes = []
        self.percentages = []
        self.virt_mem = None
        self.swap_mem = None
        self.partitions = []
        self.disk_counters = None
        self.connections = []

        if psutil:
            self.has_psutil = True
        else:
            self.has_psutil = False

    def get_dashboard_widgets(self, display, page):

        widgets = []

        # Build CPU Widgets as necessary
        if not self.cpu_widgets and self.percentages and len(self.percentages) > 0:
            self.cpu_widgets = []
            index = 0
            for percentage in self.percentages:

                index += 1

                if len(self.percentages) > 1:
                    label = "CPU {}".format(index)
                else:
                    label = "CPU"

                widget = BarChartDashboardWidget(display, page, label, value=percentage)
                self.cpu_widgets.append(widget)

        # Populate and refresh the CPU widgets
        if self.cpu_widgets:
            for cpu_widget, percentage in zip(self.cpu_widgets, self.percentages):
                cpu_widget.value = percentage
                widgets.append(cpu_widget)

                if percentage > 95:
                    cpu_widget.status = DashboardStatus.Critical
                elif percentage > 90:
                    cpu_widget.status = DashboardStatus.Caution
                else:
                    cpu_widget.status = DashboardStatus.Passive

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

                # Grab Disk IO over the course of a second
                self.disk_counters = psutil.disk_io_counters(perdisk=True)
                self.disk_counters = psutil.disk_io_counters(perdisk=True)

                self.last_drive_update = now
                
            # Connections
            if not self.last_conn_update or (now - self.last_conn_update).seconds >= self.conn_update_interval:
                try:
                    self.connections = psutil.net_connections(kind='all')
                except psutil.AccessDenied:
                    self.connections = []
                    
                self.last_conn_update = now

        super(SystemDataProvider, self).update(now)