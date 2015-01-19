# coding=utf-8
"""
Defines the MFDPage used as a root for other pages in the application.
"""
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_text_centered
from PiMFD.UI.Text import TextBlock

__author__ = 'Matt Eland'


class MFDPage(object):
    """
    Represents a page within the application
    :type controller: PiMFD.Controller.MFDController The controller
    :type application: The application containing this page.
    """
    top_headers = list()
    bottom_headers = list()
    focusables = list()

    panel = None
    application = None
    controller = None
    display = None
    focus = None

    def __init__(self, controller, application):
        self.controller = controller
        self.display = controller.display
        self.application = application
        self.top_headers = list()
        self.bottom_headers = list()
        self.panel = StackPanel(controller.display, self)
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

    def get_label(self, text):
        """
        Builds a label with the specified text. This is a conveinence method since labels are extremely common
        :param text: The text for the label
        :return: The TextBlock
        """
        return TextBlock(self.display, self, text)

    def get_header_label(self, text):
        """
        Builds a highlighted header label with the specified text.
        This is a conveinence method since header labels are extremely common
        :param text: The text for the label
        :return: The TextBlock
        """
        return TextBlock(self.display, self, text, is_highlighted=True)

    # noinspection PyMethodMayBeStatic
    def handle_unselected(self):
        """
        Occurs when a page was the selected page within an application but no longer is the selected page.
        """
        pass

    # noinspection PyMethodMayBeStatic
    def handle_selected(self):
        """
        Occurs when a page was selected but another page was selected instead, causing this page to be unselected.
        """
        pass

    def handle_reselected(self):
        """
        If the page is selected but the user is trying to navigate to it anyway, retrigger and refresh weather data.
        """
        self.application.page_reselected(self)

    def get_button_text(self):
        """
        Gets the button text
        :return: The button text
        """
        return 'UNKN'

    def render(self, display):
        """
        Handles rendering the page.
        :type display: PiMFD.DisplayManager.DisplayManager The display manager.
        """
        return self.panel.render_at(self.display.get_content_start_pos())

    def handle_enter_key(self):
        """
        Handles an enter or keypad enter keypress
        """
        if self.focus:
            self.focus.handle_enter_key()

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
        :return: True if the code was handled, otherwise false
        """
        pass

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


class SimpleMessagePage(MFDPage):
    """
    Represents a simple single-message page, defaulting to 'not implemented'.
    """

    button_text = "NI"
    message = "Not Implemented"

    def __init__(self, controller, application, label, message='Not Implemented'):
        super(SimpleMessagePage, self).__init__(controller, application)
        self.button_text = label
        self.message = message

    def get_button_text(self):
        """
        Gets the text for a button
        :return: The button text
        """
        return self.button_text

    def render(self, display):
        """
        Renders a simple message page.
        :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager
        """
        super(SimpleMessagePage, self).render(display)

        render_text_centered(display,
                             display.font_normal,
                             self.message,
                             display.res_x / 2,
                             (display.res_y / 2) - (display.font_size_normal / 2),
                             display.color_scheme.foreground)
