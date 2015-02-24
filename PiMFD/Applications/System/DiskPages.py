# coding=utf-8

"""
Contains Disk Drive Pages
"""
from datetime import datetime

from PiMFD.Applications.System.ByteFormatting import format_size
from PiMFD.UI.Widgets.Charts import BarChart
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Widgets.DashboardWidget import DashboardStatus


try:
    import psutil
    from psutil._common import sdiskpart
except ImportError:
    psutil = None
    sdiskpart = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import MenuItem

__author__ = 'Matt Eland'


class DiskDrive(object):
    def __init__(self, partition):
        """
        :type partition: sdiskpart
        """
        super(DiskDrive, self).__init__()

        # Extract things out of the partition object
        self.device = partition.device
        self.options = partition.opts.upper()
        self.mountpoint = partition.mountpoint
        self.file_system = partition.fstype
        self.counters = None
        self.old_counters = None
        self.counter_key = None

        if self.can_get_usage():

            # Normal disk - display information on availability / etc.
            self.usage = psutil.disk_usage(self.mountpoint)
            self.usage_percent = self.usage.percent

        else:
            self.usage = None
            self.usage_percent = 0.0

    def get_dashboard_status(self):
        
        if not self.can_get_usage():
            return DashboardStatus.Inactive
        elif self.usage_percent >= 90:
            return DashboardStatus.Critical
        elif self.usage_percent >= 60:
            return DashboardStatus.Caution
        else:
            return DashboardStatus.Passive

    def can_get_usage(self):
        return not ('CDROM' in self.options or self.file_system == '')

    def get_display_text(self):

        # Determine if it's a CD-Drive
        if not self.can_get_usage():

            # For CD-ROM Drives, we don't want to grab usage information
            text = "{} {}".format(self.device, self.options)

        else:
            text = "{} {} {} ({} % Full)".format(self.device, self.file_system, self.options,
                                                 self.usage_percent)

        return text

    def get_general_info(self):

        yield "Device: {}".format(self.device)
        yield "Mount Point: {}".format(self.mountpoint)
        yield "File System: {}".format(self.file_system)
        yield "Options: {}".format(self.options)

    def get_storage_info(self):
        if self.can_get_usage():
            yield "{} % Full".format(self.usage.percent)
            yield "Storage Space: {}".format(format_size(self.usage.total))
            yield "Space Used: {}".format(format_size(self.usage.used))
            yield "Space Free: {}".format(format_size(self.usage.free))

    def get_performance_info(self):
        if self.counters:
            c = self.counters
            if self.old_counters:
                o = self.old_counters
                #  yield "{}".format(self.counter_key)
                yield "Read Count: {}".format(c.read_count - o.read_count)
                yield "Read Bytes: {}".format(format_size(c.read_bytes - o.read_bytes))
                yield "Read Time: {}".format(c.read_time - o.read_time)
                yield "Write Count: {}".format(c.write_count - o.write_count)
                yield "Write Bytes: {}".format(format_size(c.write_bytes - o.write_bytes))
                yield "Write Time: {}".format(c.write_time - o.write_time)
            else:
                yield "Measuring..."

    def load_counters(self, key, counters):
        self.counter_key = key
        self.old_counters = self.counters
        self.counters = counters

    def refresh_counters(self):

        counters = psutil.disk_io_counters(perdisk=True)

        self.load_counters(self.counter_key, counters[self.counter_key])

