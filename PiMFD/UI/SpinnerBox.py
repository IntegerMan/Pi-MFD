# coding=utf-8
"""
Contains code useful for rendering spinner (+ / -) selection boxes
"""
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Panels import StackPanel

from PiMFD.UI.Text import TextBlock


__author__ = 'Matt Eland'


class SpinnerBox(FocusableWidget):
    """
    Represents a segment of text
    """

    label_block = None
    label = None
    value_block = None
    value = None
    panel = None

    def __init__(self, display, page, label, value):
        super(SpinnerBox, self).__init__(display, page)
        self.label = label
        self.value = value
        self.label_block = TextBlock(display, page, label)
        self.value_block = TextBlock(display, page, value)
        self.panel = StackPanel(display, page, is_horizontal=True)
        self.panel.children = [self.label_block, self.value_block]

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        :rtype : RectType
        """

        self.label_block.text = self.label
        self.value_block.text = self.value
        self.label_block.is_highlighted = self.is_focused()
        self.value_block.is_highlighted = self.is_focused()

        return self.set_dimensions_from_rect(self.panel.render_at(self.pos))
