# coding=utf-8
from pygame.rect import Rect

__author__ = 'Matt Eland'


class UIWidget(object):
    """
    Represents a basic UI widget that the system is capable of arranging and rendering.
    """

    # Basic Arrangement Attributes
    pos = (0, 0)
    size = (0, 0)
    left = 0
    right = 0
    top = 0
    bottom = 0
    width = 0
    height = 0
    rect = Rect(0, 0, 0, 0)

    # We'll need a reference to the display manager in order to render properly
    display = None

    def __init__(self, display):
        self.display = display

    # noinspection PyMethodMayBeStatic
    def render(self):
        """
        Renders the widget to the screen
        """
        return self.rect

    def set_dimensions_from(self, target):
        """
        Clones all dimension attributes from the target object
        :param target: The target to take values from
        """
        self.pos = target.pos
        self.size = target.size
        self.left = target.left
        self.right = target.right
        self.top = target.top
        self.bottom = target.bottom
        self.width = target.width
        self.height = target.height
        self.rect = target.rect

    def set_dimensions_from_rect(self, rect):
        """
        Copies dimensional attributes from the specified rect
        :param rect: The rectangle
        """
        self.rect = rect
        self.pos = rect.x, rect.y
        self.size = rect.size
        self.left = rect.left
        self.right = rect.right
        self.top = rect.top
        self.bottom = rect.bottom
        self.width = rect.width
        self.height = rect.height


class UIPanel(UIWidget):
    """
    A base class for panels used for UIWidget arrangement
    """

    children = list()

    def __init__(self, display):
        super(UIPanel, self).__init__(display)
        self.children = list()


class StackPanel(UIPanel):
    """
    A class used for vertical or horizontal arrangement of UIWidgets in sequence
    """

    padding = 8, 8
    is_horizontal = False

    def __init__(self, display, is_horizontal=False):
        super(StackPanel, self).__init__(display)
        self.padding = display.padding_x, display.padding_y
        self.is_horizontal = is_horizontal

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

        """
        Renders all children in the panel
        :return: A Rect representing the bounds of the panel
        """
        for child in self.children:

            # Position the child relative to where it should be and render it
            child.pos = x, y
            child_rect = child.render()

            # Now that we've rendered, we need to adjust our running dimensions
            # and figure out where to put the next one
            if self.is_horizontal:

                # Horizontal layout mode - go left to right
                if child_rect.height > self.height:
                    self.height = child_rect.height

                self.width = child.right - self.left

                x = child.right + self.padding[0]

            else:

                # Vertical layout mode (default) - go top to bottom
                if child_rect.width > self.width:
                    self.width = child_rect.width

                self.height = child.bottom - self.top

                y = child.bottom + self.padding[1]

        # Update and return our bounds
        self.rect = Rect(self.left, self.top, self.width, self.height)
        self.set_dimensions_from_rect(self.rect)
        return self.rect