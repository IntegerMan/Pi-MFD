# coding=utf-8

"""
Contains classes used to hold map entities
"""

__author__ = 'Matt Eland'


class MapEntity(object):
    """
    An abstract component present for maps
    """

    tags = list()
    lat = 0.0
    lng = 0.0

    def __init__(self, lat, lng):
        super(MapEntity, self).__init__()

        self.tags = list()
        self.lat = lat
        self.lng = lng


class MapPath(MapEntity):
    pass


class MapLocation(MapEntity):
    """
    Represents a named location on a map
    """

    name = 'UNK'
