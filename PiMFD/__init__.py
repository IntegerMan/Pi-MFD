from PiMFD.Applications.SystemApplication import SysApplication
from PiMFD.Controller import MFDController
from PiMFD.Pages.SystemPages import SysClockPage
from PiMFD.PygameHelpers import init_pygame_graphics

__author__ = 'Matt Eland'


class MFDAppOptions(object):
    app_name = 'Pi-MFD'
    app_version = '0.01 Development Version'
    font_name = 'Fonts/VeraMono.ttf'
    display = None


def start_mfd(display, app_options):

    # Start up the graphics engine
    init_pygame_graphics(display, app_options.app_name, app_options.font_name)

    # Initialize the controller
    controller = MFDController(display, app_options)
    controller.active_app = SysApplication(controller)
    controller.active_page = SysClockPage(controller)

    # Main Processing Loop
    while controller.continue_executing:
        controller.execute_main_loop()