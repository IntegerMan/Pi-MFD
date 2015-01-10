from TextUtilities import *
from PygameHelpers import *


__author__ = 'Matt Eland'


class ColorScheme:

    def __init__(self, background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255)):
        self.background = background
        self.foreground = foreground
        self.highlight = highlight
        pass

    def clone_to(self, target):
        target.background = self.background
        target.foreground = self.foreground
        target.highlight = self.highlight
        return target

    background = (0, 0, 0)
    foreground = (0, 255, 0)
    highlight = (255, 255, 255)

    pass


class ColorSchemes:

    def __init__(self):
        pass

    # A green based color scheme resembling military avionics displays
    military = ColorScheme(background=(0, 0, 0), foreground=(0, 255, 0), highlight=(255, 255, 255))

    # A cyan display
    cyan = ColorScheme(background=(0, 0, 32), foreground=(0, 255, 255), highlight=(0, 0, 255))

    pass


class DisplaySettings:
    """Contains information related to the drawing dimensions of the application window as well as the drawing surface."""

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        pass

    def start_mfd(self):
        start_mfd(self)

    res_x = 800
    res_y = 480
    padding_x = 0
    padding_y = 8
    surface = None
    is_fullscreen = True
    color_scheme = ColorSchemes.military
    pass


def render_headers(display, font, font_color, headers, start_x, end_x, y, line_offset=0):

    num_headers = len(headers)
    if num_headers > 0:

        # Do division up front
        header_offset = (end_x - start_x) / num_headers
        half_offset = (header_offset / 2.0)

        # Render from left to right
        x_offset = 0
        for header in headers:
            x = start_x + x_offset + half_offset
            pos = render_text(display, font, header, x, y, font_color)
            if line_offset < 0:
                pygame.draw.line(display.surface, font_color, (x + (pos.width / 2), y - 2), (x + (pos.width / 2), y - 2 - abs(line_offset)))
            elif line_offset > 0:
                pygame.draw.line(display.surface, font_color, (x + (pos.width / 2), y + pos.height), (x + (pos.width / 2), y + pos.height + line_offset))

            x_offset += header_offset


def start_mfd(display):

    # App Info
    app_name = 'Pi MFD'
    app_version = '0.01 Development Version'

    # Start up PyGame
    init_pygame_graphics(display, app_name)

    # Set up Font
    font_size = 24
    font = build_font(font_size)

    # Standard Timer
    clock = pygame.time.Clock()
    frames_per_second = 30

    # Main Processing Loop
    keep_rendering = True
    while keep_rendering:

        # Fill the background with black
        display.surface.fill(display.color_scheme.background)

        # Draw our App Headers
        top_headers = ('[SCH]', 'PRG', 'GAM', 'SOC', 'SYS')
        btm_headers = ('TASK', 'MAIL', 'CAL', 'NAV', 'FOR')
        render_headers(display, font, display.color_scheme.foreground, top_headers, display.padding_x, display.res_x - display.padding_x, display.padding_y, line_offset=-5)
        render_headers(display, font, display.color_scheme.foreground, btm_headers, display.padding_x, display.res_x - display.padding_x, display.res_y - font_size, line_offset=5)

        center_rect = render_text_centered(display, font, app_name + ' ' + app_version, display.res_x / 2, (display.res_y / 2) - (font_size / 2), display.color_scheme.highlight)
        render_text_centered(display, font, 'Systems Test', display.res_x / 2, center_rect.top + font_size + display.padding_y, display.color_scheme.highlight)

        # Process all events
        events = pygame.event.get()
        for event in events:

            # Check for Window Close
            if event.type == pygame.QUIT:
                keep_rendering = False

            # Check for Keyboard Input
            if event.type == pygame.KEYDOWN:

                # Handle escape by closing the app.
                if event.key == pygame.K_ESCAPE:
                    keep_rendering = False

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        clock.tick(frames_per_second)
