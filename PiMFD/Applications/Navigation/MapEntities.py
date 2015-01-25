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
    id = 'UNK'

    def __init__(self, lat, lng):
        super(MapEntity, self).__init__()

        self.tags = list()
        self.lat = lat
        self.lng = lng


class MapPath(MapEntity):
    """
    Represents a lined area on the map
    """

    points = list()

    def __init__(self, lat, lng):
        super(MapPath, self).__init__(lat, lng)

        self.points = list()

class MapLocation(MapEntity):
    """
    Represents a named location on a map
    """

    name = 'UNK'
