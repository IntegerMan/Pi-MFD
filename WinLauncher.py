__author__ = 'Matt Eland'


from PiMFD import *


app_options = MFDAppOptions()

# Build a display using the standard windowed sizes. This is great for desktop testing.
display = DisplaySettings()
display.is_fullscreen = False

# Launch
display.start_mfd(app_options)