from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt Eland'


class WeatherPage(MFDPage):

    def get_button_text(self):
        return "WTHR"

    def render(self, display):
        super(WeatherPage, self).render(display)

        start_x = display.get_content_start_x()
        start_y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        weather = self.application.weather_data

        # Current Conditions
        x = start_x
        y = start_y
        y += display.render_text(font, weather.city + " Weather", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, "      Temp: " + weather.temperature + ' (Chill: ' + weather.windchill + ')', x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "Conditions: " + weather.conditions, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "      Wind: " + weather.wind_speed + ' ' + weather.wind_cardinal_direction, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "  Humidity: " + weather.humidity, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "Visibility: " + weather.visibility, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "  Pressure: " + weather.pressure, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "  Daylight: " + weather.sunrise + ' - ' + weather.sunset, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "       GPS: " + weather.lat + ', ' + weather.long, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "   Updated: " + weather.last_result, x, y, cs.foreground).height + display.padding_y

        # Forecast - TODO: Grab forecasts
        x = display.res_x - display.padding_x - 250
        y = start_y
        y += display.render_text(font, "Forecast", x, y, cs.highlight).height + display.padding_y
        for forecast in weather.forecasts:
            y += display.render_text(font, forecast.day + ': ' + forecast.temp_range, x, y, cs.foreground).height + display.padding_y
            # TODO: Show this if we know we have enough horizontal or vertical space for it
            #y += display.render_text(font, forecast.conditions, x, y, cs.foreground).height + display.padding_y

