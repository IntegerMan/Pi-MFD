# coding=utf-8
"""
Contains code useful for rendering lines of text
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget
from PiMFD.UI.Rendering import render_text


__author__ = 'Matt Eland'


class TextBlock(UIWidget):
    """
    Represents a segment of text
    """

    foreground = (255, 255, 255, 255)
    font = None
    text = None
    format_data = None

    def __init__(self, display, text):
        super(TextBlock, self).__init__(display)
        self.font = display.font_normal
        self.foreground = display.color_scheme.foreground
        self.text = text

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        :rtype : RectType
        """

        self.left = self.pos[0]
        self.top = self.pos[1]

        # Do string formatting as needed
        effectiveText = self.text
        if self.text is not None:
            effectiveText = self.text.format(self.format_data)

        if self.font is not None and effectiveText is not None:
            self.rect = render_text(self.display, self.font, effectiveText, self.pos[0], self.pos[1], self.foreground)
            self.bottom = self.rect.bottom
            self.right = self.rect.right
        else:
            self.bottom = self.pos[1]
            self.right = self.pos[0]
            self.rect = Rect(self.left, self.top, 0, 0)

        self.width = self.right - self.left
        self.height = self.bottom - self.top

        return self.rect