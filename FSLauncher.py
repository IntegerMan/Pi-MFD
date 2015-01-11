from PiMFD import MFDAppOptions
from PiMFD.DisplayManager import DisplayManager

__author__ = 'Matt Eland'

log = open("PiMFD.log", "w")
try:
    app_options = MFDAppOptions()

    # Create a new display in fullscreen mode without specifying resolution. Resolution will be auto-detected.
    display = DisplayManager(None, None)
    display.is_fullscreen = True

    # Launch!
    display.start_mfd(app_options)

except Exception as e:
    error_message = "Unhandled error {0}\n".format(str(e))

    print(error_message)
    log.write(error_message)

finally:
    log.close()
    pass
