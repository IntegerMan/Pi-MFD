# coding=utf-8
"""
Defines the MFDPage used as a root for other pages in the application.
"""
from PiMFD.UI.Panels import StackPanel
from PiMFD.UI.Rendering import render_text_centered

__author__ = 'Matt Eland'


class MFDPage(object):
    """
    Represents a page within the application
    :type controller: PiMFD.Controller.MFDController The controller
    :type application: The application containing this page.
    """
    top_headers = list()
    bottom_headers = list()

    panel = None
    application = None
    controller = None
    display = None

    def __init__(self, controller, application):
        self.controller = controller
        self.display = controller.display
        self.application = application
        self.top_headers = list()
        self.bottom_headers = list()
        self.panel = StackPanel(controller.display)

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
        self.panel.render_at(self.display.get_content_start_pos())


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
