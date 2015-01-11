__author__ = 'Matt Eland'


from PiMFD import *

log = open("PiMFD.log", "w")

try:
    app_options = MFDAppOptions()

    # Build a display using the standard windowed sizes. This is great for desktop testing.
    display = DisplaySettings()
    display.is_fullscreen = False

    # Launch
    display.start_mfd(app_options)

except Exception as e:     # most generic exception you can catch
    log.write("Unhandled error {0}\n".format(str(e)))

finally:
    log.close()
    pass