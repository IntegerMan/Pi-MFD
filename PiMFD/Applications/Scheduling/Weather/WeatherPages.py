# coding=utf-8
"""
Holds the weather page
"""
from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Rendering import render_text

__author__ = 'Matt Eland'


class WeatherPage(MFDPage):
    """
    A page containing weather and forecast data.
    """

    def get_button_text(self):
        """
        Gets the text for the application's button
        :return: Text for the application's button
        """
        return "WTHR"

    def render(self, display):
        """
        Renders the weather page
        :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager
        """
        super(WeatherPage, self).render(display)

        start_x = display.get_content_start_x()
        start_y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        weather = self.application.weather_data

        # Current Conditions
        x = start_x
        y = start_y
        # TODO: It'd be nice to devise a system where it's simpler to print text.
        y += render_text(display, font, weather.city + " Weather", x, y, cs.highlight).height + display.padding_y
        y += render_text(display, font, "      Temp: " + weather.temperature + ' (Chill: ' + weather.windchill + ')', x,
                         y, cs.foreground).height + display.padding_y
        y += render_text(display, font, "Conditions: " + weather.conditions, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "      Wind: " + weather.wind_speed + ' ' + weather.wind_cardinal_direction, x,
                         y, cs.foreground).height + display.padding_y
        y += render_text(display, font, "  Humidity: " + weather.humidity, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "Visibility: " + weather.visibility, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "  Pressure: " + weather.pressure, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "  Daylight: " + weather.sunrise + ' - ' + weather.sunset, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "       GPS: " + weather.lat + ', ' + weather.long, x, y,
                         cs.foreground).height + display.padding_y
        y += render_text(display, font, "   Updated: " + weather.last_result, x, y,
                         cs.foreground).height + display.padding_y

        # Forecast - TODO: Grab forecasts
        x = display.res_x - display.padding_x - 250
        y = start_y
        y += render_text(display, font, "Forecast", x, y, cs.highlight).height + display.padding_y
        for forecast in weather.forecasts:
            y += render_text(display, font, forecast.day + ': ' + forecast.temp_range, x, y,
                             cs.foreground).height + display.padding_y
            # TODO: Show this if we know we have enough horizontal or vertical space for it
            # y += render_text(display, font, forecast.conditions, x, y, cs.foreground).height + display.padding_y

