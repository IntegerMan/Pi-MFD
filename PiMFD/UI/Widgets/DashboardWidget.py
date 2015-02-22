# coding=utf-8

"""
This file contains dashboard widgets
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_rectangle
from PiMFD.UI.Text import TextBlock
from PiMFD.UI.WidgetBase import UIWidget


__author__ = 'Matt Eland'


class TextDashboardWidget(UIWidget):
    """
    A simple labeled dashboard widget
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.Core.DashboardPages.DashboardPage
    :type title: str The name of the widget
    :type value: str The value used in the widget
    """

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
        # Render the base content with some padding
        padding = 8
        pos = self.pos[0] + padding, self.pos[1] + padding
        content_rect = self.panel.render_at(pos)

        # Render an outline around the entire control
        rect = Rect(self.pos[0], self.pos[1], content_rect.width + (padding * 2), content_rect.height + (padding * 2))
        color = self.display.color_scheme.foreground
        render_rectangle(self.display, color, rect)

        # Assume the width of the outer outline
        return self.set_dimensions_from_rect(rect) 

    def arrange(self):
        self.lbl_title.text = self.title
        self.lbl_value.text = self.value

        self.panel.arrange()
        self.desired_size = self.panel.desired_size
        return self.desired_size