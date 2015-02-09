# coding=utf-8

"""
Handles the "tourism" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class TourismTagHandler(TagHandler):
    """
    Provides information on the 'tourism' tag
    """

    def get_color(self, entity, value, cs):

        """
        :type entity: MapEntity
        :type value: string
        :type cs: PiMFD.UI.ColorScheme.ColorScheme
        :rtype : tuple
        """
        if value in ('alpine_hut', 'apartment', 'camp_site', 'caravan_site', 'chalet', 'guest_house', 'hostel', 'motel',
                     'wilderness_hut', 'hotel'):
            return cs.map_public
        elif value in ('attraction', 'artwork', 'gallery', 'museum', 'theme_park', 'yes', 'zoo'):
            return cs.map_recreation
        elif value in ('information',):
            return cs.map_service
        elif value in ('picnic_site', 'viewpoint'):
            return cs.map_pedestrian

        return super(TourismTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):
        """
        :type entity: MapEntity
        :type value: string
        :rtype: string
        """

        if value == 'alpine_hut':
            return 'Alpine Hut'
        elif value == 'apartment':
            return 'Time-Share Apartment'
        elif value in ('attraction', 'yes'):
            return 'Tourist Attraction'
        elif value == 'artwork':
            return 'Public Art'
        elif value == 'camp_site':
            return 'Camp Site'
        elif value == 'caravan_site':
            return 'RV Park'
        elif value == 'chalet':
            return 'Cabin'
        elif value == 'gallery':
            return 'Gallery'
        elif value == 'guest_house':
            return 'Guest House'
        elif value == 'hostel':
            return 'Hostel'
        elif value == 'hotel':
            return 'Hotel'
        elif value == 'information':
            return 'Public Information'
        elif value == 'motel':
            return 'Motel'
        elif value == 'museum':
            return 'Museum'
        elif value == 'picnic_site':
            return 'Picnic Site'
        elif value == 'theme_park':
            return 'Theme Park'
        elif value == 'viewpoint':
            return 'Observation Point'
        elif value == 'wilderness_hut':
            return 'Wilderness Hut'
        elif value == 'zoo':
            return 'Zoo'

        return super(TourismTagHandler, self).get_description_text(entity, value)