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


class DiskDrive(object):
    pass
    

class DiskDrivesPage(MFDPage):
    """
    A page displaying a list of disk drives on this machine.
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type auto_scroll: bool
    """
    drives = None

    def __init__(self, controller, application, auto_scroll=True):
        super(DiskDrivesPage, self).__init__(controller, application, auto_scroll)

        self.refresh()

    def refresh(self):

        """
        Refreshes the list of drives
        """
        
        if not psutil:
            self.drives = None
            return

        partitions = psutil.disk_partitions(all=True)

        self.panel.children.append(self.get_header_label('Drives ({})'.format(len(partitions))))

        is_first_control = True

        drives = list()

        for p in partitions:

            drive = DiskDrive()

            drives.append(drive)

            drive.device = p.device
            drive.options = p.opts.upper()
            drive.file_system = p.fstype

            # Determine if it's a CD-Drive
            if 'CDROM' in drive.options or drive.file_system == '':

                # For CD-ROM Drives, we don't want to grab usage information
                text = "{} {}".format(drive.device, drive.options)

            else:

                # Normal disk - display information on availability / etc.
                drive.usage = psutil.disk_usage(p.mountpoint)
                drive.usage_percent = drive.usage.percent
                text = "{} {} {} ({} % Full)".format(drive.device, drive.file_system, drive.options,
                                                     drive.usage_percent)

            lbl = MenuItem(self.controller.display, self, text)
            lbl.data_context = drive
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

    def handle_control_state_changed(self, widget):

        drive = widget.data_context

        if drive:
            self.application.select_page(DiskDetailsPage(self.controller, self.application, drive))

        super(DiskDrivesPage, self).handle_control_state_changed(widget)


class DiskDetailsPage(MFDPage):
    drive = None

    def __init__(self, controller, application, drive, auto_scroll=True):
        super(DiskDetailsPage, self).__init__(controller, application, auto_scroll)

        self.drive = drive

        self.panel.children.append(self.get_header_label("Drive Information"))

        # Grab all attributes of the drive and show them around
        self.panel.children.append(self.get_label("General"))
        for key in self.drive.__dict__.keys():
            lbl = self.get_label("{}: {}".format(key, self.drive.__dict__[key]))
            lbl.font = self.controller.display.fonts.list
            self.panel.children.append(lbl)


    def arrange(self):
        return super(DiskDetailsPage, self).arrange()

    def render(self):
        return super(DiskDetailsPage, self).render()

    def get_button_text(self):
        return "INFO"        
    

        
    