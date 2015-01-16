# coding=utf-8
"""
Holds system pages for use in the system application.
"""
from time import strftime, gmtime
import platform

from PiMFD.Applications.MFDPage import MFDPage


__author__ = 'Matt Eland'


class SysRootPage(MFDPage):
    """
    The root level page for the system app
    """

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: the button text for the application
        """
        return "SYS"  # Though this shouldn't get invoked since it's not going to be available

    def render(self, display):
        """
        Renders the page.
        :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager that manages the page we're rendering.
        """
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
        y += display.get_spacer_line_height()

        # System Data - TODO: These can be long and will need truncated or wrapping in some cases
        y += display.render_text(font, "System Information", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, 'System: ' + platform.platform() + ' ' + platform.release() + ' ' + platform.machine(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, '  Proc: ' + platform.processor(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, 'Net ID: ' + platform.node(), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, '  Disp: ' + str(self.display.res_x) + 'x' + str(self.display.res_y), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, 'Python: ' + platform.python_version() + ' ' + platform.python_implementation() + ' ' + platform.python_compiler(), x, y, cs.foreground).height + display.padding_y


class SysExitPage(MFDPage):
    """
    The exit Pi_MFD confirm page. Allows users to double select to quit the app.
    """

    def get_button_text(self):
        """
        Gets the button text
        :return: The button text.
        """
        return "EXIT"

    def render(self, display):
        """
        Renders the exit page.
        :param display: The DisplayManager used to manage the display.
        """
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
        """
        Handles the reselected event of the page.
        """
        self.controller.requested_exit = True


class SysClockPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """
    
    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "TIME"

    def render(self, display):
        """
        Renders the system clock page.
        :param display: The DisplayManager.
        """
        super(SysClockPage, self).render(display)

        x = display.get_content_start_x()
        y = display.get_content_start_y()

        font = display.font_normal
        cs = display.color_scheme

        y += display.render_text(font, "Current Time", x, y, cs.highlight).height + display.padding_y
        y += display.render_text(font, strftime("SYS: " + self.controller.time_format), x, y, cs.foreground).height + display.padding_y
        y += display.render_text(font, strftime("GMT: " + self.controller.time_format, gmtime()), x, y, cs.foreground).height + display.padding_y


