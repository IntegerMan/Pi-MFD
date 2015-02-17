# coding=utf-8

"""
Various input controls
"""
from pygame.rect import Rect

from PiMFD.UI import Keycodes
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Panels import UIWidget, StackPanel
from PiMFD.UI.Rendering import render_rectangle, render_text
from PiMFD.UI.Text import TextBlock


__author__ = 'Matt Eland'


class TextGlyph(UIWidget):
    """
    Represents a text entry area
    """

    render_focus = False
    text_width = 85
    text = None
    pad_x = 6
    pad_y = 6

    def arrange(self):
        vert_size = self.display.fonts.normal.size + self.display.padding_y + self.display.padding_y

        self.desired_size = self.text_width, vert_size

        return super(TextGlyph, self).arrange()


    def render(self):
        """
        Renders the glyph and returns its dimensions
        :return: The dimensions of the glyph
        """

        # Size Constants
        self.rect = Rect(self.pos[0], self.pos[1], self.desired_size[0], self.desired_size[1])

        # Draw the border
        focus_color = self.display.color_scheme.get_focus_color(self.render_focus)
        render_rectangle(self.display, focus_color, self.rect)

        # Draw the text
        display = self.display
        render_text(display, display.fonts.normal, self.text, self.pos[0] + self.pad_x, self.pos[1] + self.pad_y,
                    focus_color)

        # Update and return our dimensions
        return self.set_dimensions_from_rect(self.rect)


class TextBox(FocusableWidget):
    """
    Represents a text entry control with associated label.
    """

    label_text = None
    text = None
    text_width = 100
    max_length = None
    allow_alpha = True
    allow_numeric = True

    def __init__(self, display, page, label=None, text=None, text_width=100):
        super(TextBox, self).__init__(display, page)

        self.text = text
        self.label_text = label
        self.label = TextBlock(display, page, label)
        self.glyph = TextGlyph(display, page)
        self.text_width = 100

        self.panel = StackPanel(display, page, is_horizontal=True)
        self.panel.center_align = True
        self.panel.children = [self.label, self.glyph]

    def arrange(self):

        # Pass along our values to the children
        self.label.text = self.label_text
        self.glyph.text = self.text

        self.desired_size = self.panel.arrange()

        return super(TextBox, self).arrange()

    def render(self):
        """
        Renders the TextBox with its current state
        :return: The rectangle of the TextBox
        """

        # Render the panel's contents
        self.panel.set_dimensions_from(self)
        self.panel.render()

        return self.set_dimensions_from(self.panel)

    def got_focus(self):
        """
        Occurs when the control gets focus
        """
        self.label.is_highlighted = True
        self.glyph.render_focus = True
        super(TextBox, self).got_focus()

    def lost_focus(self):
        """
        Occurs when the control loses focus
        """
        self.label.is_highlighted = False
        self.glyph.render_focus = False
        super(TextBox, self).lost_focus()

    def can_input_more(self):
        """
        Returns whether or not there is room to enter more characters (according to max_length)
        :return: whether or not there is room to enter more characters (according to max_length)
        """
        return self.max_length is None or len(self.text) < self.max_length

    def handle_key(self, key):
        """
        Handles a keypress
        :param key: The keycode
        :returns: True if the event was handled; otherwise False
        """

        if key == Keycodes.KEY_BACKSPACE:
            if self.text and len(self.text) > 0:
                self.text = self.text[:-1]  # TODO: This is simplistic and needs to work with a cursor index
                return True

        if key == Keycodes.KEY_DELETE:
            if self.text and len(self.text) > 0:
                self.text = self.text[1:]  # TODO: This is simplistic and needs to work with a cursor index
                return True

        if self.allow_numeric and Keycodes.KEY_0 <= key <= Keycodes.KEY_9 and self.can_input_more():
            char = key - Keycodes.KEY_0
            self.text += str(char)  # TODO: This will need to take cursor location into account
            self.state_changed()
            return True

        if self.allow_alpha and Keycodes.KEY_a <= key <= Keycodes.KEY_z and self.can_input_more():
            char = chr(key)
            self.text += str(char).upper()  # TODO: This will need to take cursor location into account
            self.state_changed()
            return True

        return super(TextBox, self).handle_key(key)



