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

    def get_tag_value(self, name):
        """
        Gets the value for the first tag that matches name or returns None
        :type name: str
        :param name: The tag key
        :return: The value for the first tag that matches name or returns None
        """

        for tag in self.get_tags(name):
            return tag[1]

        return None

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


    @staticmethod
    def abbreviate(name, pretty=False):
        """
        Abbreviates a string by intelligently removing middle words and using the first initial
        """

        if name is None:
            return None

        names = name.split()

        if len(names) <= 2:
            return name

        # Chop off silly opening words
        if names[0].lower() == 'the' or names[0].lower() == 'le' or names[0].lower() == 'la' or names[
            0].lower() == 'el':
            names = names[1:]
            return MapEntity.abbreviate(' '.join(names), pretty)

        result = [names[0]]
        tiny_name = False

        for surname in names[1:-1]:
            if len(surname) <= 3:
                result.append(surname)
                tiny_name = True
            else:
                if pretty and tiny_name:
                    result.append(surname)
                else:
                    result.append(surname[0] + '.')
                tiny_name = False

        result.append(names[-1])

        return ' '.join(result)

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
