# coding=utf-8

"""
Contains Disk Drive Pages
"""

try:
    import psutil
except ImportError:
    psutil = None

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Widgets.MenuItem import MenuItem


__author__ = 'Matt Eland'


class DiskDrivesPage(MFDPage):
    """
    A page displaying a list of disk drives on this machine.
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type auto_scroll: bool
    """
    partitions = None

    def __init__(self, controller, application, auto_scroll=True):
        super(DiskDrivesPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self):

        """
        Refreshes the list of drives
        """
        
        if not psutil:
            self.partitions = None
            return

        self.partitions = psutil.disk_partitions(all=True)

        self.panel.children.append(self.get_header_label('Drives ({})'.format(len(self.partitions))))

        is_first_control = True
        
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

            lbl = MenuItem(self.controller.display, self, text)
            lbl.font = self.controller.display.fonts.list
            self.panel.children.append(lbl)

            if is_first_control:
                self.set_focus(lbl)
                is_first_control = False

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
        if not psutil:
            self.center_text("psutil offline".upper())

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