class DiskDrivesPage(MFDPage):
    """
    A page displaying a list of disk drives on this machine.
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type auto_scroll: bool
    """

    def __init__(self, controller, application, auto_scroll=True):
        super(DiskDrivesPage, self).__init__(controller, application, auto_scroll)

        self.last_refresh = datetime.now()
        self.selected_device = None

    def refresh(self):

        """
        Refreshes the list of drives
        """

        counter_index = 0

        self.panel.children = [
            self.get_header_label('Drives ({})'.format(len(self.application.data_provider.partitions)))]

        is_first_control = True

        drives = list()

        for p in self.application.data_provider.partitions:

            drive = DiskDrive(p)
            drives.append(drive)

            if drive.can_get_usage() and counter_index < len(self.application.data_provider.disk_counters):
                key = "PhysicalDrive" + str(counter_index)
                if key in self.application.data_provider.disk_counters:
                    drive.load_counters(key, self.application.data_provider.disk_counters[key])
                else:
                    key = self.application.data_provider.disk_counters.keys()[counter_index]
                    drive.load_counters(key, self.application.data_provider.disk_counters[key])
                counter_index += 1

            text = drive.get_display_text()

            lbl = self.get_list_label(text)
            chart = BarChart(self.display, self, float(drive.usage_percent), width=lbl.font.size * 2,
                             height=lbl.font.size)
            sp = StackPanel(self.display, self, is_horizontal=True)
            sp.children = [chart, lbl]

            mi = MenuItem(self.controller.display, self, sp)
            mi.data_context = drive

            self.panel.children.append(mi)

            if is_first_control and not self.selected_device:
                self.set_focus(mi, play_sound=False)
                is_first_control = False
            elif self.selected_device and self.selected_device == drive.device:
                self.set_focus(mi, play_sound=False)

    def set_focus(self, widget, play_sound=True):
        
        if widget and widget.data_context:
            self.selected_device = widget.data_context.device
        else:
            self.selected_device = None
        
        return super(DiskDrivesPage, self).set_focus(widget, play_sound=play_sound)

    def arrange(self):
        """
        Arranges the control to the page
        :return: The desired size of the page
        """
            
        return super(DiskDrivesPage, self).arrange()

    def render(self):

        """
        Renders the control to the screen
        :return: The rectangle of the control
        """
        if not self.application.data_provider.has_psutil:
            self.center_text("System Monitoring Offline".upper())

        return super(DiskDrivesPage, self).render()

    def handle_reselected(self):
        """
        Handles the reselected event
        """
        self.refresh()
        super(DiskDrivesPage, self).handle_reselected()

    def get_button_text(self):
        """
        Gets the text for this page's button
        :return: The text for this page's button
        :rtype: str
        """
        return "DRVS"

    def handle_control_state_changed(self, widget):

        drive = widget.data_context

        if drive:
            self.application.select_page(DiskDetailsPage(self.controller, self.application, drive))

        super(DiskDrivesPage, self).handle_control_state_changed(widget)


class DiskDetailsPage(MFDPage):
    """
    A page detailing an individual disk drive.
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type drive: DiskDrive
    :type auto_scroll: bool
    """
    drive = None
    perf_panel = None

    def __init__(self, controller, application, drive, auto_scroll=True):
        super(DiskDetailsPage, self).__init__(controller, application, auto_scroll)

        self.drive = drive

        self.segment_panel = StackPanel(self.display, self, is_horizontal=True, auto_orient=True, keep_together=True)
        self.panel.children = [self.get_header_label("Drive Information"), self.segment_panel]

        # Display basic attributes for the drive
        general_panel = StackPanel(self.display, self)
        general_panel.children.append(self.get_label("General"))
        for info_item in self.drive.get_general_info():
            lbl = self.get_label(info_item)
            lbl.font = self.controller.display.fonts.list
            general_panel.children.append(lbl)
        self.segment_panel.children.append(general_panel)

        if drive.can_get_usage():
            usage_panel = StackPanel(self.display, self)
            usage_panel.children.append(self.get_label("Storage"))
            for info_item in self.drive.get_storage_info():
                lbl = self.get_list_label(info_item)
                if info_item.endswith('% Full'):
                    chart = BarChart(self.display, self, value=float(self.drive.usage_percent))
                    chart.height = lbl.font.size
                    chart.width = lbl.font.size
                    pnl = StackPanel(self.display, self, is_horizontal=True)
                    pnl.children = [chart, lbl]
                    usage_panel.children.append(pnl)
                else:
                    usage_panel.children.append(lbl)

            self.segment_panel.children.append(usage_panel)

        if self.drive.counters:
            self.perf_panel = StackPanel(self.display, self)
            self.refresh_performance_counters()
            self.segment_panel.children.append(self.perf_panel)
            self.last_refresh = datetime.now()

    def refresh_performance_counters(self):

        if self.drive.counters:

            self.drive.refresh_counters()

            self.perf_panel.children = [self.get_label("Performance")]
            for info_item in self.drive.get_performance_info():
                lbl = self.get_label(info_item)
                lbl.font = self.controller.display.fonts.list
                self.perf_panel.children.append(lbl)

    def arrange(self):

        if self.drive.counter_key:

            now = datetime.now()

            delta = now - self.last_refresh
            if delta.seconds >= 1:
                self.last_refresh = now
                self.refresh_performance_counters()                
        
        return super(DiskDetailsPage, self).arrange()

    def render(self):
        return super(DiskDetailsPage, self).render()

    def get_button_text(self):
        return "INFO"