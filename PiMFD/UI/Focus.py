# coding=utf-8
"""
Code for UI Widget focusability / navigation
"""
from PiMFD.UI.Panels import UIWidget

__author__ = 'Matt Eland'


class FocusableWidget(UIWidget):
    """
    A UIWidget that can receieve and manage focus
    """

    def __init__(self, display, page):
        super(FocusableWidget, self).__init__(display, page)
        page.register_focusable(self)


    def is_focused(self):
        """
        Determines whether or not this widget is focused
        :return: whether or not this widget is focused
        """
        return self.page.focus is self

    # noinspection PyMethodMayBeStatic
    def got_focus(self):
        """
        Occurs when the control gets focus
        """
        pass

    # noinspection PyMethodMayBeStatic
    def lost_focus(self):
        """
        Occurs when the control loses focus
        """
        pass

    # noinspection PyMethodMayBeStatic
    def handle_key(self, key):
        """
        Handles a keypress
        :param key: The keycode
        :returns: True if the event was handled; otherwise False
        """
        return False

    def state_changed(self):
        """
        Handles the control's state changed by passing along a message to the container
        """
        if self.page:
            self.page.handle_control_state_changed(self)