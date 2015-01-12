import pygame

__author__ = 'Matt Eland'


class MFDButton(object):

    text = None
    enabled = True
    selected = False

    def __init__(self, text, selected=False, enabled=True):
        self.text = text
        self.selected = selected
        self.enabled = enabled

    def render(self, display, x, is_top):

        # Figure out where we're starting vertically
        y = display.padding_y
        if not is_top:
            y = display.res_y - display.padding_y - display.font_size_normal

        font_color = display.color_scheme.foreground
        background = None

        label = self.text

        # If it's selected, use inverted colors
        if self.selected:
            font_color = display.color_scheme.background
            background = display.color_scheme.foreground
            label = ' ' + label + ' '  # Pad out the display so it appears wider with a background

        pos = display.render_text(display.font_normal, label, x, y, font_color, background=background)

        line_length = 5

        # TODO: This shouldn't have to know anything about pygame. Abstract that to display.
        if is_top:
            pygame.draw.line(display.surface, display.color_scheme.foreground, (x + (pos.width / 2), y - 2),
                             (x + (pos.width / 2), y - 2 - line_length))
        else:
            pygame.draw.line(display.surface, display.color_scheme.foreground, (x + (pos.width / 2), y + pos.height),
                             (x + (pos.width / 2), y + pos.height + line_length))


