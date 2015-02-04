# coding=utf-8

"""
Contains color-related items
"""

__author__ = 'Matt Eland'


class MapColorizer(object):

    @staticmethod
    def get_color(entity, context, cs):

        building = entity.get_tag_value('building')
        shop = entity.get_tag_value('shop')
        amenity = entity.get_tag_value('amenity')

        if entity.has_tag('railway'):

            # TODO: There's likely a lot more nuance to be had here
            return cs.map_structural

        elif entity.has_tag('highway'):

            color = context.tag_handlers.get_color('highway', entity, cs)
            if color:
                return color

        elif entity.has_tag_value('boundary', 'administrative'):
            return cs.map_government

        elif entity.has_tag_value('natural', 'water') or entity.has_tag('water'):
            return cs.map_water

        elif entity.has_tag_value('natural', 'wood') or entity.has_tag('wood'):
            return cs.map_vegitation

        elif entity.has_tag('waterway'):
            return cs.map_water

        elif entity.has_tag('leisure'):

            leisure = entity.get_tag_value('leisure')

            if leisure in ('pitch', 'park', 'golf_course', 'sports_centre'):
                return cs.map_recreation

            elif leisure in ('playground', 'track'):
                return cs.map_pedestrian

            elif leisure == 'swimming_pool':
                return cs.map_water

        elif entity.has_tag('landuse'):

            landuse = entity.get_tag_value('landuse')

            if landuse in ('cemetery', 'cemetery'):
                return cs.map_structural

            elif landuse == 'grass':
                return cs.map_recreation

            elif landuse == 'construction':
                return cs.map_infrastructure

        elif entity.has_tag('tourism'):

            tourism = entity.get_tag_value('tourism')
            if tourism in (
                    'hotel', 'apartment', 'alpine_hut', 'camp_site', 'caravan_site', 'chalet', 'guest_house', 'hostel',
                    'motel',
                    'wilderness_hut'):
                return cs.map_public  # Travel instead? New thing? Residential?

            elif tourism == 'theme_park':
                return cs.map_recreation

        elif entity.has_tag('power'):
            return cs.map_infrastructure

        elif entity.has_tag('barrier'):
            color = context.tag_handlers.get_color('barrier', entity, cs)
            if color:
                return color


        elif entity.has_tag('traffic_sign'):
            return cs.map_government

        elif amenity:
            return MapColorizer.get_amenity_color(cs, amenity)

        elif shop:
            return MapColorizer.get_shop_color(cs, shop)

        elif building:

            if shop:
                return MapColorizer.get_shop_color(cs, shop)

            elif amenity:
                return MapColorizer.get_amenity_color(cs, amenity)

            else:
                color = context.tag_handlers.get_color('building', entity, cs)
                if color:
                    return color

        elif entity.has_tag('place'):

            place = entity.get_tag_value('place')
            if place in ('hamlet', 'town', 'village'):
                return cs.map_government
            elif place == 'island':
                return cs.background

        elif entity.has_tag_value('footway', 'crossing'):
            return cs.yellow

        elif entity.has_tag('surveillance'):
            return cs.map_emergency

        elif entity.has_tag('man_made'):

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

        elif entity.has_tag('actor'):

            actor = entity.get_tag_value('actor')

            if actor in ('self', 'cursor'):
                return cs.highlight

        elif entity.has_tag('weather'):
            return cs.foreground

        return None

    @staticmethod
    def get_shop_color(cs, shop):

        if shop == 'car_repair':
            return cs.map_automotive

        return cs.map_commercial

    @staticmethod
    def get_amenity_color(cs, amenity):

        if amenity in ('pharmacy', 'veterinary', 'hospital', 'clinic'):
            return cs.map_health
        elif amenity in ('fuel', 'parking', 'car_wash'):
            return cs.map_automotive
        elif amenity in ('school', 'public_building'):
            return cs.map_public
        elif amenity == 'place_of_worship':
            return cs.map_private
        elif amenity in ('restaurant', 'fast_food', 'supermarket'):
            return cs.map_commercial
        elif amenity == 'fire_station':
            return cs.map_emergency
        elif amenity == 'grave_yard':
            return cs.gray
        elif amenity == 'post_office':
            return cs.map_government

        return cs.map_service


