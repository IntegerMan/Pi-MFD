# coding=utf-8
"""
Contains code useful for rendering lines of text
"""
from pygame.rect import Rect

from PiMFD.UI.Panels import UIWidget
from PiMFD.UI.Rendering import render_text


__author__ = 'Matt Eland'


class SpacerLine(UIWidget):
    """
    A simple construct for a blank line
    """

    def arrange(self):

        self.desired_size = self.display.fonts.normal.size, self.display.fonts.normal.size

        return super(SpacerLine, self).arrange()

    def render(self):
        """
        Renders a spacer line by taking up font-sized values and returning a modified bounding rect.
        """
        self.rect = Rect(self.pos[0], self.pos[1], self.desired_size[0], self.desired_size[1])
        return self.set_dimensions_from_rect(self.rect)


class TextBlock(UIWidget):
    """
    Represents a segment of text
    """

    font = None
    text = None
    text_data = None
    is_highlighted = False
    is_enabled = True
    color = None

    def __init__(self, display, page, text, is_highlighted=False):
        super(TextBlock, self).__init__(display, page)
        self.font = display.fonts.normal
        self.text = text
        self.is_highlighted = is_highlighted
        self.is_enabled = True

    def get_foreground(self):
        """
        Gets the calculated foreground color based on the label's attributes and the current color scheme.
        By having foreground be calculated like this, it provides a poor man's binding system where we can
        always grab the correct color from the color scheme, even when the color scheme changes.
        :return: The foreground
        """
        
        # When using custom colors, just use that
        if self.color:
            return self.color
        
        cs = self.display.color_scheme

        if not self.is_enabled:
            return cs.disabled

        if self.is_highlighted:
            return cs.highlight
        else:
            return cs.foreground

    def arrange(self):

        effective_text = self.get_effective_text()

        self.desired_size = self.font.measure(effective_text)

        return super(TextBlock, self).arrange()

    def get_effective_text(self):

        # Do string formatting as needed
        if isinstance(self.text, unicode):
            effective_text = self.text
        else:
            effective_text = str(self.text)

        try:
            if self.text is not None:

                if isinstance(self.text, str) or isinstance(self.text, unicode):
                    if isinstance(self.text_data, tuple):
                        effective_text = self.text.format(*self.text_data)
                    else:
                        effective_text = self.text.format(self.text_data)
        except:
            effective_text = str(self.text)

        return effective_text

    def render(self):
        """
        Renders the textblock to the default surface using the current properties of this object
        :rtype : RectType
        """

        self.left = self.pos[0]
        self.top = self.pos[1]

        effective_text = self.get_effective_text()

        if self.font is not None and effective_text is not None:
            color = self.get_foreground()
            self.rect = render_text(self.display, self.font, effective_text, self.pos[0], self.pos[1], color)
        else:
            self.rect = Rect(self.left, self.top, 0, 0)

        return self.set_dimensions_from_rect(self.rect)
