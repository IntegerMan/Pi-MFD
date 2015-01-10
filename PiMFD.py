__author__ = 'Matt Eland'

from TextUtilities import *
from PygameHelpers import *


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
                pygame.draw.line(display, font_color, (x + (pos.width / 2), y - 2), (x + (pos.width / 2), y - 2 - abs(line_offset)))
            elif line_offset > 0:
                pygame.draw.line(display, font_color, (x + (pos.width / 2), y + pos.height), (x + (pos.width / 2), y + pos.height + line_offset))

            x_offset += header_offset


def start_mfd():

    # App Info
    app_name = 'Pi MFD'
    app_version = '0.01 Development Version'

    # Display Constants
    res_x = 800
    res_y = 480
    padding_x = 0
    padding_y = 8

    # Start up PyGame
    lcd = init_pygame_graphics(res_x, res_y, app_name)

    # Set up Font
    font_size = 24
    font = build_font(font_size)
    color_white = (255, 255, 255)
    color_black = (0, 0, 0)
    color_green = (0, 255, 0)

    # Standard Timer
    clock = pygame.time.Clock()
    frames_per_second = 30

    # Main Processing Loop
    keep_rendering = True
    while keep_rendering:

        # Fill the background with black
        lcd.fill(color_black)

        # Draw our App Headers
        top_headers = ('[SCH]', 'PRG', 'GAM', 'SOC', 'SYS')
        btm_headers = ('TASK', 'MAIL', 'CAL', 'NAV', 'FOR')
        render_headers(lcd, font, color_green, top_headers, padding_x, res_x - padding_x, padding_y, line_offset=-5)
        render_headers(lcd, font, color_green, btm_headers, padding_x, res_x - padding_x, res_y - font_size, line_offset=5)

        center_rect = render_text_centered(lcd, font, app_name + ' ' + app_version, res_x / 2, (res_y / 2) - (font_size / 2), color_white)
        render_text_centered(lcd, font, 'Systems Test', res_x / 2, center_rect.top + font_size + padding_y, color_white)

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
