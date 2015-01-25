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

    def get_tags(self, name):
        """
        Gets all tags that have name as their key
        :type name: str
        :param name: The tag key
        :return: All tags (yielded) that have the matching name
        """

        for tag in self.tags:
            if tag[0] == name:
                yield tag

    def has_tag(self, name):
        """
        Returns True if a tag with a key of name was found, regardless of value
        :param name: The key to look for
        :return: True if a tag with a key of name was found, otherwise False
        """

        for tag in self.get_tags(name):
            return True

        return False

    def has_tag_value(self, name, value):
        """
        Determins if the specified tag / value pair exists in this set
        :type name: str
        :param name: The tag key
        :type value: str
        :param value: The tag value
        :return: True if the key / value pair was present, otherwise False
        """

        for tag in self.get_tags(name):
            if tag[1] == value:
                return True

        return False


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
