__author__ = 'Matt Eland'


from PiMFD import *


app_options = MFDAppOptions()

display = DisplaySettings()
display.color_scheme = ColorSchemes.military
display.is_fullscreen = False

display.start_mfd(app_options)