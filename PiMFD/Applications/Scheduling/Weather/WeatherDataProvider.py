# coding=utf-8

"""
This file contains data provider for weather information
"""
from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, DashboardStatus

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

        weather_status = DashboardStatus.Passive

        if self.weather_data:
            weather_text = u"{}{} {}".format(self.weather_data.temperature, self.weather_data.temp_units, self.weather_data.conditions)
            
            # Certain Temperatures should function as alerts
            numeric_temp = float(self.weather_data.temperature)
            if numeric_temp <= 10 or numeric_temp >= 100:
                weather_status = DashboardStatus.Critical
            elif numeric_temp <= 32 or numeric_temp >= 90:
                weather_status = DashboardStatus.Caution
                
        else:
            # We may be loading
            weather_text = "Offline"
            weather_status = DashboardStatus.Inactive

        if not self.current_conditions_widget:
            # Build out the widget
            self.current_conditions_widget = TextDashboardWidget(display, page, "Current Weather", weather_text)
        else:
            # Update with current system time
            self.current_conditions_widget.value = weather_text
            
        self.current_conditions_widget.status = weather_status

        return [self.current_conditions_widget]