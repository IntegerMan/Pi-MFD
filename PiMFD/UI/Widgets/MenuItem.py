# coding=utf-8

"""
Contains code for a menu item focusable widget
"""

__author__ = 'Matt Eland'

from PiMFD.UI import Keycodes
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Keycodes import is_right_key, is_enter_key
from PiMFD.UI.Text import TextBlock


class MenuItem(FocusableWidget):
    """
    Represents a segment of text
    """

    text = None
    text_data = None

    def __init__(self, display, page, text):

        """
        :type text: str
        """
        super(MenuItem, self).__init__(display, page)
        self.text = text
        self.label = TextBlock(display, page, text)

    def arrange(self):
        """
        Handles the arrangement of the control
        :return: The desired size of the control
        """

        # Pass on data to the control
        self.label.text = self.text
        self.label.text_data = self.text_data
        self.label.is_highlighted = self.is_focused()
        self.label.arrange()

        self.desired_size = self.label.desired_size

        return super(MenuItem, self).arrange()

    def render(self):
        """
        Renders the control to the screen
        :rtype : RectType
        """

        return self.label.render_at(self.pos)

    def handle_key(self, key):
        """
        Handles a keypress
        :type key: int
        :param key: The key pressed
        :return: True if handled; otherwise False
        """

        # Allow the user to click it
        if is_enter_key(key) or key == Keycodes.KEY_SPACE or is_right_key(key):
            self.play_button_sound()
            self.state_changed()
            return True

        return super(MenuItem, self).handle_key(key)

