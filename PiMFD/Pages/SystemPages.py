from time import strftime, gmtime
from PiMFD.Pages.MFDPage import MFDPage
import platform

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

        # App Version
        y += display.render_text(font, self.controller.app_name + " Information", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, "   Ver: " + self.controller.app_version, x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, " Legal: Copyright (c) " + self.controller.app_author + " " + str(self.controller.copyright_year), x, y, cs.foreground).height + display.padding_y

        # Separator Line
        y += (display.padding_y * 2) + display.font_size_normal

        # System Data - TODO: These can be long and will need truncated or wrapping in some cases
        y += display.render_text(font, "System Information", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, 'System: ' + platform.platform() + ' ' + platform.release() + ' ' + platform.machine(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, '  Proc: ' + platform.processor(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, 'Net ID: ' + platform.node(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, 'Python: ' + platform.python_version() + ' ' + platform.python_implementation() + ' ' + platform.python_compiler(), x, y, cs.foreground).height + display.padding_y

class SysExitPage(MFDPage):

    def get_button_text(self):
        return "EXIT"

    def render(self, display):
        super(SysExitPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        if not self.controller.requested_exit:
            rect = display.render_text(font, "Exit Application", x, y, cs.highlight)
            y = rect.bottom + display.padding_y

            display.render_text(font, "Confirm exit by re-selecting '" + self.get_button_text() + "'", x, y, cs.foreground)
        else:
            display.render_text(font, "The application will now close.", x, y, cs.foreground)

    def handle_reselected(self):
        self.controller.requested_exit = True


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

        y += display.render_text(font, "Current Time", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, strftime("SYS: " + time_format), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, strftime("GMT: " + time_format, gmtime()), x, y, cs.foreground).height + display.padding_y


