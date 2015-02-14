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
        self.pnl_virt_mem = StackPanel(controller.display, self)
        self.pnl_swap_mem = StackPanel(controller.display, self)

        self.panel.is_horizontal = True
        self.panel.auto_scroll = True
        self.panel.children = [self.pnl_cpu, self.pnl_virt_mem, self.pnl_swap_mem]

        self.refresh()

        self.last_refresh = datetime.now()

    def refresh(self):

        """
        Refreshes the list of drives
        """

        # CPU Usage        
        self.pnl_cpu.children = [self.get_header_label('CPU Performance')]
        percentages = psutil.cpu_percent(percpu=True)

        if percentages:
            cpu_index = 1
            for percent in percentages:

                # Protect against bad values on first round
                if not percent:
                    percent = 0.0

                lbl = self.get_list_label('{}: {:02.1f} %'.format(cpu_index, percent))
                self.pnl_cpu.children.append(lbl)
                cpu_index += 1

        # Virtual Memory
        self.pnl_virt_mem.children = [self.get_header_label('Virtual Memory')]
        virt_mem = psutil.virtual_memory()

        if virt_mem:
            self.pnl_virt_mem.children.append(self.get_list_label("Percent Used: {} %".format(virt_mem.percent)))
            self.pnl_virt_mem.children.append(self.get_list_label("Total: {}".format(virt_mem.total)))
            self.pnl_virt_mem.children.append(self.get_list_label("Used: {}".format(virt_mem.used)))
            self.pnl_virt_mem.children.append(self.get_list_label("Free: {}".format(virt_mem.free)))
            self.pnl_virt_mem.children.append(self.get_list_label("Available: {}".format(virt_mem.available)))

        # Swap Memory
        self.pnl_swap_mem.children = [self.get_header_label('Swap Memory')]
        swap_mem = psutil.swap_memory()

        if swap_mem:
            self.pnl_swap_mem.children.append(self.get_list_label("Percent Used: {} %".format(swap_mem.percent)))
            self.pnl_swap_mem.children.append(self.get_list_label("Total: {}".format(swap_mem.total)))
            self.pnl_swap_mem.children.append(self.get_list_label("Used: {}".format(swap_mem.used)))
            self.pnl_swap_mem.children.append(self.get_list_label("Free: {}".format(swap_mem.free)))


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


