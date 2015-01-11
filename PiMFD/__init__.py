from PiMFD.ColorScheme import ColorSchemes
from PiMFD.MFDButton import MFDButton
from PiMFD.Pages.MFDPage import MFDRootPage
from PiMFD.Pages.SystemPages import SysClockPage

from PiMFD.PygameHelpers import *


__author__ = 'Matt Eland'


class MFDAppOptions(object):
    app_name = 'Pi-MFD'
    app_version = '0.01 Development Version'
    font_name = 'Fonts/VeraMono.ttf'
    display = None


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
        page.top_headers.append(MFDButton("SCH"))
        page.top_headers.append(MFDButton("NAV"))
        page.top_headers.append(MFDButton("SOC"))
        page.top_headers.append(MFDButton("MED"))
        page.top_headers.append(MFDButton("SYS", selected=True))

        page.bottom_headers = list()
        page.bottom_headers.append(MFDButton('TIME', selected=True))
        page.bottom_headers.append(MFDButton('PERF'))
        page.bottom_headers.append(MFDButton('NET'))
        page.bottom_headers.append(MFDButton('OPTS'))
        page.bottom_headers.append(MFDButton('EXIT'))


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
