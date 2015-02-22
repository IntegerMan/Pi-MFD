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


class DashboardStatus(object):
    
    Inactive = -1
    Passive = 0
    Notification = 1
    Caution = 2
    Critical = 3

class TextDashboardWidget(UIWidget):
    """
    A simple labeled dashboard widget
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.Core.DashboardPages.DashboardPage
    :type title: str The name of the widget
    :type value: str The value used in the widget
    """
    
    def __init__(self, display, page, title, value, status=DashboardStatus.Passive):
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
        
        self.status = status
        
    def get_title_color(self):

        if self.status in [DashboardStatus.Passive, DashboardStatus.Notification]:
            return self.display.color_scheme.highlight
        elif self.status == DashboardStatus.Inactive:
            return self.display.color_scheme.disabled
        elif self.status == DashboardStatus.Caution:
            return self.display.color_scheme.caution
        elif self.status == DashboardStatus.Critical:
            return self.display.color_scheme.critical

        return self.display.color_scheme.highlight       
        
    def get_color(self):
        
        if self.status in [DashboardStatus.Passive, DashboardStatus.Notification]:
            return self.display.color_scheme.foreground
        elif self.status == DashboardStatus.Inactive:
            return self.display.color_scheme.disabled
        elif self.status == DashboardStatus.Caution:
            return self.display.color_scheme.caution
        elif self.status == DashboardStatus.Critical:
            return self.display.color_scheme.critical

        return self.display.color_scheme.foreground

    def render(self):

        # Colorize as needed
        color = self.get_color()        
        self.lbl_value.color = color
        self.lbl_title.color = self.get_title_color()

        # Render an outline around the entire control
        padding = 8
        rect = Rect(self.pos[0], self.pos[1], self.panel.desired_size[0] + (padding * 2), self.panel.desired_size[1] + (padding * 2))
        
        # Some statuses need custom backgrounds
        if self.status == DashboardStatus.Caution:
            render_rectangle(self.display, self.display.color_scheme.caution_bg, rect, width=0)
        elif self.status == DashboardStatus.Critical:
            render_rectangle(self.display, self.display.color_scheme.critical_bg, rect, width=0)
            
        # Render the outline
        render_rectangle(self.display, color, rect)

        # Render the base content with some padding
        pos = self.pos[0] + padding, self.pos[1] + padding
        self.panel.render_at(pos)

        # Assume the width of the outer outline
        return self.set_dimensions_from_rect(rect) 

    def arrange(self):
        self.lbl_title.text = self.title
        self.lbl_value.text = self.value

        self.panel.arrange()
        self.desired_size = self.panel.desired_size
        return self.desired_size