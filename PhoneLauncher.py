# coding=utf-8
"""
A windowed-mode entry point for Pi-MFD
"""
import traceback

from PiMFD.Options import MFDAppOptions
from PiMFD.UI.DisplayManager import DisplayManager


__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")

try:
    # Initialize our settings. This will create a default settings file if none exists
    app_options = MFDAppOptions()
    app_options.load_from_settings()
    app_options.save_to_settings()

    # Build a display using the standard windowed sizes. This is great for desktop testing.
    display = DisplayManager()
    display.res_x = 480
    display.res_y = 320
    display.allow_resize = False
    display.is_fullscreen = False  # TODO: Once this is more developed, this should probably be True

    # Launch
    display.start_mfd(app_options)

except Exception as e:

    error_message = "Unhandled error {0}\n".format(str(traceback.format_exc()))

    print(error_message)
    log.write(error_message)

finally:
    log.close()
    pass