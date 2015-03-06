# coding=utf-8

"""
This file contains a definition for the data categories page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Widgets.MenuItem import TextMenuItem

__author__ = 'Matt Eland'


class DataPage(MFDPage):
    def __init__(self, controller, application, data_page_provider, auto_scroll=True):
        super(DataPage, self).__init__(controller, application, auto_scroll)

        self.data_page_provider = data_page_provider
        self.lbl_header = self.get_header_label(data_page_provider.name)
        self.pnl_data = StackPanel(controller.display, self)

        self.refresh_children()

        self.panel.children = [self.lbl_header, self.pnl_data]

    def handle_selected(self):
        self.refresh_children()

        super(DataPage, self).handle_selected()

    def refresh_children(self):
        pass

    def arrange(self):
        return super(DataPage, self).arrange()

    def render(self):
        return super(DataPage, self).render()
    
    def focus_first_child(self):
        if len(self.pnl_data.children) > 0:
            self.set_focus(self.pnl_data.children[0])



class DataCategoriesPage(MFDPage):
    """
    The data categories page
    """

    def __init__(self, controller, application, auto_scroll=True):
        super(DataCategoriesPage, self).__init__(controller, application, auto_scroll)

        self.lbl_header = self.get_header_label("Data Categories")

        self.pnl_items = StackPanel(self.display, self)

        self.panel.children = [self.lbl_header, self.pnl_items]
        
    def refresh_list(self):

        self.pnl_items.children = []

        for provider in self.controller.data_providers:
            
            for page in provider.get_data_pages():
                menu_item = TextMenuItem(self.display, self, page.name)
                menu_item.font = self.controller.display.fonts.list
                menu_item.data_context = page
                self.pnl_items.children.append(menu_item)


    def handle_selected(self):
        
        self.refresh_list()
        
        if len(self.pnl_items.children) > 0:            
            self.set_focus(self.pnl_items.children[0])
            
        super(DataCategoriesPage, self).handle_selected()

    def get_button_text(self):
        return "DATA"

    def handle_control_state_changed(self, widget):
        
        if widget:
            data_provider = widget.data_context
        
            if data_provider:
                page = data_provider.get_data_details_page(self.controller, self.application, back_page=self)
                
                if page:
                    self.application.select_page(page)
                    return
                    
        super(DataCategoriesPage, self).handle_control_state_changed(widget)