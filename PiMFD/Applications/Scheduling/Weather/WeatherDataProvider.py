# coding=utf-8

"""
This file contains data provider for weather information
"""
from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget

__author__ = 'Matt Eland'

class WeatherDataProvider(DataProvider):

    weather_data = None

    def __init__(self, application):
        super(WeatherDataProvider, self).__init__("Weather Data Provider")

        self.application = application

        self.current_conditions_widget = None

    def update(self):
        super(WeatherDataProvider, self).update()

    def get_dashboard_widgets(self, display, page):

        if self.weather_data:
            weather_text = u"{}{} {}".format(self.weather_data.temperature, self.weather_data.temp_units, self.weather_data.conditions)
        else:
            weather_text = "Loading..."

        if not self.current_conditions_widget:
            # Build out the widget
            self.current_conditions_widget = TextDashboardWidget(display, page, "Current Weather", weather_text)
        else:
            # Update with current system time
            self.current_conditions_widget.value = weather_text

        return [self.current_conditions_widget]