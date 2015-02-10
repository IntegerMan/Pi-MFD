# coding=utf-8
"""
Defines the MFDPage used as a root for other pages in the application.
"""
import traceback

import pygame

from PiMFD.UI.ImageRendering import ImageRenderer, WebImageRenderer
from PiMFD.UI.Pages import UIPage
from PiMFD.UI.Rendering import render_text_centered
from PiMFD.UI.Text import TextBlock


__author__ = 'Matt Eland'


class MFDPage(UIPage):
    """
    Represents a page within the application
    :type controller: PiMFD.Controller.MFDController The controller
    :type application: The application containing this page.
    """
    top_headers = list()
    bottom_headers = list()

    application = None
    controller = None

    auto_scroll = True

    def __init__(self, controller, application, auto_scroll=True):
        super(MFDPage, self).__init__(controller.display)

        self.controller = controller
        self.application = application
        self.top_headers = list()
        self.bottom_headers = list()

        self.auto_scroll = auto_scroll

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

    def get_image(self, image_path, interval=0, max_width=None):

        """
        Builds an Image Renderer Component
        :rtype : ImageRenderer
        :type image_path: str
        :type interval: int
        :type max_width: int
        """
        try:
            if image_path.startswith('http'):
                return WebImageRenderer(self.display, self, image_path, interval=interval, max_width=max_width)
            else:
                surface = pygame.image.load(image_path)
                return ImageRenderer(self.display, self, surface, max_width=max_width)

        except:
            error_message = "Problem loading image {0}: {1}\n".format(image_path, str(traceback.format_exc()))
            print(error_message)
            return None

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

    def set_focus(self, widget):
        self.controller.play_button_sound()

        return super(MFDPage, self).set_focus(widget)

    def center_text(self, text, color=None):
        if not color:
            color = self.display.color_scheme.highlight

        render_text_centered(self.display,
                             self.display.fonts.normal,
                             text,
                             self.display.res_x / 2.0,
                             self.display.res_y / 2.0 - (self.display.fonts.normal.size / 2),
                             color)


    def handle_mouse_left_click(self, pos):
        return False

