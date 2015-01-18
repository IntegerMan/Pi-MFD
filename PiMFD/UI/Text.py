# coding=utf-8
"""
Contains code useful for rendering lines of text
"""
from PiMFD.UI.Rendering import render_text

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

    # We'll need a reference to the display manager in order to render properly
    display = None

    def __init__(self, display):
        self.display = display

    def render(self):
        """
        Renders the widget to the screen
        """
        pass


class TextBlock(UIWidget):
    """
    Represents a segment of text
    """

    foreground = (255, 255, 255, 255)
    font = None
    text = None

    def __init__(self, display, text):
        super(TextBlock, self).__init__(display)
        self.font = display.font_normal
        self.foreground = display.color_scheme.foreground
        self.text = text

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        """

        self.left = self.pos[0]
        self.top = self.pos[1]

        if self.font is not None:
            self.rect = render_text(self.display, self.font, self.text, self.pos[0], self.pos[1], self.foreground)
            self.bottom = self.rect.bottom
            self.right = self.rect.right
        else:
            self.bottom = self.pos[1]
            self.right = self.pos[0]

        self.width = self.right - self.left
        self.height = self.bottom - self.top