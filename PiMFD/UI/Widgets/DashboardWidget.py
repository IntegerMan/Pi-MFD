# coding=utf-8

"""
This file contains dashboard widgets
"""
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Text import TextBlock
from PiMFD.UI.WidgetBase import UIWidget

__author__ = 'Matt Eland'


class TextDashboardWidget(UIWidget):
    def __init__(self, display, page, title, value):
        super(TextDashboardWidget, self).__init__(display, page)

        self.title = title
        self.value = value

        self.panel = StackPanel(display, page)

        self.lbl_title = TextBlock(display, page, title, is_highlighted=True)
        self.lbl_title.font = display.fonts.list
        self.panel.children.append(self.lbl_title)

        self.lbl_value = TextBlock(display, page, value)
        self.lbl_value.font = display.fonts.list
        self.panel.children.append(self.lbl_value)

    def render(self):
        return self.panel.render_at(self.pos)

    def arrange(self):
        self.lbl_title.text = self.title
        self.lbl_value.text = self.value

        self.panel.arrange()
        self.desired_size = self.panel.desired_size
        return self.desired_size