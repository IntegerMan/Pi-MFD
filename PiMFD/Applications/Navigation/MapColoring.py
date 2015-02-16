# coding=utf-8

"""
Contains color-related items
"""
from PiMFD.UI.ColorScheme import ColorScheme

__author__ = 'Matt Eland'


class MapColorizer(object):

    @staticmethod
    def get_color(entity, context, cs):

        """

        :type cs: ColorScheme
        :type entity: PiMFD.Applications.Navigation.MapEntities.MapEntity
        :type context: PiMFD.Applications.Navigation.MapContext.MapContext
        :rtype: tuple
        """

        if entity.has_tag('railway'):
            return cs.map_structural  # TODO: There's likely a lot more nuance to be had here

        elif entity.has_tag('highway'):
            color = context.tag_handlers.get_color('highway', entity, cs)
            if color:
                return color

        elif entity.has_tag_value('boundary', 'administrative'):
            return cs.map_government

        elif entity.has_tag('water'):
            return cs.map_water

        elif entity.has_tag('wood'):
            return cs.map_vegetation

        elif entity.has_tag('natural'):
            color = context.tag_handlers.get_color('natural', entity, cs)
            if color:
                return color

        elif entity.has_tag('waterway'):
            return cs.map_water

        elif entity.has_tag('leisure'):
            color = context.tag_handlers.get_color('leisure', entity, cs)
            if color:
                return color

        elif entity.has_tag('landuse'):

            # TODO: Probably need a tag handler for this eventually

            landuse = entity.get_tag_value('landuse')

            if landuse in ('cemetery', 'cemetery'):
                return cs.map_structural

            elif landuse == 'grass':
                return cs.map_recreation

            elif landuse == 'construction':
                return cs.map_infrastructure

            elif landuse == 'wetlands':
                return cs.map_vegetation

        elif entity.has_tag('tourism'):
            color = context.tag_handlers.get_color('tourism', entity, cs)
            if color:
                return color

        elif entity.has_tag('power'):
            return cs.map_infrastructure

        elif entity.has_tag('barrier'):
            color = context.tag_handlers.get_color('barrier', entity, cs)
            if color:
                return color

        elif entity.has_tag('traffic_sign'):
            return cs.map_government

        elif entity.has_tag('amenity'):
            color = context.tag_handlers.get_color('amenity', entity, cs)
            if color:
                return color

        elif entity.has_tag('shop'):
            color = context.tag_handlers.get_color('shop', entity, cs)
            if color:
                return color

        elif entity.has_tag('building'):
            color = context.tag_handlers.get_color('building', entity, cs)
            if color:
                return color

        elif entity.has_tag('place'):

            place = entity.get_tag_value('place')
            if place in ('hamlet', 'town', 'village'):
                return cs.map_government
            elif place == 'island':
                return cs.map_vegetation

        elif entity.has_tag_value('footway', 'crossing'):
            return cs.yellow

        elif entity.has_tag('surveillance'):
            return cs.map_emergency

        elif entity.has_tag('man_made'):

            # TODO: Probably need a tag handler for this eventually

            man_made = entity.get_tag_value('man_made')

            if man_made == 'water_tower':
                return cs.map_infrastructure

            elif man_made == 'surveillance':
                return cs.map_emergency

            elif man_made == 'tower':
                if entity.has_tag_value('tower:type', 'communication'):
                    return cs.map_infrastructure

        elif entity.has_tag('incident'):

            return cs.map_emergency

        elif entity.has_tag('office'):
            return cs.map_private

        elif entity.has_tag('actor'):

            actor = entity.get_tag_value('actor')

            if actor in ('self', 'cursor'):
                return cs.highlight

        elif entity.has_tag('weather'):
            return cs.foreground

        elif entity.has_tag('boundary'):
            return cs.map_government

        elif entity.has_tag('noexit'):
            return cs.map_automotive

        elif entity.has_tag_starting_with('abandoned:'):
            return cs.map_structural

        return None


