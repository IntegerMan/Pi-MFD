__author__ = 'Matt Eland'


from PiMFD import *


app_options = MFDAppOptions()
app_options.font_name = None

# Create a new display in fullscreen mode without specifying resolution. Resolution will be auto-detected.
display = DisplaySettings(None, None)
display.is_fullscreen = True

# Launch!
display.start_mfd(app_options)
