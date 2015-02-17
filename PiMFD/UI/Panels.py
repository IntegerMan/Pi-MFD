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
            child.parent = self
            child.arrange()

        return super(UIPanel, self).arrange()
    
    def child_focused(self, widget):
        pass

class StackPanel(UIPanel):
    """
    A class used for vertical or horizontal arrangement of UIWidgets in sequence
    """

    padding = 8, 8
    is_horizontal = False
    auto_orient = False
    pad_last_item = True
    center_align = False

    def __init__(self, display, page, is_horizontal=False, auto_orient=False, keep_together=False):
        super(StackPanel, self).__init__(display, page, keep_together=keep_together)
        self.padding = display.padding_x, display.padding_y
        self.is_horizontal = is_horizontal
        self.auto_orient = auto_orient

    def arrange(self):

        x, y = self.pos

        width = 0
        height = 0

        # Cause all children to arrange so we have valid sizes
        for child in self.children:
            child.parent = self
            child.arrange()
            if self.is_highlighted is not None:
                child.is_highlighted = self.is_highlighted

        max_x = self.display.get_content_end_x()
        page_size = self.display.get_content_size()[1]

        page_remaining = page_size

        # Auto-Orient as needed
        if self.auto_orient:

            item_widths = [c.width + self.padding[0] for c in self.children]
            if sum(item_widths) > max_x:
                self.is_horizontal = False
            else:
                self.is_horizontal = True

        if self.children and len(self.children) > 0:
            last_child = self.children[-1]
        else:
            last_child = None

        # Put each child where it should be
        for child in self.children:

            child_size = child.desired_size

            # Auto jump to next page to keep together
            if self.keep_together and not self.is_horizontal:
                if page_remaining < child_size[1] <= page_size:
                    y += page_remaining
                    page_remaining = page_size

            # Set position. Some things use abstract positioning, so we'll need to invalidate arrange if our position
            # has changed since initial arrange.
            if child.pos[0] != x or child.pos[1] != y:
                child.pos = x, y
                child.arrange()

            if self.is_horizontal:

                # Add up widths (with padding) and use largest height encountered
                if child_size[0] > 0:

                    if not self.pad_last_item and child is last_child:
                        child_width = child_size[0]
                    else:
                        child_width = child_size[0] + self.padding[0]

                    width += child_width
                    x += child_width

                height = max(child_size[1], height)

            else:

                # Add up heights (with padding) and use largest width encountered
                if child_size[1] > 0:

                    if not self.pad_last_item and child is last_child:
                        child_height = child_size[1]
                    else:
                        child_height = child_size[1] + self.padding[1]

                    height += child_height
                    y += child_height
                    if self.keep_together:
                        page_remaining -= child_height

                width = max(child_size[0], width)
                
        if self.center_align:
            if self.is_horizontal:
                for c in self.children:
                    half_delta = (height - c.desired_size[1]) / 2.0
                    if half_delta > 0:
                        c.pos = c.pos[0], y + half_delta
            else:
                for c in self.children:
                    half_delta = (width - c.desired_size[0]) / 2.0
                    if half_delta > 0:
                        c.pos = x + half_delta, c.pos[1]

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

        min_y = self.display.get_content_start_y()
        max_y = self.display.get_content_end_y()

        # Render children where arrange told us to
        for child in self.children:

            # Only render nodes that will be visible
            if child.pos[1] < max_y and (child.pos[1] + child.desired_size[1]) > min_y:
                child.render()

        # Update and return our bounds
        self.rect = Rect(self.left, self.top, self.width, self.height)
        return self.set_dimensions_from_rect(self.rect)
