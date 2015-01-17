# coding=utf-8
"""
A windowed-mode entry point for Pi-MFD
"""
from PiMFD.Options import MFDAppOptions
from PiMFD.UI.DisplayManager import DisplayManager
from PiMFD.UI.Overlays import ScanlineOverlay, FPSOverlay

__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")

try:
    # Initialize our settings. This will create a default settings file if none exists
    app_options = MFDAppOptions()
    app_options.load_from_settings()
    app_options.save_to_settings()

    # Build a display using the standard windowed sizes. This is great for desktop testing.
    display = DisplayManager()
    display.is_fullscreen = False
    display.overlays.append(ScanlineOverlay())
    display.overlays.append(FPSOverlay())

    # Launch
    display.start_mfd(app_options)

except Exception as e:

    error_message = "Unhandled error {0}\n".format(str(e))

    print(error_message)
    log.write(error_message)

finally:
    log.close()
    pass