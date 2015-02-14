# coding=utf-8
"""
Defines the MFDPage used as a root for other pages in the application.
"""
import traceback

import pygame

from PiMFD.UI import Keycodes
from PiMFD.UI.ImageRendering import ImageRenderer, WebImageRenderer
from PiMFD.UI.Pages import UIPage
from PiMFD.UI.Rendering import render_text_centered, render_triangle_down, render_triangle_up
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

    page_y = 1
    num_pages_y = 1

    def __init__(self, controller, application, auto_scroll=True):
        """

        :type controller: PiMFD.Controller.MFDController
        """
        super(MFDPage, self).__init__(controller.display)

        self.controller = controller
        self.application = application
        self.top_headers = list()
        self.bottom_headers = list()

        # Position at start of content area
        self.panel.pos = controller.display.get_content_start_pos()
        self.panel.left = self.panel.pos[0]
        self.panel.top = self.panel.pos[1]

        self.auto_scroll = auto_scroll

    def get_label(self, text):
        """
        Builds a label with the specified text. This is a conveinence method since labels are extremely common
        :param text: The text for the label
        :return: The TextBlock
        """
        return TextBlock(self.display, self, text)

    def get_list_label(self, text):
        """
        Builds a label with the specified text. This is a conveinence method since labels are extremely common
        :param text: The text for the label
        :return: The TextBlock
        """

        block = self.get_label(text)
        block.font = self.display.fonts.list
        return block

    def get_header_label(self, text):
        """
        Builds a highlighted header label with the specified text.
        This is a conveinence method since header labels are extremely common
        :param text: The text for the label
        :return: The TextBlock
        """
        block = self.get_label(text)
        block.is_highlighted = True
        return block

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

    def constrain_pages(self):
        if self.page_y > self.num_pages_y:
            self.page_y = max(1, self.num_pages_y)
        elif self.page_y <= 0:
            self.page_y = 1

    def arrange(self):

        self.desired_size = self.panel.arrange()

        return super(MFDPage, self).arrange()


    def render(self):

        min_y = self.display.get_content_start_y()
        max_y = self.display.get_content_end_y()
        page_size_y = max_y - min_y

        if self.panel:
            target_pos = (self.display.get_content_start_x(), min_y - ((self.page_y - 1) * page_size_y))
            rect = self.panel.render_at(target_pos)
        else:
            rect = super(MFDPage, self).render()

        # Calculate number of whole pages
        self.num_pages_y = rect.height / page_size_y

        # Advance to the next whole page if first page or non-trivial content on last page
        if self.num_pages_y == 0 or rect.height % page_size_y > 16:
            self.num_pages_y += 1

        # Smart-Constrain Page
        self.constrain_pages()

        # Render Overflow indicators if off screen
        if self.auto_scroll:

            paging_color = self.display.color_scheme.foreground

            # If we have already paged, show MORE link at the top
            if self.page_y > 1:
                arrow_pos = [self.display.res_x - 18, min_y]
                render_triangle_up(self.display, paging_color, arrow_pos, 8)
                render_text_centered(self.display,
                                     self.display.fonts.small,
                                     "MORE",
                                     arrow_pos[0],
                                     arrow_pos[1] + 3,
                                     paging_color)

            # If we have more pages, show a MORE link at the bottom
            if self.page_y < self.num_pages_y:
                arrow_pos = [self.display.res_x - 18, max_y]
                render_triangle_down(self.display, paging_color, arrow_pos, 8)
                render_text_centered(self.display,
                                     self.display.fonts.small,
                                     "MORE",
                                     arrow_pos[0],
                                     arrow_pos[1] - 3 - self.display.fonts.small.size,
                                     paging_color)

        return rect

    def handle_key(self, key):

        if key in (Keycodes.KEY_PAGEDOWN, Keycodes.KEY_KP3):
            if self.num_pages_y > self.page_y:
                self.page_y += 1
                self.constrain_pages()
                return True

        elif key in (Keycodes.KEY_PAGEUP, Keycodes.KEY_KP9):
            if self.page_y > 1:
                self.page_y -= 1
                self.constrain_pages()
                return True

        return super(MFDPage, self).handle_key(key)

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

