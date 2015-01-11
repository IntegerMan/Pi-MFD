import pygame
from PiMFD.Pages.MFDPage import MFDRootPage
from PiMFD.Button import MFDButton

__author__ = 'Matt Eland'


class MFDController(object):

    display = None
    continue_executing = True
    clock = None

    active_page = None
    active_app = None

    applications = list()

    def __init__(self, display, app_options):

        self.display = display
        self.clock = pygame.time.Clock()

        if app_options is not None:
            self.app_name = app_options.app_name
            self.app_version = app_options.app_version

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

        # Ask the current application for available buttons
        if self.active_app is not None:
            bottom_buttons = self.active_app.get_buttons()
            page.bottom_headers = bottom_buttons
        else:
            # Perhaps this will need to ask the current page for options in this case, but for now, just go empty
            page.bottom_headers = list()

    def execute_main_loop(self):

        # Fill the background with black
        self.display.surface.fill(self.display.color_scheme.background)

        # Ensure a page is selected
        if self.active_page is None:
            if self.active_app is None:
                self.active_page = MFDRootPage(self)
            else:
                self.active_page = self.active_app.get_default_page()

        # Update the headers
        self.update_application()

        # Render the current page
        self.active_page.render(self.display)

        # Handle input, allow user to close window / exit / control the app
        self.process_events()

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        self.clock.tick(self.display.frames_per_second)

        pass
