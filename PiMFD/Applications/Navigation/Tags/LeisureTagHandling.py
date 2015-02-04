# coding=utf-8

"""
Handles the "leisure" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class LeisureTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        if value in ('pitch', 'park', 'golf_course', 'sports_centre', 'adult_gaming_centr', 'amusement_arcade',
                     'beach_resort', 'bandstand', 'dog_park', 'dance', 'hackerspace', 'ice_rink', 'sports_centre',
                     'stadium', 'summer_camp'):
            return cs.map_recreation

        elif value in ('playground', 'track', 'bird_hide', 'firepit', 'fishing', 'wildlife_hide'):
            return cs.map_pedestrian

        elif value in ('garden', 'golf_course', 'miniature_golf', 'nature_reserve'):
            return cs.map_vegitation

        elif value in ('swimming_pool', 'marina', 'water_park'):
            return cs.map_water

        elif value == 'slipway':
            return cs.map_structural

        return super(LeisureTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):

        if value == 'adult_gaming_centre':
            return 'Arcade (Adults Only)'
        elif value == 'amusement_arcade':
            return 'Arcade'
        elif value == 'beach_resort':
            return 'Beach Resort'
        elif value == 'bandstand':
            return 'Bandstand'
        elif value == 'bird_hide':
            return 'Bird Hide'
        elif value == 'dance':
            return 'Dance'
        elif value == 'dog_park':
            return 'Dog Park'
        elif value == 'firepit':
            return 'Fire Pit'
        elif value == 'fishing':
            return 'Fishing'
        elif value == 'garden':
            return 'Garden'
        elif value == 'golf_course':
            return 'Golf Course'
        elif value == 'hackerspace':
            return 'Hackerspace'
        elif value == 'ice_rink':
            return 'Ice Rink'
        elif value == 'marina':
            return 'Marina'
        elif value == 'miniature_golf':
            return 'Mini-Golf Course'
        elif value == 'nature_reserve':
            return 'Nature Reserve'
        elif value == 'park':
            return 'Park'
        elif value == 'pitch':
            return 'Sporting Pitch'
        elif value == 'playground':
            return 'Playground'
        elif value == 'slipway':
            return 'Boat Launch'
        elif value == 'sports_centre':
            return 'Sports Center'
        elif value == 'stadium':
            return 'Stadium'
        elif value == 'summer_camp':
            return 'Summer Camp'
        elif value == 'swimming_pool':
            return 'Swimming Pool'
        elif value == 'track':
            return 'Track'
        elif value == 'water_park':
            return 'Water Park'
        elif value == 'wildlife_hide':
            return 'Wildlife Hide'

        return super(LeisureTagHandler, self).get_description_text(entity, value)