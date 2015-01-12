import pygame
from PiMFD.Pages.MFDPage import MFDRootPage
from PiMFD.Button import MFDButton
from PiMFD.Applications.SystemApplication import SysApplication
from PiMFD.Applications.Application import PlaceholderApp

__author__ = 'Matt Eland'


class MFDController(object):

    display = None
    continue_executing = True
    clock = None

    active_page = None
    active_app = None

    sys_app = None
    sch_app = None
    nav_app = None
    med_app = None
    soc_app = None

    applications = list()

    def __init__(self, display, app_options):

        self.display = display
        self.clock = pygame.time.Clock()

        if app_options is not None:
            self.app_name = app_options.app_name
            self.app_version = app_options.app_version

        self.nav_app = PlaceholderApp(self, 'NAV')
        self.sch_app = PlaceholderApp(self, 'SCH')
        self.med_app = PlaceholderApp(self, 'MED')
        self.soc_app = PlaceholderApp(self, 'SCL')
        self.sys_app = SysApplication(self)

        self.applications = list([self.sys_app, self.nav_app, self.sch_app, self.med_app, self.soc_app])
        
        self.active_app = self.sys_app

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

        # Render our applications
        page.top_headers = list()
        for app in self.applications:
            page.top_headers.append(MFDButton(app.get_button_text(), selected=(app is self.active_app)))

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
