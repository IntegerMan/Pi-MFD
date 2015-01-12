from time import strftime, gmtime
from PiMFD.Pages.MFDPage import MFDPage

__author__ = 'Matt Eland'


class SysClockPage(MFDPage):
    
    def get_button_text(self):
        return "TIME"

    def render(self, display):
        super(SysClockPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        time_format = '%m/%d/%Y - %H:%M:%S'

        # TODO: It should be simpler to render 3 lines of text
        rect = display.render_text(display.font_normal,
                                   "Current Time",
                                   x,
                                   y,
                                   self.display.color_scheme.highlight)

        y = rect.bottom + display.padding_y

        rect = display.render_text(display.font_normal,
                                   strftime("SYS: " + time_format),
                                   x,
                                   y,
                                   self.display.color_scheme.foreground)

        y = rect.bottom + display.padding_y

        display.render_text(display.font_normal,
                            strftime("GMT: " + time_format, gmtime()),
                            x,
                            y,
                            display.color_scheme.foreground)


