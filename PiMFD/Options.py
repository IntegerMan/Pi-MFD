# coding=utf-8
"""
Contains code related to application options management
"""
from ConfigParser import ConfigParser

from PiMFD.CougarMFDHandling import CougarMFDInputHandler


__author__ = 'Matt Eland'


class MFDAppOptions(object):
    """
    Contains misc. application options
    """

    version = 0.07
    app_name = 'Pi-MFD'
    app_version = '0.07 Development Version'
    app_author = 'Matt Eland'
    copyright_year = 2015
    font_name = 'Fonts/VeraMono.ttf'
    display = None
    location = '43035'
    lat = 40
    lng = -83
    enable_scan_line = True
    enable_interlacing = True
    enable_fps = True
    enable_shadow_effect = True
    button_sound = 'sounds/button.ogg'
    key_sound = 'sounds/keypress.ogg'
    map_output_file = 'map_data.xml'
    bing_maps_key = None
    color_scheme = 'Green'
    font_scaling = 8
    min_font_size = 8
    force_square_resolution = False
    mfd_controller_rotation = CougarMFDInputHandler.rotation_left
    save_map_to_disk = True
    profile = False

    def load_from_settings(self, filename='settings.ini'):
        """
        Loads settings from the default configuration file.
        :param filename: The filename to load. This file does not need to exist.
        """

        settings = ConfigParser()
        settings.read(filename)

        if 'config' in settings.sections():
            version = float(settings.get('config', 'version'))
        else:
            version = self.version

        if 'ui' in settings.sections():
            self.enable_scan_line = settings.getboolean('ui', 'enable_scan_line')
            self.enable_interlacing = settings.getboolean('ui', 'enable_interlacing')
            self.enable_fps = settings.getboolean('ui', 'enable_fps')

            if version >= 0.06:
                self.color_scheme = settings.get('ui', 'color_scheme')

            if version >= 0.07:
                self.force_square_resolution = settings.getboolean('ui', 'force_square_resolution')

        if 'location' in settings.sections():
            self.location = settings.get('location', 'zipcode')
            self.lat = float(settings.get('location', 'gps_lat'))
            self.lng = float(settings.get('location', 'gps_long'))

        if 'auth' in settings.sections():
            self.bing_maps_key = settings.get('auth', 'bing_maps_key')

        if 'input' in settings.sections():
            self.mfd_controller_rotation = settings.get('input', 'mfd_controller_rotation')

    def save_to_settings(self, filename='settings.ini'):
        """
        Persists settings to a configuration file.
        :param filename: The filename to write to. This file does not need to exist.
        """

        # Build out our settings
        settings = ConfigParser()

        settings.add_section('config')
        settings.set('config', 'version', self.version)

        settings.add_section('location')
        settings.set('location', 'zipcode', self.location)
        settings.set('location', 'gps_lat', self.lat)
        settings.set('location', 'gps_long', self.lng)

        settings.add_section('ui')
        settings.set('ui', 'enable_scan_line', bool(self.enable_scan_line))
        settings.set('ui', 'enable_interlacing', bool(self.enable_interlacing))
        settings.set('ui', 'enable_fps', bool(self.enable_fps))
        settings.set('ui', 'force_square_resolution', bool(self.force_square_resolution))
        settings.set('ui', 'color_scheme', self.color_scheme)

        settings.add_section('auth')
        settings.set('auth', 'bing_maps_key', self.bing_maps_key)

        settings.add_section('input')
        settings.set('input', 'mfd_controller_rotation', self.mfd_controller_rotation)

        # Output to the file
        config_file = open(filename, 'w')
        settings.write(config_file)
        config_file.close()
