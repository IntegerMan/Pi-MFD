# coding=utf-8

"""
This file contains data provider for weather information
"""
from datetime import datetime

from PiMFD.Applications.Scheduling.Weather.WeatherAPIWrapper import WeatherAPI
from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class WeatherDataProvider(DataProvider):

    weather_data = None
    weather_api = None
    last_request = None
    refresh_interval_minutes = 15
    
    def __init__(self, application, options):
        super(WeatherDataProvider, self).__init__("Weather Data Provider")

        self.application = application
        self.weather_api = WeatherAPI()
        self.options = options
        self.current_conditions_widget = None

    def update(self):

        # Auto-Fetch Weather
        now = datetime.now()
        if not self.last_request or (now - self.last_request).seconds > (60 * self.refresh_interval_minutes):
            self.get_weather()

        super(WeatherDataProvider, self).update()

    def get_weather(self, consumer=None):
        """
        Gets weather data from the weather API (Yahoo Weather) and stores it for the weather page.
        """

        if not consumer:
            consumer = self

        if self.options.location:
            now = datetime.now()
            self.last_request = now
            self.weather_api.get_yahoo_weather_async(self.options.location, consumer)

    def get_weather_for_zip(self, zip, consumer=None, updateError=False):

        try:
            if consumer:
                self.weather_api.get_yahoo_weather_async(zip, consumer)
            else:
                return self.weather_api.get_yahoo_weather(zip)

        except Exception as exception:

            if updateError:
                self.weather_data.last_result = 'Could not get weather: ' + exception.message

            return None

    def weather_received(self, location, weather):
        self.weather_data = weather

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