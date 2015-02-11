# coding=utf-8
"""
Holds system pages for use in the system application.
"""
from time import strftime, gmtime

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Checkboxes import CheckBox
from PiMFD.UI.SpinnerBox import SpinnerBox
from PiMFD.UI.Text import SpacerLine
from PiMFD.UI.TextBoxes import TextBox


__author__ = 'Matt Eland'


class SysExitPage(MFDPage):
    """
    The exit Pi_MFD confirm page. Allows users to double select to quit the app.
    """

    def __init__(self, controller, application):
        super(SysExitPage, self).__init__(controller, application)

        header = self.get_header_label("Exit Application")
        confirm = self.get_label("Confirm exit by re-selecting '" + self.get_button_text() + "'")

        self.panel.children = [header, confirm]

    def get_button_text(self):
        """
        Gets the button text
        :return: The button text.
        """
        return "EXIT"

    def handle_reselected(self):
        """
        Handles the reselected event of the page.
        """
        self.controller.requested_exit = True


class DashboardPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """

    def __init__(self, controller, application):
        super(DashboardPage, self).__init__(controller, application)

        header = self.get_header_label("Current Time")
        self.lbl_sys_time = self.get_label("SYS: {}")
        self.lbl_gmt_time = self.get_label("GMT: {}")

        header_alerts = self.get_header_label("Alerts")
        self.lbl_alerts = self.get_label("No Alerts")

        self.panel.children = [header,
                               self.lbl_sys_time,
                               self.lbl_gmt_time,
                               SpacerLine(self.display, self),
                               header_alerts,
                               self.lbl_alerts]

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "ALRT"

    def arrange(self):

        # Grab the time and stick it in the labels
        self.lbl_sys_time.text_data = strftime(self.controller.time_format)
        self.lbl_gmt_time.text_data = strftime(self.controller.time_format, gmtime())

        return super(DashboardPage, self).arrange()


class SettingsPage(MFDPage):
    """
    A page for viewing and managing user settings
    """

    chk_scanline = None
    ddl_color_scheme = None
    txt_zipcode = None

    def __init__(self, controller, application):
        """
        :type application: PiMFD.Applications.MFDApplication
        :type controller: PiMFD.Controller.MFDController
        """
        super(SettingsPage, self).__init__(controller, application)

        # Build basic controls
        header = self.get_header_label("Settings")
        self.chk_full_screen = CheckBox(controller.display, self, "Fullscreen:")  # Not currently working so don't add it
        self.chk_scanline = CheckBox(controller.display, self, "Scanline:")
        self.chk_interlace = CheckBox(controller.display, self, "Interlace:")
        self.chk_fps = CheckBox(controller.display, self, "FPS:")
        self.txt_zipcode = TextBox(controller.display, self, label="Zip Code:")
        self.txt_zipcode.allow_alpha = False
        self.txt_zipcode.max_length = 5
        self.ddl_color_scheme = SpinnerBox(controller.display, self, 'Color Scheme:',
                                           controller.display.color_scheme,
                                           controller.display.color_schemes)

        # Add Controls to the page's panel
        self.panel.children = [header,
                               self.chk_scanline,
                               self.chk_interlace,
                               self.chk_fps,
                               self.txt_zipcode,
                               self.ddl_color_scheme]

        # We DO care about input on this page. Set up our input.
        self.set_focus(self.chk_scanline)

    def handle_selected(self):
        super(SettingsPage, self).handle_selected()
        self.txt_zipcode.text = self.controller.options.location

    def arrange(self):

        opts = self.controller.options
        display = self.display

        # Update properties on controls
        self.ddl_color_scheme.value = display.color_scheme
        self.chk_scanline.checked = opts.enable_scan_line
        self.chk_interlace.checked = opts.enable_interlacing
        self.chk_fps.checked = opts.enable_fps
        self.chk_full_screen.checked = display.is_fullscreen

        return super(SettingsPage, self).arrange()

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "OPTS"

    def handle_control_state_changed(self, widget):
        """
        Responds to control state changes
        :type widget: UIWidget
        """
        super(SettingsPage, self).handle_control_state_changed(widget)

        opts = self.controller.options

        if widget is self.chk_scanline:
            opts.enable_scan_line = widget.checked
        elif widget is self.chk_full_screen:
            self.display.set_fullscreen(widget.checked)
        elif widget is self.chk_fps:
            opts.enable_fps = widget.checked
        elif widget is self.chk_interlace:
            opts.enable_interlacing = widget.checked
        elif widget is self.txt_zipcode and len(widget.text) >= 5:  # Ensure zip code is valid
            opts.location = widget.text
        elif widget is self.ddl_color_scheme:
            opts.color_scheme = str(widget.value)
            self.display.color_scheme = widget.value

        # Persist to disk
        opts.save_to_settings()

