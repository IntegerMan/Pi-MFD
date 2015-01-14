import pygame
from PiMFD.Applications.ScheduleApplication import ScheduleApp
from PiMFD.Pages.MFDPage import SimpleMessagePage
from PiMFD.Button import MFDButton
from PiMFD.Applications.SystemApplication import SysApplication
from PiMFD.Applications.Application import PlaceholderApp

__author__ = 'Matt Eland'


class MFDController(object):

    display = None
    requested_exit = False
    clock = None

    app_author = 'Matt Eland'
    copyright_year = 2015

    active_app = None

    top_headers = list()
    bottom_headers = list()

    max_app_buttons = 5
    max_page_buttons = 5

    # TODO: Grab location from GPS
    # TODO: Allow user to manually set location
    location = '43035'

    time_format = '%m/%d/%Y - %H:%M:%S'

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
            self.app_author = app_options.app_author
            self.copyright_year = app_options.copyright_year

        # Placeholders for navigation app
        self.nav_app = PlaceholderApp(self, 'NAV')
        self.nav_app.pages.append(SimpleMessagePage(self, self.nav_app, 'MAP'))
        self.nav_app.pages.append(SimpleMessagePage(self, self.nav_app, 'GAS'))
        self.nav_app.pages.append(SimpleMessagePage(self, self.nav_app, 'FOOD'))
        self.nav_app.pages.append(SimpleMessagePage(self, self.nav_app, 'TRAF'))
        self.nav_app.pages.append(SimpleMessagePage(self, self.nav_app, 'COND'))

        # Scheduling App
        self.sch_app = ScheduleApp(self)

        # Placeholders for media app
        self.med_app = PlaceholderApp(self, 'MED')
        self.med_app.pages.append(SimpleMessagePage(self, self.med_app, 'IMG'))
        self.med_app.pages.append(SimpleMessagePage(self, self.med_app, 'PAND'))
        self.med_app.pages.append(SimpleMessagePage(self, self.med_app, 'TUBE'))
        self.med_app.pages.append(SimpleMessagePage(self, self.med_app, 'FLIX'))
        self.med_app.pages.append(SimpleMessagePage(self, self.med_app, 'AZIW'))

        # Placeholders for social app
        self.soc_app = PlaceholderApp(self, 'SOCL')
        self.soc_app.pages.append(SimpleMessagePage(self, self.soc_app, 'NEWS'))
        self.soc_app.pages.append(SimpleMessagePage(self, self.soc_app, 'FACE'))
        self.soc_app.pages.append(SimpleMessagePage(self, self.soc_app, 'TWTR'))
        self.soc_app.pages.append(SimpleMessagePage(self, self.soc_app, 'RSS'))
        self.soc_app.pages.append(SimpleMessagePage(self, self.soc_app, 'WEB'))

        self.sys_app = SysApplication(self)

        self.applications = list([self.sys_app, self.nav_app, self.sch_app, self.med_app, self.soc_app])
        
        self.active_app = self.sys_app

    def process_events(self):

        # Process all events
        events = pygame.event.get()
        for event in events:

            # Check for Window Close
            if event.type == pygame.QUIT:
                self.requested_exit = True

            # Respond to screen size changes
            # TODO: It'd be nice to be able to enforce a minimum width / height - we don't support watch-sized resolutions yet
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.display.res_x = event.dict['size'][0]
                self.display.res_y = event.dict['size'][1]
                pygame.display.update()

            # Check for Keyboard Input
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:  # Handle escape by closing the app.
                    self.requested_exit = True
                elif event.key == pygame.K_F1:    # Simulate Hardware Upper Button 1
                    self.handle_button(0, True)
                elif event.key == pygame.K_F2:    # Simulate Hardware Upper Button 2
                    self.handle_button(1, True)
                elif event.key == pygame.K_F3:    # Simulate Hardware Upper Button 3
                    self.handle_button(2, True)
                elif event.key == pygame.K_F4:    # Simulate Hardware Upper Button 4
                    self.handle_button(3, True)
                elif event.key == pygame.K_F5:    # Simulate Hardware Upper Button 5
                    self.handle_button(4, True)
                elif event.key == pygame.K_F6:    # Simulate Hardware Upper Special Button (reserved for future)
                    pass
                elif event.key == pygame.K_F7:    # Simulate Hardware Lower Special Button (reserved for future)
                    pass
                elif event.key == pygame.K_F8:    # Simulate Hardware Lower Button 1
                    self.handle_button(0, False)
                elif event.key == pygame.K_F9:    # Simulate Hardware Lower Button 2
                    self.handle_button(1, False)
                elif event.key == pygame.K_F10:   # Simulate Hardware Lower Button 3
                    self.handle_button(2, False)
                elif event.key == pygame.K_F11:   # Simulate Hardware Lower Button 4
                    self.handle_button(3, False)
                elif event.key == pygame.K_F12:   # Simulate Hardware Lower Button 5
                    self.handle_button(4, False)

    def render_button_row(self, headers, is_top):

        start_x = self.display.padding_x
        end_x = self.display.res_x - self.display.padding_x

        # Do division up front
        header_offset = (end_x - start_x) / self.max_app_buttons
        half_offset = (header_offset / 2.0)

        # Render from left to right
        x_offset = 0
        for header in headers[0:self.max_app_buttons]:  # TODO: Support > max_app_buttons apps by allowing paging
            x = start_x + x_offset + half_offset
            header.render(self.display, x, is_top)
            x_offset += header_offset

    def render_button_rows(self):
        self.render_button_row(self.top_headers, True)
        self.render_button_row(self.bottom_headers, False)

    def update_application(self):

        # Render our applications
        self.top_headers = list()
        for app in self.applications:
            self.top_headers.append(MFDButton(app.get_button_text(), selected=(app is self.active_app and app is not None)))

        # Ask the current application for available buttons
        if self.active_app is not None:

            self.bottom_headers = self.active_app.get_buttons()

        else:
            # Perhaps this will need to ask the current page for options in this case, but for now, just go empty
            self.bottom_headers = list()

    def execute_main_loop(self):

        self.display.render_background()

        # Ensure an app is selected
        if self.active_app is None:
            self.active_app = self.sys_app

        # Ensure a page is selected
        if self.active_app.active_page is None:
            self.active_app.active_page = self.active_app.get_default_page()

        # Update the headers
        self.update_application()
        self.render_button_rows()

        # Render the current page
        if self.active_app is not None and self.active_app.active_page is not None:
            # let the page speak for itself
            self.active_app.active_page.render(self.display)
        else:
            # No content defined for the app. Render a not implemented message
            SimpleMessagePage(self, self.active_app, 'N/A').render(self.display)

        # Handle input, allow user to close window / exit / control the app
        self.process_events()

        # Update the UI and give a bit of time before going again
        pygame.display.update()
        self.clock.tick(self.display.frames_per_second)

        pass

    def handle_button(self, index, is_top_row):

        # TODO: Render this as a click by bordering the clickable area in a special color

        # Pass on the selection command to the owner
        if is_top_row:
            self.select_app_by_index(index)
        elif self.active_app is not None:
            self.active_app.select_page_by_index(index)

    def select_app_by_index(self, index):

        # Figure out where we're going
        if index < len(self.applications):
            new_app = self.applications[index]
        else:
            new_app = None

        self.select_app(new_app)

    def select_app(self, new_app):

        # Don't allow users to select blank spots
        if new_app is None:
            return

        if new_app is self.active_app:

            # We just reselected the current app. Some apps will want to handle that specially.
            self.active_app.handle_reselected()

        else:

            # Tell our old app it's going to sleep
            if self.active_app is not None:
                self.active_app.handle_unselected()

            # Tell the new app it's now selected
            self.active_app = new_app
            new_app.handle_selected()