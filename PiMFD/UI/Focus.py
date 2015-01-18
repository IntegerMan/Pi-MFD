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
