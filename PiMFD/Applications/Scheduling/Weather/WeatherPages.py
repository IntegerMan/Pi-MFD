# coding=utf-8
"""
Holds the weather page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.Applications.Scheduling.Weather.WeatherData import get_condition_icon
from PiMFD.UI.Charts import BoxChart
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Text import SpacerLine

__author__ = 'Matt Eland'


class WeatherPage(MFDPage):
    """
    A page containing weather and forecast data.
    """

    pnl_today = None
    pnl_forecast = None
    lbl_today_header = None
    lbl_cond = None
    lbl_cond_icon = None
    lbl_wind = None
    lbl_humidity = None
    lbl_visible = None
    lbl_pressure = None
    lbl_daylight = None
    lbl_gps = None
    lbl_updated = None

    # These two are really arrays
    lbl_forecast = None
    lbl_forecast_icon = None
    chart_forecast = None

    weather_provider = None
    weather = None

    max_forecasts = 5

    # noinspection PyCompatibility
    def __init__(self, controller, application, weather_provider):
        super(WeatherPage, self).__init__(controller, application)

        self.weather_provider = weather_provider

        # Build out the Today Panel
        self.pnl_today = StackPanel(controller.display, self)
        self.lbl_today_header = self.get_header_label("{} Weather")
        self.lbl_temp = self.get_label(u"      Temp: {}{} (Chill: {}{})")
        self.lbl_cond = self.get_label(u"Conditions: {}")
        self.lbl_cond_icon = self.get_label(u"{}")
        self.lbl_cond_icon.font = controller.display.fonts.weather
        pnl_cond = StackPanel(controller.display, self, is_horizontal=True)
        pnl_cond.children = (self.lbl_cond, self.lbl_cond_icon)
        self.lbl_wind = self.get_label(u"      Wind: {} {} {}")
        self.lbl_humidity = self.get_label(u"  Humidity: {} %")
        self.lbl_visible = self.get_label(u"Visibility: {} {}")
        self.lbl_pressure = self.get_label(u"  Pressure: {} {}")
        self.lbl_daylight = self.get_label(u"  Daylight: {} - {}")
        self.lbl_gps = self.get_label(u"       GPS: {}, {}")
        self.lbl_updated = self.get_label(u"   Updated: {}")

        self.pnl_today.children = (
            self.lbl_today_header,
            self.lbl_temp,
            pnl_cond,
            self.lbl_wind,
            self.lbl_humidity,
            self.lbl_visible,
            self.lbl_pressure,
            self.lbl_daylight,
            self.lbl_gps
        )

        # Build out the Forecast Panel
        self.pnl_forecast = StackPanel(controller.display, self)
        forecast_header = self.get_header_label("Forecast")
        self.pnl_forecast.children.append(forecast_header)

        # Add placeholders for the individual forecasts
        self.lbl_forecast = dict()
        self.lbl_forecast_icon = dict()
        self.chart_forecast = dict()
        for i in range(0, self.max_forecasts):
            label = self.get_label(u"{}: {}-{}{}")
            self.lbl_forecast[i] = label

            icon = self.get_label(u"{}")
            icon.font = controller.display.fonts.weather
            self.lbl_forecast_icon[i] = icon

            pnl_day = StackPanel(controller.display, self, is_horizontal=True)
            pnl_day.children = (label, icon)

            self.pnl_forecast.children.append(pnl_day)

            chart = BoxChart(controller.display, self)
            chart.width = 225
            chart.range_low = -20
            chart.range_high = 120
            chart.ticks = (0, 32, 100)
            self.chart_forecast[i] = chart
            self.pnl_forecast.children.append(chart)

        self.pnl_forecast.children.append(SpacerLine(controller.display, self))

        # Set up the main content panel
        self.content_panel = StackPanel(controller.display, self, is_horizontal=True, keep_together=True)
        self.content_panel.pad_last_item = True
        self.content_panel.auto_orient = True
        self.content_panel.children = (self.pnl_today, self.pnl_forecast)

        # Set up the master panel
        self.panel.children = (self.content_panel, self.lbl_updated)
        self.panel.pad_last_item = False

    def get_button_text(self):
        """
        Gets the text for the application's button
        :return: Text for the application's button
        """
        return "WTHR"

    def arrange(self):

        weather = self.weather_provider.weather_data

        self.weather = weather

        if weather:
            self.lbl_today_header.text_data = weather.city
            self.lbl_temp.text_data = (weather.temperature, weather.temp_units, weather.windchill, weather.temp_units)
            self.lbl_cond.text_data = weather.conditions
            self.lbl_cond_icon.text_data = get_condition_icon(weather.code)
            self.lbl_wind.text_data = (weather.wind_speed, weather.wind_units, weather.wind_cardinal_direction)
            self.lbl_humidity.text_data = weather.humidity
            self.lbl_visible.text_data = (weather.visibility, weather.visibility_units)
            self.lbl_pressure.text_data = (weather.pressure, weather.pressure_units)
            self.lbl_daylight.text_data = (weather.sunrise, weather.sunset)
            self.lbl_gps.text_data = (weather.lat, weather.long)
            self.lbl_updated.text_data = weather.last_result

            # Update Forecasts
            i = 0
            for forecast in weather.forecasts:
                label = self.lbl_forecast[i]
                icon = self.lbl_forecast_icon[i]
                chart = self.chart_forecast[i]

                label.text_data = (forecast.day, forecast.low, forecast.high, weather.temp_units)
                icon.text_data = get_condition_icon(forecast.code)
                chart.value_low = forecast.low
                chart.value_high = forecast.high

                i += 1

        return super(WeatherPage, self).arrange()

    def render(self):
        """
        Renders the weather page
        """

        if not self.weather:
            self.center_text("NO WEATHER DATA")
        else:
            super(WeatherPage, self).render()