__author__ = 'Matt Eland'


from PiMFD import *

log = open("PiMFD.log", "w")

try:
    app_options = MFDAppOptions()

    # Create a new display in fullscreen mode without specifying resolution. Resolution will be auto-detected.
    display = DisplaySettings(None, None)
    display.is_fullscreen = True

    # Launch!
    display.start_mfd(app_options)

except Exception as e:     # most generic exception you can catch
    log.write("Unhandled error {0}\n".format(str(e)))

finally:
    log.close()
    pass
