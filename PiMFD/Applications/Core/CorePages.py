# coding=utf-8
"""
Holds system pages for use in the system application.
"""

from PiMFD.Applications.MFDPage import MFDPage


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


