# coding=utf-8
"""
Contains code related to application options management
"""
from ConfigParser import ConfigParser

__author__ = 'Matt Eland'


class MFDAppOptions(object):
    """
    Contains misc. application options
    """

    app_name = 'Pi-MFD'
    app_version = '0.01 Development Version'
    app_author = 'Matt Eland'
    copyright_year = 2015
    font_name = 'Fonts/VeraMono.ttf'
    display = None
    location = '60045'

    def load_from_settings(self, filename='settings.ini'):
        """
        Loads settings from the default configuration file.
        :param filename: The filename to load. This file does not need to exist.
        """

        settings = ConfigParser()
        settings.read(filename)

        if 'location' in settings.sections():
            self.location = settings.get('location', 'zipcode')

    def save_to_settings(self, filename='settings.ini'):
        """
        Persists settings to a configuration file.
        :param filename: The filename to write to. This file does not need to exist.
        """

        # Build out our settings
        settings = ConfigParser()
        settings.add_section('location')
        settings.set('location', 'zipcode', self.location)

        # Output to the file
        config_file = open(filename, 'w')
        settings.write(config_file)
        config_file.close()
