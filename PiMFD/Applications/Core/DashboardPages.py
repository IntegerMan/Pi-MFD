# coding=utf-8

"""
This file contains dashboard pages
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel

__author__ = 'Matt Eland'


class DashboardPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """

    def __init__(self, controller, application, time_data_provider):
        super(DashboardPage, self).__init__(controller, application)

        header = self.get_header_label("Pi-MFD System Dashboard")

        self.pnl_alerts = StackPanel(controller.display, self)

        self.time_data_provider = time_data_provider

        self.panel.children = [header, self.pnl_alerts]

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "HOME"

    def arrange(self):

        # Get the widgets from the data provider
        self.pnl_alerts.children = []
        if self.controller.data_providers:
            for provider in self.controller.data_providers:
                widgets = provider.get_dashboard_widgets(self.display, self)
                if widgets:
                    for widget in widgets:
                        if widget:
                            self.pnl_alerts.children.append(widget)

        return super(DashboardPage, self).arrange()