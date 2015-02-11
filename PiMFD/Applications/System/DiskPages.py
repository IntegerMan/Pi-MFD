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
            text = "Device: {} {} {}".format(p.device, p.fstype, p.opts)
            lbl = self.get_label(text)
            #lbl.font = self.controller.display.fonts.small
            self.panel.children.append(lbl)

    def arrange(self):
        return super(DiskDrivesPage, self).arrange()

    def handle_reselected(self):
        self.refresh()
        super(DiskDrivesPage, self).handle_reselected()

    def get_button_text(self):
        return "DRVS"




