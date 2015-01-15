__author__ = 'Matt Eland'


class MFDButton(object):

    text = None
    enabled = True
    selected = False

    def __init__(self, text, selected=False, enabled=True):
        self.text = text
        self.selected = selected
        self.enabled = enabled

    def render(self, display, x_start, x_end, is_top):

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

        midpoint = ((x_end - x_start) / 2) + x_start

        pos = display.render_text_centered(display.font_normal, label, midpoint, y, font_color, background=background)

        # Render tick marks
        line_length = 5
        if is_top:
            display.draw_vertical_line(display.color_scheme.foreground, midpoint, y - 2, y - 2 - line_length)
        else:
            display.draw_vertical_line(display.color_scheme.foreground, midpoint, y + pos.height - 2, y + pos.height + line_length - 2)



