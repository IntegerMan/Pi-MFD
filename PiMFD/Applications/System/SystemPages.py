# coding=utf-8
"""
Holds system pages for use in the system application.
"""
from time import strftime, gmtime
import platform

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Checkboxes import CheckBox
from PiMFD.UI.SpinnerBox import SpinnerBox
from PiMFD.UI.TextBoxes import TextBox
from PiMFD.UI.Text import SpacerLine


__author__ = 'Matt Eland'


class SysRootPage(MFDPage):
    """
    The root level page for the system app
    """

    def __init__(self, controller, application):
        super(SysRootPage, self).__init__(controller, application)

        self.lbl_app_header = self.get_header_label("{} Information")
        self.lbl_app_version = self.get_label("   Ver: {}")
        self.lbl_app_legal = self.get_label(" Legal: Copyright (c) {} {}")
        lbl_sys_header = self.get_header_label("System Information")
        self.lbl_sys_name = self.get_label("System: {} {} {}")
        self.lbl_sys_processor = self.get_label("  Proc: {}")
        self.lbl_sys_net_id = self.get_label("Net ID: {}")
        self.lbl_sys_display = self.get_label("  Disp: {}x{}")
        self.lbl_sys_python = self.get_label("Python: {} {} {}")

        self.panel.children = (
            self.lbl_app_header,
            self.lbl_app_version,
            self.lbl_app_legal,
            SpacerLine(self.display, self),
            lbl_sys_header,
            self.lbl_sys_name,
            self.lbl_sys_processor,
            self.lbl_sys_net_id,
            self.lbl_sys_display,
            self.lbl_sys_python
        )

    def get_button_text(self):
        """
        Gets the button text for the application
        :return: the button text for the application
        """
        return "SYS"  # Though this shouldn't get invoked since it's not going to be available

    def render(self):
        """
        Renders the page.
        """

        opts = self.controller.options

        self.lbl_app_header.text_data = opts.app_name
        self.lbl_app_version.text_data = opts.app_version
        self.lbl_app_legal.text_data = opts.app_author, opts.copyright_year
        self.lbl_sys_name.text_data = platform.platform(), platform.release(), platform.machine()
        self.lbl_sys_processor.text_data = platform.processor()
        self.lbl_sys_net_id.text_data = platform.node()
        self.lbl_sys_display.text_data = self.display.res_x, self.display.res_y
        self.lbl_sys_python.text_data = platform.python_version(), platform.python_implementation(), platform.python_compiler()

        return super(SysRootPage, self).render()

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


class SysClockPage(MFDPage):
    """
    A system clock page displaying the time in GMT and the current time zone.
    """

    def __init__(self, controller, application):
        super(SysClockPage, self).__init__(controller, application)

        header = self.get_header_label("Current Time")
        self.lbl_sys_time = self.get_label("SYS: {}")
        self.lbl_gmt_time = self.get_label("GMT: {}")
        self.panel.children = [header, self.lbl_sys_time, self.lbl_gmt_time]

    def get_button_text(self):
        """
        Gets the button text.
        :return: The button text.
        """
        return "TIME"

    def render(self):
        """
        Renders the system clock page.
        """

        # Grab the time and stick it in the labels
        self.lbl_sys_time.text_data = strftime(self.controller.time_format)
        self.lbl_gmt_time.text_data = strftime(self.controller.time_format, gmtime())

        return super(SysClockPage, self).render()


class SettingsPage(MFDPage):
    """
    A page for viewing and managing user settings
    """

    chk_scanline = None
    ddl_color_scheme = None
    txt_zipcode = None

    def __init__(self, controller, application):
        """
        :type application: PiMFD.Applications.System.SystemApplication.SysApplication
        :type controller: PiMFD.Controller.MFDController
        """
        super(SettingsPage, self).__init__(controller, application)

        # Build basic controls
        header = self.get_header_label("Settings")
        self.chk_scanline = CheckBox(controller.display, self, "Scanline:")
        self.chk_interlace = CheckBox(controller.display, self, "Interlace:")
        self.chk_fps = CheckBox(controller.display, self, "FPS:")
        self.txt_zipcode = TextBox(controller.display, self, label="Zip Code:")
        self.txt_zipcode.allow_alpha = False
        self.txt_zipcode.max_length = 5
        self.ddl_color_scheme = SpinnerBox(controller.display, self, 'Color Scheme:',
                                           controller.display.color_scheme.name)

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

    def render(self):
        """
        Renders the page.
        """
        opts = self.controller.options
        display = self.display

        # Update properties on controls
        self.ddl_color_scheme.value = display.color_scheme.name
        self.chk_scanline.checked = opts.enable_scan_line
        self.chk_interlace.checked = opts.enable_interlacing
        self.chk_fps.checked = opts.enable_fps

        # Render all controls
        return super(SettingsPage, self).render()

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
        elif widget is self.chk_fps:
            opts.enable_fps = widget.checked
        elif widget is self.chk_interlace:
            opts.enable_interlacing = widget.checked
        elif widget is self.txt_zipcode and len(widget.text) >= 5:  # Ensure zip code is valid
            opts.location = widget.text

        # Persist to disk
        opts.save_to_settings()

