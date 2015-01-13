from PiMFD.Pages.MFDPage import MFDPage

__author__ = 'Matt Eland'


class WeatherPage(MFDPage):

    def get_button_text(self):
        return "WTHR"

    def render(self, display):
        super(WeatherPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        # Current Conditions - TODO: Grab current data
        y += display.render_text(font, "Current Weather", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, "Temperature Unavailable", x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, "Conditions Unavailable", x, y, cs.foreground).height + display.padding_y

        # Separator Line
        y += display.get_spacer_line_height()

        # Forecast - TODO: Grab forecasts
        y += display.render_text(font, "Forecast", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, 'Forecast Unavailable', x, y, cs.foreground).height + display.padding_y


