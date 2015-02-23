# coding=utf-8

"""
This file contains definitions for a custom dashboard widget for weather conditions and forecasts
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_rectangle
from PiMFD.UI.Text import TextBlock
from PiMFD.UI.Widgets.Charts import BoxChart
from PiMFD.UI.Widgets.DashboardWidget import DashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class WeatherForecastDashboardWidget(DashboardWidget):
    """
    A dashboard widget containing weather condition information
    :type display: PiMFD.UI.DisplayManager.DisplayManager
    :type page: PiMFD.Applications.Core.DashboardPages.DashboardPage
    :type title: str The name of the widget
    :type value: str The value used in the widget
    """

    def __init__(self, display, page, title, weather=None, forecast=None, is_today=False):
        super(WeatherForecastDashboardWidget, self).__init__(display, page, DashboardStatus.Inactive)

        self.title = title
        self.forecast = forecast
        self.weather = weather
        self.is_today = is_today

        self.panel = StackPanel(display, page)

        self.lbl_title = TextBlock(display, page, title, is_highlighted=True)
        self.lbl_title.font = display.fonts.list
        self.panel.children.append(self.lbl_title)

        self.lbl_value = TextBlock(display, page, "Offline")
        self.lbl_value.font = display.fonts.list
        self.panel.children.append(self.lbl_value)

        self.chart = BoxChart(display, page)
        self.chart.width = 200
        self.chart.range_low = -20
        self.chart.range_high = 120
        self.chart.is_highlighted = False
        self.chart.box_width = 0
        self.chart.ticks = (0, 32, 100)
        self.panel.children.append(self.chart)

    def render(self):

        # Colorize as needed
        color = self.get_color()
        self.lbl_value.color = color
        self.lbl_title.color = self.get_title_color()
        self.chart.color = color

        # Render an outline around the entire control
        rect = Rect(self.pos[0], self.pos[1], self.panel.desired_size[0] + (self.padding * 2),
                    self.panel.desired_size[1] + (self.padding * 2))

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

    def arrange(self):

        self.status = self.get_status()
        self.lbl_title.text = self.title
        if self.forecast and self.weather:
            if self.is_today:
                self.lbl_value.text = u'{}{} {}'.format(self.weather.temperature, self.weather.temp_units,
                                                        self.forecast.conditions)
            else:
                self.lbl_value.text = u'{} {}'.format(self.forecast.temp_range, self.forecast.conditions)
        else:
            self.lbl_value.text = 'Offline'

        if self.forecast:
            self.chart.value_low = self.forecast.low
            self.chart.value_high = self.forecast.high

            if self.is_today:
                self.chart.value_current = float(self.weather.temperature)
                self.chart.box_width = -1

        self.panel.arrange()
        self.desired_size = self.panel.desired_size[0] + (self.padding * 2), self.panel.desired_size[1] + (self.padding * 2)
        return self.desired_size

    def get_status(self):

        if not self.weather or not self.forecast:
            return DashboardStatus.Inactive
           
        # Certain Temperatures should function as alerts
        low = self.forecast.low
        high = self.forecast.high

        # If it's today, we don't care about forecast - go off of current temperature
        if self.is_today:
            low = high = float(self.weather.temperature)
        
        if low <= 10 or high >= 100:
            return DashboardStatus.Critical
        elif low <= 32 or high >= 90:
            return DashboardStatus.Caution
        else:
            return DashboardStatus.Passive
