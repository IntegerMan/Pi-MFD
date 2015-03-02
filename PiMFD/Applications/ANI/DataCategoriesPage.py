# coding=utf-8

"""
This file contains a definition for the data categories page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.Applications.PlaceholderPage import SimpleMessagePage
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Widgets.MenuItem import TextMenuItem

__author__ = 'Matt Eland'


class DataCategoriesPage(MFDPage):
    """
    The data categories page
    """

    def __init__(self, controller, application, auto_scroll=True):
        super(DataCategoriesPage, self).__init__(controller, application, auto_scroll)

        self.lbl_header = self.get_header_label("Data Categories")

        self.pnl_items = StackPanel(self.display, self)

        self.mnu_traffic = TextMenuItem(self.display, self, "Traffic Incidents")
        self.mnu_traffic.font = self.controller.display.fonts.list
        self.pnl_items.children.append(self.mnu_traffic)

        self.panel.children = [self.lbl_header, self.pnl_items]

        self.set_focus(self.mnu_traffic)

    def get_button_text(self):
        return "DATA"

    def handle_control_state_changed(self, widget):
        if widget is self.mnu_traffic:
            self.application.select_page(SimpleMessagePage(self.controller, self.application, "TRFC"))
            return

        super(DataCategoriesPage, self).handle_control_state_changed(widget)