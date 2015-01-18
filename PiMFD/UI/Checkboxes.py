# coding=utf-8

"""
Contains checkbox style controls for manipulating pages
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget, StackPanel
from PiMFD.UI.Rendering import draw_rectangle
from PiMFD.UI.Text import TextBlock

__author__ = 'Matt Eland'


class CheckBoxGlyph(UIWidget):
    """
    A checkbox style UI without a label associated with it. This is used by other controls to render a checkbox UI.
    Use CheckBox instead if you're wanting to put this on a page.
    """

    checked = False

    def __init__(self, display, checked=False):
        super(CheckBoxGlyph, self).__init__(display)
        self.checked = checked

    def render(self):
        """
        Renders the glyph and returns its dimensions
        :return: The dimensions of the glyph
        """

        rect_size = 28

        self.rect = Rect(self.pos[0], self.pos[1], rect_size, rect_size)

        # Draw the border
        draw_rectangle(self.display, self.display.color_scheme.foreground, self.rect)

        # Draw checkmark (if checked)
        if self.checked:
            check_pad = 4
            checked_rect = Rect(self.pos[0] + check_pad,
                                self.pos[1] + check_pad,
                                rect_size - (check_pad * 2),
                                rect_size - (check_pad * 2))

            draw_rectangle(self.display, self.display.color_scheme.foreground, checked_rect, width=0)

        # Update and return our dimensions
        self.set_dimensions_from_rect(self.rect)
        return self.rect


class CheckBox(UIWidget):
    """
    A CheckBox with an associated label.
    """

    text = None
    panel = None
    label = None
    glyph = None
    checked = False

    def __init__(self, display, label):
        super(CheckBox, self).__init__(display)
        self.label = TextBlock(display, label)
        self.text = label
        self.glyph = CheckBoxGlyph(display)
        self.panel = StackPanel(display, is_horizontal=True)
        self.panel.children = [self.label, self.glyph]

    def render(self):
        """
        Renders the checkbox with its current state
        :return: The rectangle of the checkbox
        """

        # Pass along our values to the children
        self.label.text = self.text
        self.glyph.checked = self.checked

        # Render the panel's contents
        self.panel.set_dimensions_from(self)
        self.panel.render()

        self.set_dimensions_from(self.panel)

        return self.panel.rect
