# coding=utf-8
from pygame.rect import Rect

from PiMFD.UI.WidgetBase import UIWidget


__author__ = 'Matt Eland'

class UIPanel(UIWidget):
    """
    A base class for panels used for UIWidget arrangement
    """

    children = list()
    keep_together = False

    def __init__(self, display, page, keep_together=False):
        super(UIPanel, self).__init__(display, page)
        self.children = list()
        self.keep_together = keep_together

    def arrange(self):
        # Not a correct implementation for most usages, but we do want to ensure things get arranged
        for child in self.children:
            child.arrange()

        return super(UIPanel, self).arrange()

class StackPanel(UIPanel):
    """
    A class used for vertical or horizontal arrangement of UIWidgets in sequence
    """

    padding = 8, 8
    is_horizontal = False
    auto_orient = False

    def __init__(self, display, page, is_horizontal=False, auto_orient=False, keep_together=False):
        super(StackPanel, self).__init__(display, page, keep_together=keep_together)
        self.padding = display.padding_x, display.padding_y
        self.is_horizontal = is_horizontal
        self.auto_orient = auto_orient

    def arrange(self):

        width = 0
        height = 0

        for child in self.children:

            # Ask the child to measure itself
            child_size = child.arrange()

            if self.is_horizontal:

                # Add up widths (with padding) and use largest height encountered
                if child_size[0] > 0:
                    width += child_size[0] + self.padding[0]

                height = max(child_size[1], height)

            else:

                # Add up heights (with padding) and use largest width encountered
                if child_size[1] > 0:
                    height += child_size[1] + self.padding[1]

                width = max(child_size[0], width)

        # Update size and return
        self.desired_size = width, height
        return self.desired_size


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
        self.width = self.desired_size[0]
        self.height = self.desired_size[1]

        for child in self.children:

            # Position the child relative to where it should be and render it
            child.render_at((x, y))

            # Now that we've rendered, we need to adjust our running dimensions
            # and figure out where to put the next one
            if self.is_horizontal:

                # Don't add padding if we're zero-width
                if child.right > child.left:
                    x = child.right + self.padding[0]
                else:
                    x = child.right

            else:

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