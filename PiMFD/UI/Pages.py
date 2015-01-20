# coding=utf-8

"""
Contains logic on pages for rendering controls and handling input
"""

from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.WidgetBase import UIObject

__author__ = 'Matt Eland'


class UIPage(UIObject):
    """
    Represents a user interface page.
    """

    focusables = list()

    panel = None
    focus = None

    def __init__(self, display):
        super(UIPage, self).__init__(display)
        self.panel = StackPanel(display, self)
        self.focusables = list()

    def set_focus(self, widget):
        """
        Sets focused to the specified control. The prior focus (if one is present) will receive a lost_focus call and
        the newly focused control (if one is present) will receive a got_focus control
        :param widget: The widget to focus. Can be None.
        :return: The new focus
        """

        # If this is a non-event, just go away
        if self.focus is widget:
            return

        # Tell the old focus it's old news
        if self.focus:
            self.focus.lost_focus()

        self.focus = widget

        # Tell the new focus it's getting some TLC
        if widget:
            widget.got_focus()

        return self.focus

    def clear_focus(self):
        """
        Clears the currently focused control (if any was present)
        """
        self.set_focus(None)

    def render(self):
        """
        Handles rendering the page.
        :type display: PiMFD.DisplayManager.DisplayManager The display manager.
        """
        return self.panel.render_at(self.display.get_content_start_pos())

    def focus_first_eligibile(self):
        """
        Focuses the first eligible input element
        :return: the first eligible input element
        """
        if len(self.focusables) > 0:
            return self.set_focus(self.focusables[0])
        else:
            return None

    def handle_up_key(self):
        """
        Handles an up keypress
        """
        if self.focus:
            index = self.focusables.index(self.focus)
            if index == 0:
                self.set_focus(self.focusables[-1])
            elif index < 0:
                self.focus_first_eligibile()
            else:
                self.set_focus(self.focusables[index - 1])
        else:
            self.focus_first_eligibile()

    def handle_down_key(self):
        """
        Handles a down keypress
        """
        if self.focus:
            index = self.focusables.index(self.focus)
            if 0 <= index < (len(self.focusables) - 1):
                self.set_focus(self.focusables[index + 1])
            else:
                self.focus_first_eligibile()
        else:
            self.focus_first_eligibile()

    # noinspection PyMethodMayBeStatic
    def handle_key(self, key):
        """
        Handles a miscellaneous keyboard input
        :param key: The keycode
        :return: True if the code was handled, otherwise False
        """
        if self.focus:
            return self.focus.handle_key(key)

        return False

    # noinspection PyMethodMayBeStatic
    def handle_left_key(self):
        """
        Handles a left keypress
        """
        pass

    # noinspection PyMethodMayBeStatic
    def handle_right_key(self):
        """
        Handles a right keypress
        """
        pass

    # noinspection PyMethodMayBeStatic
    def handle_control_state_changed(self, widget):
        """
        Responds to a state changed event in the specified widget
        :param widget: The widget whose state changed
        """
        pass

    def register_focusable(self, focusable):
        """
        Registers a control as a focusable input element. This is necessary to hook up the keyboard navigational
        system.
        :param focusable: The control that can receive focus
        """
        if focusable is not None:
            self.focusables.append(focusable)


