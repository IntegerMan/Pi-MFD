# coding=utf-8

"""
This file contains a data page provider for map information
"""
from PiMFD.Applications.ANI.DataCategoriesPage import DataPage
from PiMFD.Applications.ANI.DataPageProvider import DataPageProvider
from PiMFD.UI.Button import MFDButton
from PiMFD.UI.Widgets.MenuItem import TextMenuItem

__author__ = 'Matt Eland'


class MapDataPageProvider(DataPageProvider):
    def __init__(self, name, data_source):
        super(MapDataPageProvider, self).__init__(name)

        self.data_source = data_source

    def get_data_details_page(self, controller, application, back_page=None):
        return MapNodesDataPage(controller, application, self, back_page=back_page)


class MapNodesDataPage(DataPage):
    def __init__(self, controller, application, data_page_provider, back_page=None, auto_scroll=True):
        super(MapNodesDataPage, self).__init__(controller, application, data_page_provider, auto_scroll)

        self.back_page = back_page
        self.btn_back = MFDButton("BACK")

    def get_button_text(self):
        return "DATA"

    def get_lower_buttons(self):

        if self.back_page:
            return [self.btn_back]

        return super(MapNodesDataPage, self).get_lower_buttons()

    def handle_lower_button(self, index):

        if index == 0 and self.back_page:
            self.application.select_page(self.back_page)
            return

        return super(MapNodesDataPage, self).handle_lower_button(index)


    def refresh_children(self):

        self.pnl_data.children = []

        for node_key in self.data_page_provider.data_source:
            node = self.data_page_provider.data_source[node_key]

            title = node.get_menu_name()
            menu_item = TextMenuItem(self.display, self, title)
            menu_item.font = self.controller.display.fonts.list
            menu_item.data_context = node
            self.pnl_data.children.append(menu_item)

        if len(self.pnl_data.children) > 0:
            self.set_focus(self.pnl_data.children[0])

    def handle_control_state_changed(self, widget):

        if widget:
            incident = widget.data_context
            if incident:
                self.application.show_map(incident.lat, incident.lng)
                return

        super(MapNodesDataPage, self).handle_control_state_changed(widget)
