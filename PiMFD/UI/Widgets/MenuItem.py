# coding=utf-8

"""
Contains code for a menu item focusable widget
"""
from datetime import datetime

__author__ = 'Matt Eland'

from PiMFD.UI import Keycodes
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Keycodes import is_right_key, is_enter_key
from PiMFD.UI.Text import TextBlock


class MenuItem(FocusableWidget):
    def __init__(self, display, page, content=None):
        super(MenuItem, self).__init__(display, page)

        self.content = content

    def render(self):
        """
        Renders the control to the screen
        :rtype : RectType
        """

        if self.content:
            return self.content.render_at(self.pos)
        else:
            return self.rect

    def arrange(self):

        if self.content:
            self.content.arrange()
            self.desired_size = self.content.desired_size

        return super(MenuItem, self).arrange()

    def handle_key(self, key):
        """
        Handles a keypress
        :type key: int
        :param key: The key pressed
        :return: True if handled; otherwise False
        """

        # Allow the user to click it via enter / space / right
        if self.is_enabled:
            if is_enter_key(key) or key == Keycodes.KEY_SPACE or is_right_key(key):

                process = True

                # Ensure we're not clicking too closely to a prior click event
                now = datetime.now()
                if self.last_click:
                    delta = now - self.last_click
                    if delta.microseconds < 300000:
                        process = False

                # Okay, it's not a sticky key - go for it
                if process:
                    self.last_click = now
                    self.play_button_sound()
                    self.state_changed()
                    return True

        return super(MenuItem, self).handle_key(key)


class TextMenuItem(MenuItem):
    """
    Represents a segment of text
    """

    text = None
    text_data = None
    last_click = None
    font = None

    def __init__(self, display, page, text):

        """
        :type text: str
        """
        self.text = text
        self.font = display.fonts.normal
        self.label = TextBlock(display, page, text)
        super(TextMenuItem, self).__init__(display, page, content=self.label)

    def arrange(self):
        """
        Handles the arrangement of the control
        :return: The desired size of the control
        """

        # Pass on data to the control
        self.label.text = self.text
        self.label.text_data = self.text_data
        self.label.is_highlighted = self.is_focused()
        self.label.is_enabled = self.is_enabled
        self.label.font = self.font

        return super(TextMenuItem, self).arrange()
