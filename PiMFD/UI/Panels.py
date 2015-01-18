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


class UIPanel(UIWidget):
    children = list()

    def __init__(self, display):
        super(UIPanel, self).__init__(display)
        self.children = list()


class StackPanel(UIPanel):
    padding_y = 8

    def __init__(self, display):
        super(StackPanel, self).__init__(display)
        self.padding_y = display.padding_y

    # TODO: It'd be good to support horizontal rendering as well



    def render(self):

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

            # Position the child relative to where it should be.
            child.pos = x, y

            child_rect = child.render()
            if child_rect.width > self.width:
                self.width = child_rect.width

            self.height = child.bottom - self.top

            y = child.bottom + self.padding_y

        # Update and return our bounds
        self.rect = Rect(self.left, self.top, self.width, self.height)
        self.right, self.bottom = self.rect.right, self.rect.bottom
        return self.rect