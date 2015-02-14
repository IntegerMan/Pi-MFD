# coding=utf-8

"""
Contains Computer Performance Pages
"""
from datetime import datetime

from PiMFD.UI.Panels import StackPanel


try:
    import psutil
except ImportError:
    psutil = None

from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt Eland'


class PerformancePage(MFDPage):
    """
    A page displaying machine performance.
    :type controller: PiMFD.Controller.MFDController
    :type application: PiMFD.Applications.System.SystemApplication.SysApplication
    :type auto_scroll: bool
    """
    drives = None

    def __init__(self, controller, application, auto_scroll=True):
        super(PerformancePage, self).__init__(controller, application, auto_scroll)

        self.pnl_cpu = StackPanel(controller.display, self)

        self.panel.children = [self.pnl_cpu]

        self.refresh()

        self.last_refresh = datetime.now()

    def refresh(self):

        """
        Refreshes the list of drives
        """

        self.pnl_cpu.children = [self.get_header_label('CPU Performance')]
        percentages = psutil.cpu_percent(percpu=True)

        cpu_index = 1
        for percent in percentages:
            lbl = self.get_label('{}: {:02.1f} %'.format(cpu_index, percent))
            lbl.font = self.controller.display.fonts.list
            self.pnl_cpu.children.append(lbl)
            cpu_index += 1


    def arrange(self):
        """
        Arranges the control to the page
        :return: The desired size of the page
        """

        if psutil:
            now = datetime.now()

            delta = now - self.last_refresh
            if delta.seconds >= 1:
                self.last_refresh = now
                self.refresh()

        return super(PerformancePage, self).arrange()

    def render(self):

        """
        Renders the control to the screen
        :return: The rectangle of the control
        """
        if not psutil:
            self.center_text("psutil offline".upper())

        return super(PerformancePage, self).render()

    def handle_reselected(self):
        """
        Handles the reselected event
        """
        self.refresh()
        super(PerformancePage, self).handle_reselected()

    def get_button_text(self):
        """
        Gets the text for this page's button
        :return: The text for this page's button
        :rtype: str
        """
        return "PERF"


