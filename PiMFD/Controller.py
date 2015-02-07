# coding=utf-8

"""
Contains application control logic for Pi-MFD.
"""

import pygame

from PiMFD.Applications.Navigation.NavigationApplication import NavigationApp
from PiMFD.Applications.Scheduling.ScheduleApplication import ScheduleApp
from PiMFD.Applications.MFDPage import SimpleMessagePage
from PiMFD.Options import MFDAppOptions
from PiMFD.UI import Keycodes
from PiMFD.UI.Button import MFDButton
from PiMFD.Applications.System.SystemApplication import SysApplication


__author__ = 'Matt Eland'


class MFDController(object):
    """
    The MFDController coordinates between the various applications and pages and determines what actions and
    navigation should occur in response to apps, pages, and user input.
    :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager used to render the user interface
    :type app_options: PiMFD.MFDAppOptions Application options
    """
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

    button_sound = None
    keypress_sound = None

    time_format = '%m/%d/%Y - %H:%M:%S'

    sys_app = None
    sch_app = None
    nav_app = None
    med_app = None
    soc_app = None

    applications = list()

    def __init__(self, display, app_options):

        """
        :type app_options: PiMFD.Options.MFDAppOptions
        :type display: PiMFD.UI.DisplayManager.DisplayManager
        """
        self.display = display

        if app_options is not None:
            self.options = app_options
        else:
            self.options = MFDAppOptions()

        # Navigation app
        self.nav_app = NavigationApp(self)

        # Scheduling App
        self.sch_app = ScheduleApp(self)

        # Set up the sound effect for button presses
        if self.options.button_sound:
            self.button_sound = pygame.mixer.Sound(self.options.button_sound)
        if self.options.key_sound:
            self.keypress_sound = pygame.mixer.Sound(self.options.key_sound)

        self.sys_app = SysApplication(self)

        self.applications = list([self.sys_app, self.nav_app, self.sch_app])
        
        self.active_app = self.sys_app

    def process_events(self):
        """
        Processes events such as keyboard, mouse, and hardware input as well as external events such as window resize
        or application closing notifications.
        """

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
                self.display.update_graphics_mode()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left Mouse Button
                    self.handle_mouse_left_click(event.pos)

            elif event.type == pygame.KEYDOWN:
                self.handle_keyboard_event(event.key)

    def get_active_page(self):
        """
        Returns the active page or None if no page is active
        :return: The active page or None if no page is active
        """
        if self.active_app is not None:
            return self.active_app.active_page
        else:
            return None

    def handle_keyboard_event(self, key):
        """
        Processes keyboard input
        :param key: The keyboard data
        """
        active_page = self.get_active_page()

        if key == Keycodes.KEY_ESCAPE:  # Handle escape by closing the app.
            self.requested_exit = True
        elif key == Keycodes.KEY_F1:  # Simulate Hardware Upper Button 1
            self.handle_button(0, True)
        elif key == Keycodes.KEY_F2:  # Simulate Hardware Upper Button 2
            self.handle_button(1, True)
        elif key == Keycodes.KEY_F3:  # Simulate Hardware Upper Button 3
            self.handle_button(2, True)
        elif key == Keycodes.KEY_F4:  # Simulate Hardware Upper Button 4
            self.handle_button(3, True)
        elif key == Keycodes.KEY_F5:  # Simulate Hardware Upper Button 5
            self.handle_button(4, True)
        elif key == Keycodes.KEY_F6:  # Simulate Hardware Upper Special Button (reserved for future)
            pass
        elif key == Keycodes.KEY_F7:  # Simulate Hardware Lower Special Button (reserved for future)
            pass
        elif key == Keycodes.KEY_F8:  # Simulate Hardware Lower Button 1
            self.handle_button(0, False)
        elif key == Keycodes.KEY_F9:  # Simulate Hardware Lower Button 2
            self.handle_button(1, False)
        elif key == Keycodes.KEY_F10:  # Simulate Hardware Lower Button 3
            self.handle_button(2, False)
        elif key == Keycodes.KEY_F11:  # Simulate Hardware Lower Button 4
            self.handle_button(3, False)
        elif key == Keycodes.KEY_F12:  # Simulate Hardware Lower Button 5
            self.handle_button(4, False)
        elif active_page:
            active_page.handle_key(key)

    def render_button_row(self, headers, is_top):
        """
        Renders a row of buttons.
        :type headers: list The buttons to render
        :type is_top: bool True if this is the top row, False for the bottom row
        """
        # Do division up front
        header_offset = self.display.res_x / float(self.max_app_buttons)

        # Render from left to right
        x_offset = 0
        for header in headers[0:self.max_app_buttons]:  # TODO: Support > max_app_buttons apps by allowing paging
            x = x_offset
            if header:
                header.render(self.display, x, x + header_offset, is_top)
            x_offset += header_offset

    def render_button_rows(self):
        """
        Renders the top and bottom rows of buttons
        """
        self.render_button_row(self.top_headers, True)
        self.render_button_row(self.bottom_headers, False)

    def update_application(self):
        """
        Causes the applications to regenerate their list of buttons (as needed)
        """

        # TODO: This really should not be instantiating new button objects every render cycle. Those should live at the
        # app-level

        always_render_background = self.active_app and self.active_app.always_render_background

        # Render our applications
        self.top_headers = list()
        for app in self.applications:
            button = MFDButton(app.get_button_text(), selected=(app is self.active_app and app is not None))
            button.always_render_background = always_render_background
            self.top_headers.append(button)

        # Ask the current application for available buttons
        if self.active_app is not None:
            self.bottom_headers = self.active_app.get_buttons()

            for button in self.bottom_headers:
                if button:
                    button.always_render_background = always_render_background

        else:
            # Perhaps this will need to ask the current page for options in this case, but for now, just go empty
            self.bottom_headers = list()

    def execute_main_loop(self):
        """
        The main processing loop of the system. Renders the current page, ensures events are responded to, and
        coordinates with the graphics engine to maintain proper display frame rates.
        """

        # Renders the background of the application
        self.display.render_background()

        # Ensure an app is selected
        if self.active_app is None:
            self.active_app = self.sys_app

        # Ensure a page is selected
        if self.active_app.active_page is None:
            self.active_app.active_page = self.active_app.get_default_page()

        # Update the headers
        self.update_application()

        # Render the current page
        if self.active_app is not None and self.active_app.active_page is not None:
            # let the page speak for itself
            self.active_app.active_page.render()
        else:
            # No content defined for the app. Render a not implemented message
            SimpleMessagePage(self, self.active_app, 'N/A').render()

        # Render the headers on top of everything else
        self.render_button_rows()

        # Render the overlay layer
        self.display.render_overlays()

        # Handle input, allow user to close window / exit / control the app
        self.process_events()

        # Update the UI and give a bit of time before going again
        self.display.wait_for_next_frame()

        pass

    def handle_button(self, index, is_top_row):
        """
        Responds to a button click
        :type index: int The 0-based index of the button in its row.
        :type is_top_row: bool True if it was a top row button, False for a bottom row button
        """

        # TODO: Render this as a click by bordering the clickable area in a special color

        # Pass on the selection command to the owner
        if is_top_row:
            self.select_app_by_index(index)
        elif self.active_app is not None:
            self.active_app.select_page_by_index(index)

        # Play a Sound Effect for pressing the button (even if it does nothing)
        self.play_button_sound(is_app_change=is_top_row)

    def select_app_by_index(self, index):
        """
        Selects an application by its index in the list of apps.
        :type index: int The 0-based application index.
        """

        # Figure out where we're going
        if index < len(self.applications):
            new_app = self.applications[index]
        else:
            new_app = None

        self.select_app(new_app)

    def select_app(self, new_app):
        """
        Selects the specified app and tells it that it is now active, coordinating with the prior app.
        :type new_app: MFDApplication to select.
        """

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

    def handle_mouse_left_click(self, pos):
        """
        Maps mouse left clicks to clicks on any button in range
        :type pos: tuple The position where the mouse was when the click occurred
        :return: True if the click was handled, otherwise False
        """

        # Check Top Buttons and respond to the first match
        index = 0
        for button in self.top_headers:
            if button and button.enabled and button.contains_point(pos):
                self.handle_button(index, True)
                return True

            index += 1

        # Check Bottom Buttons and respond to the first match
        index = 0
        for button in self.bottom_headers:
            if button and button.enabled and button.contains_point(pos):
                self.handle_button(index, False)
                return True

            index += 1

        if self.active_app and self.active_app.handle_mouse_left_click(pos):
            return True

        # No takers
        return False

    def play_button_sound(self, is_app_change=False):
        """
        Plays a sound effect for pressing a button
        :param is_app_change: Whether the button press represents an app change
        """

        if is_app_change and self.button_sound:
            self.button_sound.play()
        elif self.keypress_sound:
            self.keypress_sound.play()

    def get_weather_data(self, zip):
        return self.sch_app.get_weather_for_zip(zip)




