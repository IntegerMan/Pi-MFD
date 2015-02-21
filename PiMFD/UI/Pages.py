# coding=utf-8

"""
Contains logic on pages for rendering controls and handling input
"""
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Keycodes import is_up_key, is_down_key

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
        """
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        """
        super(UIPage, self).__init__(display)
        self.panel = self.get_panel()
        self.focusables = list()
        
    def get_panel(self):
        """
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        """
        return StackPanel(self.display, self)
        
    def set_focus(self, widget):
        """
        Sets focused to the specified control. The prior focus (if one is present) will receive a lost_focus call and
        the newly focused control (if one is present) will receive a got_focus control
        :type widget: FocusableWidget or None
        :param widget: The widget to focus. Can be None.
        :return: The new focus
        """

        had_focus = self.focus is not None

        # If this is a non-event, just go away
        if self.focus is widget:
            return

        # Tell the old focus it's old news
        if self.focus:
            self.focus.lost_focus()

        self.focus = widget

        # Tell the new focus it's getting some TLC
        if widget:

            print('focusing {}'.format(str(widget)))
            widget.got_focus()
            
            if widget.parent:
                widget.parent.child_focused(widget)

        elif had_focus:
            print('no focus')

        return self.focus

    def clear_focus(self):
        """
        Clears the currently focused control (if any was present)
        """
        self.set_focus(None)

    def arrange(self):
        
        if self.panel:
            self.panel.pos = self.display.get_content_start_pos()
            self.desired_size = self.panel.desired_size
        
        return super(UIPage, self).arrange()

    def render(self):
        """
        Handles rendering the page.
        """
        return self.panel.render()

    def focus_first_eligibile(self):
        """
        Focuses the first eligible input element
        :return: the first eligible input element
        """
        if len(self.focusables) > 0:
            return self.set_focus(self.focusables[0])
        else:
            return None

    # noinspection PyMethodMayBeStatic
    def handle_key(self, key):
        """
        Handles a miscellaneous keyboard input
        :param key: The keycode
        :return: True if the code was handled, otherwise False
        """

        # Give the focused control first crack at the event
        if self.focus:
            if self.focus.handle_key(key):
                return True

        # Okay, control didn't want anything, now let's process some specialized input handlers for navigation

        # TODO: This code will need to bypass disabled focusable controls

        if is_up_key(key):
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

            return True

        if is_down_key(key):
            if self.focus:

                index = self.focusables.index(self.focus)
                if 0 <= index < (len(self.focusables) - 1):
                    self.set_focus(self.focusables[index + 1])
                else:
                    self.focus_first_eligibile()

            else:
                self.focus_first_eligibile()

            return True

        # I don't know what this key is, I'm not going to handle this.

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

    def unregister_focusable(self, focusable):
        """
        Deregisters a control as a focusable input element.
        :param focusable: The control that can no longer receive focus
        """
        if focusable is not None and focusable in self.focusables:
            self.focusables.remove(focusable)

    def clear_focusables(self):
        """
        Clears the list of focusable controls.
        """
        self.focusables = []