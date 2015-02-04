# coding=utf-8

"""
Handles the "building" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class BuildingTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        if value in ('residential', 'terrace', 'apartment', 'apartments', 'garage', 'garages'):
            return cs.map_residential

        elif value in ('kindergarten', 'school'):
            return cs.map_public

        elif value in ('retail', 'commercial', 'shop', 'restaurant', 'fast_food', 'supermarket'):
            return cs.map_commercial

        elif value == 'power':
            return cs.map_infrastructure

        elif value in ('warehouse', 'industrial', 'office'):
            return cs.map_private

        elif value == 'hotel':
            return cs.map_public

        elif value in ('yes', 'roof'):
            return cs.map_structural

        return super(BuildingTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):

        if value == 'terrace':
            return 'Residential Townhouse'
        elif value == 'kindergarten':
            return 'Preschool / Kindergarten'
        elif value == 'roof':
            return 'Shelter / Awning'
        elif value == 'commercial':
            return 'Commercial Building'
        elif value == 'retail':
            return 'Strip Mall'
        elif value == 'mall':
            return 'Shopping Mall'
        elif value == 'yes':
            return 'Unclassified Building'

        return super(BuildingTagHandler, self).get_description_text(entity, value)