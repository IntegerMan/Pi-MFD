# coding=utf-8

"""
This file contains data provider for weather information
"""
from datetime import datetime

from PiMFD.Applications.Scheduling.Weather.WeatherAPIWrapper import WeatherAPI
from PiMFD.Applications.Scheduling.Weather.WeatherDashboardWidget import WeatherForecastDashboardWidget
from PiMFD.DataProvider import DataProvider


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
        self.tomorrow_conditions_widget = None
        self.today_forecast_widget = None

    def update(self, now):

        # Auto-Fetch Weather
        if not self.last_request or (now - self.last_request).seconds > (60 * self.refresh_interval_minutes):
            self.get_weather()

        super(WeatherDataProvider, self).update(now)

    def get_weather(self, consumer=None):
        """
        Gets weather data from the weather API (Yahoo Weather) and stores it for the weather page.
        """

        if not consumer:
            consumer = self

        if self.options.location:
            now = datetime.now()
            self.last_request = now
            self.weather_api.get_weather_async(self.options.location, consumer)

    def get_weather_for_zip(self, zip, consumer=None, updateError=False):

        try:
            if consumer:
                self.weather_api.get_weather_async(zip, consumer)
            else:
                return self.weather_api.get_yahoo_weather(zip)

        except Exception as exception:

            if updateError:
                self.weather_data.last_result = 'Could not get weather: ' + exception.message

            return None

    def weather_received(self, location, weather):
        self.weather_data = weather

    def build_weather(self, display, page, widget, label, forecast_index, is_forecast):
        # Update the current weather widget
        if not widget:
            widget = WeatherForecastDashboardWidget(display,
                                                    page,
                                                    label,
                                                    self.weather_data,
                                                    is_forecast=is_forecast)
        else:
            widget.weather = self.weather_data
        if self.weather_data and self.weather_data.forecasts and len(self.weather_data.forecasts) > forecast_index:
            widget.forecast = self.weather_data.forecasts[forecast_index]
        else:
            widget.forecast = None

        return widget

    def get_dashboard_widgets(self, display, page):

        if self.weather_data:
            if not self.current_conditions_widget:
                self.current_conditions_widget = self.build_weather(display, page, self.current_conditions_widget,
                                                                    "Weather", 0, False)
            else:
                self.current_conditions_widget.weather = self.weather_data

            if not self.today_forecast_widget:
                self.today_forecast_widget = self.build_weather(display, page, self.today_forecast_widget, "Today", 0,
                                                                True)
            else:
                self.current_conditions_widget.forecast = self.weather_data.forecasts[0]

            if not self.tomorrow_conditions_widget:
                self.tomorrow_conditions_widget = self.build_weather(display, page, self.tomorrow_conditions_widget,
                                                                     "Tomorrow", 1, True)
            else:
                self.tomorrow_conditions_widget.forecast = self.weather_data.forecasts[1]

            self.tomorrow_conditions_widget.minutes_to_clean_frost = self.weather_data.forecasts[
                1].minutes_to_clean_frost

        return [self.current_conditions_widget, self.today_forecast_widget, self.tomorrow_conditions_widget]