# coding=utf-8
"""
Contains code useful for rendering spinner (+ / -) selection boxes
"""
from PiMFD.UI.Focus import FocusableWidget
from PiMFD.UI.Keycodes import is_right_key, is_plus_key, is_minus_key, is_left_key
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
    items = []

    def __init__(self, display, page, label, value, items=None):

        """
        :type items: list
        """
        if not items:
            items = []

        super(SpinnerBox, self).__init__(display, page)
        self.label = label
        self.value = value
        self.label_block = TextBlock(display, page, label)
        self.value_block = TextBlock(display, page, value)
        self.panel = StackPanel(display, page, is_horizontal=True)
        self.panel.children = [self.label_block, self.value_block]
        self.items = items

    def arrange(self):

        self.label_block.text = self.label
        self.value_block.text = self.value
        self.label_block.is_highlighted = self.is_focused()
        self.value_block.is_highlighted = self.is_focused()

        self.desired_size = self.panel.arrange()

        return super(SpinnerBox, self).arrange()

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        :rtype : RectType
        """

        return self.set_dimensions_from_rect(self.panel.render_at(self.pos))

    def handle_key(self, key):

        if is_plus_key(key) or is_right_key(key):
            self.move_next()
            return True

        if is_minus_key(key) or is_left_key(key):
            self.move_previous()
            return True

        return super(SpinnerBox, self).handle_key(key)

    def get_selected_index(self):

        if not self.items or self.value not in self.items:
            return -1

        return self.items.index(self.value)

    def move_next(self):

        if not self.items or len(self.items) <= 0:
            return

        current_index = self.get_selected_index()

        if current_index < 0:
            current_index = 0
        elif current_index >= len(self.items) - 1:
            current_index = 0
        else:
            current_index += 1

        new_value = self.items[current_index]
        if self.value != new_value:
            self.value = new_value
            self.state_changed()

    def move_previous(self):

        if not self.items or len(self.items) <= 0:
            return

        current_index = self.get_selected_index()

        if current_index < 0:
            current_index = len(self.items) - 1
        elif current_index >= len(self.items):
            current_index = 0
        else:
            current_index -= 1

        new_value = self.items[current_index]
        if self.value != new_value:
            self.value = new_value
            self.state_changed()

