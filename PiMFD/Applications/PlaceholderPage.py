# coding=utf-8

"""
Contains a placeholder page used for indicating that content is coming soon.
"""

from PiMFD.Applications.MFDPage import MFDPage

__author__ = 'Matt Eland'


class SimpleMessagePage(MFDPage):
    """
    Represents a simple single-message page, defaulting to 'not implemented'.
    """

    button_text = "NI"
    message = "NO DATA"

    def __init__(self, controller, application, label, message='NO DATA'):
        super(SimpleMessagePage, self).__init__(controller, application)
        self.button_text = label
        self.message = message

    def get_button_text(self):
        """
        Gets the text for a button
        :return: The button text
        """
        return self.button_text

    def render(self):
        """
        Renders a simple message page.
        """

        self.center_text(self.message)

        return super(SimpleMessagePage, self).render()