# coding=utf-8
from pygame.rect import Rect

from PiMFD.UI.WidgetBase import UIWidget


__author__ = 'Matt Eland'

class UIPanel(UIWidget):
    """
    A base class for panels used for UIWidget arrangement
    """

    children = list()

    def __init__(self, display, page):
        super(UIPanel, self).__init__(display, page)
        self.children = list()


class StackPanel(UIPanel):
    """
    A class used for vertical or horizontal arrangement of UIWidgets in sequence
    """

    padding = 8, 8
    is_horizontal = False
    auto_orient = False

    def __init__(self, display, page, is_horizontal=False, auto_orient=False):
        super(StackPanel, self).__init__(display, page)
        self.padding = display.padding_x, display.padding_y
        self.is_horizontal = is_horizontal
        self.auto_orient = auto_orient

    def render(self):
        """
        Renders the panel and all of its children
        :return: A rect indicating the dimensions of the panel
        """

        self.width = 0
        self.height = 0

        x, y = self.pos

        self.top = y
        self.left = x

        for child in self.children:

            # Position the child relative to where it should be and render it
            child_rect = child.render_at((x, y))

            # Now that we've rendered, we need to adjust our running dimensions
            # and figure out where to put the next one
            if self.is_horizontal:

                # Horizontal layout mode - go left to right
                self.height = max(self.height, child_rect.height)
                self.width = child.right - self.left

                # Don't add padding if we're zero-width
                if child.right > child.left:
                    x = child.right + self.padding[0]
                else:
                    x = child.right

            else:

                # Vertical layout mode (default) - go top to bottom
                self.width = max(self.width, child_rect.width)
                self.height = child.bottom - self.top

                # Don't add padding if we're zero-height
                if child.bottom > child.top:
                    y = child.bottom + self.padding[1]
                else:
                    y = child.bottom

        # This would be better suited during an arrange / render model, but we don't have one yet, so do it here and it
        # will impact the next render pass
        if self.auto_orient:
            item_widths = [x.width + self.padding[0] for x in self.children]
            if sum(item_widths) > self.display.res_x - 32:
                self.is_horizontal = False
            else:
                self.is_horizontal = True

        # Update and return our bounds
        self.rect = Rect(self.left, self.top, self.width, self.height)
        return self.set_dimensions_from_rect(self.rect)