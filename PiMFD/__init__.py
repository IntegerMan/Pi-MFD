# coding=utf-8
import pygame

from PiMFD.Applications.System.SystemApplication import SysApplication
from PiMFD.Controller import MFDController
from PiMFD.Applications.System.SystemPages import SysClockPage


__author__ = 'Matt Eland'


def start_mfd(display, app_options):
    """
    Initializes Pi-MFD and starts the main execution loop.
    :type display: PiMFD.DisplayManager.DisplayManager The DisplayManager that runs the graphical settings
    :type app_options: PiMFD.MFDAppOptions Options for the application
    """

    # Start up the graphics engine
    display.init_graphics(app_options)

    # Initialize the controller
    controller = MFDController(display, app_options)

    # Main Processing Loop
    while not controller.requested_exit:
        controller.execute_main_loop()

    # Shutdown things that require it
    pygame.quit()