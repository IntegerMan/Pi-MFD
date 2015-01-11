from PiMFD.ColorScheme import ColorSchemes
from PiMFD.Pages.MFDPage import MFDRootPage
from PiMFD.Pages.SystemPages import SysClockPage

from PiMFD.PygameHelpers import *


__author__ = 'Matt Eland'


class MFDAppOptions(object):
    app_name = 'Pi-MFD'
    app_version = '0.01 Development Version'
    font_name = 'Fonts/VeraMono.ttf'
    display = None


class DisplayManager(object):
    """Contains information and functions related to the drawing dimensions of the application window as well as the drawing surface."""

    def __init__(self, x=800, y=480):
        self.res_x = x
        self.res_y = y
        pass

    def start_mfd(self, app_options):
        start_mfd(self, app_options)

    res_x = 800
    res_y = 480

    padding_x = 8
    padding_y = 8

    surface = None

    is_fullscreen = False

    frames_per_second = 30

    color_scheme = ColorSchemes.military

    font_size_normal = 24
    font_normal = None

    def get_content_start_y(self):
        return (self.padding_y * 2) + self.font_size_normal

    pass

    def render_text(self, font, text, left, top, color, background=None):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(top=top, left=left)

        if background is not None:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect

    def render_text_centered(self, font, text, left, top, color, background=None):
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(left, top))

        if background is not None:
            self.surface.fill(background, rect=rect)

        self.surface.blit(text_surface, rect)
        return rect


class MFDController(object):

    display = None
    active_page = None
    continue_executing = True

    def __init__(self, display):
        self.display = display

    def process_events(self):
        # Process all events
        events = pygame.event.get()
        for event in events:

            # Check for Window Close
            if event.type == pygame.QUIT:
                self.continue_executing = False

            # Check for Keyboard Input
            if event.type == pygame.KEYDOWN:

                # Handle escape by closing the app.
                if event.key == pygame.K_ESCAPE:
                    self.continue_executing = False

    def update_application(self):

        page = self.active_page

        page.top_headers = list()
        page.top_headers.append(MFDButton("SCH", selected=True))
        page.top_headers.append(MFDButton("PRG"))
        page.top_headers.append(MFDButton("GAM"))
        page.top_headers.append(MFDButton("SOC"))
        page.top_headers.append(MFDButton("SYS"))

        page.bottom_headers = list()
        page.bottom_headers.append(MFDButton('TASK'))
        page.bottom_headers.append(MFDButton('MAIL'))
        page.bottom_headers.append(MFDButton('CAL'))
        page.bottom_headers.append(MFDButton('NAV'))
        page.bottom_headers.append(MFDButton('WTHR'))


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

        # If it's selected, use a different color and surround with brackets
        if self.selected:
            font_color = display.color_scheme.background
            background = display.color_scheme.foreground
            label = '[' + label + ']'

        pos = display.render_text(display.font_normal, label, x, y, font_color, background=background)

        line_length = 5

        if is_top:
            pygame.draw.line(display.surface, display.color_scheme.foreground, (x + (pos.width / 2), y - 2),
                             (x + (pos.width / 2), y - 2 - line_length))
        else:
            pygame.draw.line(display.surface, display.color_scheme.foreground, (x + (pos.width / 2), y + pos.height),
                             (x + (pos.width / 2), y + pos.height + line_length))


def start_mfd(display, app_options):

    # TODO: This should not need to know anything about pygame

    # Start up the graphics engine
    init_pygame_graphics(display, app_options.app_name, app_options.font_name)

    # Standard Timer
    clock = pygame.time.Clock()

    # Initialize the controller
    controller = MFDController(display)
    controller.app_name = app_options.app_name
    controller.app_version = app_options.app_version

    controller.active_page = SysClockPage(controller)

    # Main Processing Loop
    while controller.continue_executing:

        # Fill the background with black
        display.surface.fill(display.color_scheme.background)

        # Ensure a page is selected
        if controller.active_page is None:
            controller.active_page = MFDRootPage(controller)

        # Update the headers
        controller.update_application()

        # Render the current page
        controller.active_page.render(display)

        # Handle input, allow user to close window / exit / control the app
        controller.process_events()

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        clock.tick(display.frames_per_second)
