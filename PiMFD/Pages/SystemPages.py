from time import strftime, gmtime
from PiMFD.Pages.MFDPage import MFDPage

__author__ = 'Matt Eland'


class SysRootPage(MFDPage):

    def get_button_text(self):
        return "SYS"  # Though this shouldn't get invoked since it's not going to be available

    def render(self, display):
        super(SysRootPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        rect = display.render_text(font, "System Information", x, y, cs.highlight)
        y = rect.bottom + display.padding_y

        rect = display.render_text(font, self.controller.app_name + " - " + self.controller.app_version, x, y, cs.foreground)
        y = rect.bottom + display.padding_y

        display.render_text(font, "Copyright (c) " + self.controller.app_author + " " + str(self.controller.copyright_year), x, y, cs.foreground)


class SysClockPage(MFDPage):
    
    def get_button_text(self):
        return "TIME"

    def render(self, display):
        super(SysClockPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        time_format = '%m/%d/%Y - %H:%M:%S'

        font = display.font_normal
        cs = display.color_scheme

        rect = display.render_text(font, "Current Time", x, y, cs.highlight)
        y = rect.bottom + display.padding_y

        rect = display.render_text(font, strftime("SYS: " + time_format), x, y, cs.foreground)
        y = rect.bottom + display.padding_y

        display.render_text(font, strftime("GMT: " + time_format, gmtime()), x, y, cs.foreground)


