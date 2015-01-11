from PiMFD import MFDAppOptions
from PiMFD.DisplayManager import DisplayManager

__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")

try:
    app_options = MFDAppOptions()

    # Build a display using the standard windowed sizes. This is great for desktop testing.
    display = DisplayManager()
    display.is_fullscreen = False

    # Launch
    display.start_mfd(app_options)

except Exception as e:

    error_message = "Unhandled error {0}\n".format(str(e))

    print(error_message)
    log.write(error_message)

finally:
    log.close()
    pass