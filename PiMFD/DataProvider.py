# coding=utf-8

"""
This file contains base definitions for data providers
"""
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Text import TextBlock

__author__ = 'Matt Eland'


class DataProvider(object):
    def __init__(self, name):
        super(DataProvider, self).__init__()

        self.name = name

    def update(self):
        pass

    def get_dashboard_widgets(self, display, page):
        return None

    def build_widget(self, display, page, title, value):

        panel = StackPanel(display, page)

        if title:
            lbl_title = TextBlock(display, page, title, is_highlighted=True)
            lbl_title.font = display.fonts.list
            panel.children.append(lbl_title)

        if value:
            lbl_value = TextBlock(display, page, value)
            lbl_value.font = display.fonts.list
            panel.children.append(lbl_value)

        return panel