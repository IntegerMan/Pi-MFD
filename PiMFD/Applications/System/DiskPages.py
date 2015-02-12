# coding=utf-8
import psutil
from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt Eland'


class DiskDrivesPage(MFDPage):

    partitions = None

    def __init__(self, controller, application, auto_scroll=True):
        super(DiskDrivesPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self,):

        self.partitions = psutil.disk_partitions(all=True)

        self.panel.children.append(self.get_header_label('Disk Drives'))
        for p in self.partitions:

            drive = p.device
            options = p.opts.upper()
            file_system = p.fstype

            # Determine if it's a CD-Drive
            if 'CDROM' in options or file_system == '':

                # For CD-ROM Drives, we don't want to grab usage information
                text = "{} {}".format(drive, options)

            else:

                # Normal disk - display information on availability / etc.
                usage = psutil.disk_usage(p.mountpoint)
                percent = usage.percent
                text = "{} {} {} ({} % Full)".format(drive, file_system, options, percent)

            lbl = self.get_label(text)
            self.panel.children.append(lbl)

    def arrange(self):
        return super(DiskDrivesPage, self).arrange()

    def handle_reselected(self):
        self.refresh()
        super(DiskDrivesPage, self).handle_reselected()

    def get_button_text(self):
        return "DRVS"




