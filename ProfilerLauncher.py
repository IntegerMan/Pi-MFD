# coding=utf-8
"""
A windowed-mode entry point for Pi-MFD with Profiling active
"""
import pstats
import traceback
import cProfile

from PiMFD.Options import MFDAppOptions
from PiMFD.UI.DisplayManager import DisplayManager


__author__ = 'Matt Eland'


def launch_app():
    log = open("PiMFD.log", "w")

    try:
        # Initialize our settings. This will create a default settings file if none exists
        app_options = MFDAppOptions()
        app_options.load_from_settings()
        app_options.save_to_settings()
        app_options.lat, app_options.lng = 28.4012277, -81.2076703

        # Build a display using the standard windowed sizes. This is great for desktop testing.
        display = DisplayManager()
        display.is_fullscreen = False

        # Launch
        display.start_mfd(app_options)

    except:
        error_message = "Unhandled error {0}\n".format(str(traceback.format_exc()))

        print(error_message)
        log.write(error_message)

    finally:
        log.close()
        pass


filename = 'performance.cprof'
cProfile.run('launch_app()', filename=filename)
stream = open('performance.txt', 'w')
stats = pstats.Stats(filename, stream=stream)
stats.sort_stats('time').print_stats()
stream.close()