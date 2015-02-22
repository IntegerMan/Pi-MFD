# coding=utf-8

"""
This file contains the core module data provider
"""
from PiMFD.DataProvider import DataProvider

__author__ = 'Matt Eland'


class CoreDataProvider(DataProvider):
    def __init__(self, application):
        super(CoreDataProvider, self).__init__("Core Data Provider")

        self.application = application