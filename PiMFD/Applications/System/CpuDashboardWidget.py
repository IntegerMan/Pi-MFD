# coding=utf-8

"""
This file contains a dashboard widget for CPU usage
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_rectangle
from PiMFD.UI.Text import TextBlock
from PiMFD.UI.Widgets.Charts import BarChart
from PiMFD.UI.Widgets.DashboardWidget import DashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class CpuDashboardWidget(DashboardWidget):
    charts = None

    def __init__(self, display, page, title="CPU", values=None, status=DashboardStatus.Passive):
        super(CpuDashboardWidget, self).__init__(display, page, status)

        self.title = title
        self.values = values

        self.panel = StackPanel(display, page)

        self.lbl_title = TextBlock(display, page, title, is_highlighted=True)
        self.lbl_title.font = display.fonts.list
        self.panel.children.append(self.lbl_title)

        self.pnl_charts = StackPanel(display, page, is_horizontal=True)
        self.pnl_charts.padding = 2, 0
        self.panel.children.append(self.pnl_charts)

    def arrange(self):

        if not self.charts and self.values and len(self.values) > 0:
            self.charts = []

            chart_width = (150 - (len(self.values) * 2)) / len(self.values)

            for value in self.values:
                chart = BarChart(self.display, self.page, value=value)
                chart.width = chart_width
                chart.height = 12
                self.charts.append(chart)
                self.pnl_charts.children.append(chart)

        elif self.charts and self.values and len(self.values) > 0:

            for chart, value in zip(self.charts, self.values):
                chart.value = value

        self.lbl_title.text = self.title

        self.panel.arrange()
        self.desired_size = 150 + (self.padding * 2), self.panel.desired_size[1] + (self.padding * 2)
        return self.desired_size

    def render(self):

        # Colorize as needed
        color = self.get_color()
        self.lbl_title.color = self.get_title_color()

        # Render an outline around the entire control
        rect = Rect(self.pos[0], self.pos[1], self.desired_size[0], self.desired_size[1])

        # Some statuses need custom backgrounds
        if self.status == DashboardStatus.Caution:
            render_rectangle(self.display, self.display.color_scheme.caution_bg, rect, width=0)
        elif self.status == DashboardStatus.Critical:
            render_rectangle(self.display, self.display.color_scheme.critical_bg, rect, width=0)

        # Render the outline
        render_rectangle(self.display, color, rect)

        # Render the base content with some padding
        pos = self.pos[0] + self.padding, self.pos[1] + self.padding
        self.panel.render_at(pos)

        # Assume the width of the outer outline
        return self.set_dimensions_from_rect(rect)