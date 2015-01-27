# coding=utf-8

"""
Contains classes used to hold map entities
"""

__author__ = 'Matt Eland'


class MapEntity(object):
    """
    An abstract component present for maps
    """

    has_lines = False

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

    def get_shop_color(self, cs, shop):

        if shop == 'car_repair':
            return cs.map_automotive

        return cs.map_commercial

    def get_amenity_color(self, cs, amenity):

        if amenity in ('pharmacy', 'veterinary', 'hospital', 'clinic'):
            return cs.map_health
        elif amenity in ('fuel', 'parking'):
            return cs.map_automotive
        elif amenity in ('school', 'public_building'):
            return cs.map_public
        elif amenity == 'place_of_worship':
            return cs.map_private
        elif amenity in ('restaurant', 'fast_food'):
            return cs.map_commercial
        elif amenity == 'fire_station':
            return cs.map_emergency
        elif amenity == 'grave_yard':
            return cs.gray
        elif amenity == 'post_office':
            return cs.map_government

        return cs.map_service

    def get_building_color(self, cs, building):

        if building in ('residential', 'terrace', 'apartment', 'apartments', 'garage', 'garages'):
            return cs.map_residential

        elif building in ('kindergarten', 'school'):
            return cs.map_public

        elif building in ('retail', 'commercial'):
            return cs.map_commercial  # TODO: It'd be good to narrow down if possible

        elif building == 'office':
            return cs.map_private

        elif building == 'power':
            return cs.map_infrastructure

        elif building == 'warehouse':
            return cs.map_private

        elif building == 'shop':
            return cs.map_commercial

        elif building == 'hotel':
            return cs.map_public

        elif building in ('yes', 'roof'):
            return cs.map_structural

        return cs.map_unknown

    def get_display_name(self):

        display_name = self.get_tag_value('short_name')
        if not display_name:
            display_name = self.abbreviate(self.name)

        return display_name

    @staticmethod
    def abbreviate(name, pretty=False):
        """
        Abbreviates a string by intelligently removing middle words and using the first initial
        """

        if name is None:
            return None

        # For / deliminated / multi-role establishments, just take the first chunk
        if '/' in name:
            return MapEntity.abbreviate(name[0:(name.index('/'))])
        elif '\\' in name:
            return MapEntity.abbreviate(name[0:(name.index('\\'))])

        # If we're a long name and we have a 's in the name, chop everything else after that
        if len(name) >= 10 and "'s" in name:
            return name[0:(name.index("'s") + 2)]

        names = name.split()

        # Just two words, don't abbreviate
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


    def __init__(self, lat, lng):
        super(MapPath, self).__init__(lat, lng)

        self.points = list()

class MapLocation(MapEntity):
    """
    Represents a named location on a map
    """

    name = None
