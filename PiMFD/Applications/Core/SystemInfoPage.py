# coding=utf-8

import platform

from PiMFD.Applications.MFDPage import MFDPage
from PiMFD.UI.Text import SpacerLine


__author__ = 'Matt Eland'


class SysInfoPage(MFDPage):
    """
    The root level page for the system app
    """

    def __init__(self, controller, application):
        super(SysInfoPage, self).__init__(controller, application)

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
        return "INFO"

    def arrange(self):

        opts = self.controller.options

        self.lbl_app_header.text_data = opts.app_name
        self.lbl_app_version.text_data = opts.app_version
        self.lbl_app_legal.text_data = opts.app_author, opts.copyright_year
        self.lbl_sys_name.text_data = platform.platform(), platform.release(), platform.machine()
        self.lbl_sys_processor.text_data = platform.processor()
        self.lbl_sys_net_id.text_data = platform.node()
        self.lbl_sys_display.text_data = self.display.bounds.right, self.display.bounds.bottom
        self.lbl_sys_python.text_data = platform.python_version(), platform.python_implementation(), platform.python_compiler()

        return super(SysInfoPage, self).arrange()
