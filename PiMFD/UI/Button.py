# coding=utf-8
"""
UI Button related functionality
"""

from pygame.rect import Rect

from PiMFD.UI.Rendering import draw_vertical_line, draw_rectangle, render_text_centered


__author__ = 'Matt Eland'


class MFDButton(object):
    """
    Represents a UI button at the edge of the screen and controls the rendering and mouse collision detection of that
    button given its current text, enabled, and selected state.
    """

    text = None
    enabled = True
    selected = False
    always_render_background = False

    def __init__(self, text, selected=False, enabled=True):
        self.bounds = Rect(-1, -1, -1, -1)
        self.text = text
        self.selected = selected
        self.enabled = enabled
        self.draw_border = False

    def render(self, display, x_start, x_end, is_top):
        """
        Renders the button with its current state.
        :type display: The PiMFD.DisplayManager.DisplayManager that manages display settings
        :param x_start: The leftmost side of the button's bounds
        :param x_end: The rightmost side of the button's bounds
        :type is_top: bool True if this button is on the top of the screen, False if on the bottom.
        """

        # Figure out where we're starting vertically
        y = display.padding_y
        if not is_top:
            y = display.res_y - display.padding_y - display.fonts.normal.size

        font_color = display.color_scheme.foreground

        # Figure out background color - sometimes we'll want to render it on top of other content
        background = None
        if self.always_render_background:
            background = display.color_scheme.background

        label = self.text

        # If it's selected, use inverted colors
        if self.selected:
            font_color = display.color_scheme.background
            background = display.color_scheme.foreground
            label = ' ' + label + ' '  # Pad out the display so it appears wider with a background

        midpoint = ((x_end - x_start) / 2) + x_start

        pos = render_text_centered(display, display.fonts.normal, label, midpoint, y, font_color, background=background)

        # Render tick marks
        line_length = 5
        if is_top:
            draw_vertical_line(display,
                               display.color_scheme.foreground,
                               midpoint,
                               y - 2,
                               y - 2 - line_length)

            top = y - 2 - line_length
            bottom = pos.bottom
        else:
            draw_vertical_line(display,
                               display.color_scheme.foreground,
                               midpoint,
                               y + pos.height - 2,
                               y + pos.height + line_length - 2)

            top = pos.top
            bottom = y + pos.height + line_length - 2

        # Update the bounds of the button for collision detection later
        self.bounds = Rect(x_start, top, x_end - x_start, bottom - top)

        # Render the bounds of the rectangle
        if self.draw_border:
            draw_rectangle(display, display.color_scheme.foreground, self.bounds)

    def contains_point(self, pos):
        """
        Determines whether the bounds of this button contains the specified point. Bounds are defined as a general area
        represented by the button and not just rendered content.
        :param pos: The point to test
        :return: True if pos is inside the bounds of this button, otherwise False.
        """
        return self.bounds.collidepoint(pos)
