# coding=utf-8

"""
Contains color-related items
"""

__author__ = 'Matt Eland'


class MapColorizer(object):
    @staticmethod
    def get_color(entity, cs):

        building = entity.get_tag_value('building')
        shop = entity.get_tag_value('shop')
        amenity = entity.get_tag_value('amenity')

        if entity.has_tag('railway'):

            # TODO: There's likely a lot more nuance to be had here
            return cs.map_structural

        elif entity.has_tag('highway'):

            # If it's got a bridge, we'll handle it a bit differently
            if entity.has_tag('bridge'):
                return cs.map_structural

            value = entity.get_tag_value('highway')

            if value in ('motoway', 'motorway'):
                return cs.map_major_road
            elif value in ('trunk', 'motorway_link'):
                return cs.map_major_road
            elif value == 'primary':
                return cs.map_major_road
            elif value == 'secondary':
                return cs.map_major_road
            elif value == 'tertiary':
                return cs.map_major_road
            elif value == ('unclassified', 'road'):
                return cs.map_unknown
            elif value in ('residential', 'living_street'):
                return cs.map_residential
            elif value in ('turning_circle', 'mini_roundabout', 'motorway_junction'):
                return cs.map_automotive
            elif value in ('street_lamp', 'construction'):
                return cs.map_infrastructure
            elif value in ('path', 'footway', 'cycleway'):
                return cs.map_pedestrian
            elif value == 'crossing':
                return cs.yellow
            elif value == 'service':
                return cs.map_service
            elif value == 'proposed':
                return cs.map_emergency
            else:
                return cs.map_unknown  # For Debugging

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

            barrier = entity.get_tag_value('barrier')
            if barrier in (
                    'city_wall', 'guard_rail', 'cable_barrier', 'block', 'border_control', 'debris',
                    'height_restrictor',
                    'jersey_barrier', 'sally_port'):
                return cs.map_structural
            elif barrier in ('ditch', 'retaining_wall', 'hedge', 'horse_stile', 'log'):
                return cs.map_vegitation
            elif barrier in ('wall', 'fence', 'entrance', 'gate', 'hampshire_gate', 'lift_gate', 'spikes'):
                return cs.map_private
            elif barrier in (
                    'bollard', 'kerb', 'cycle_barrier', 'chain', 'full-height_turnstile', 'kissing_gate',
                    'kent_carriage_gap',
                    'rope', 'motorcycle_barrier'):
                return cs.map_pedestrian
            else:
                return cs.map_unknown

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
                return MapColorizer.get_building_color(cs, building)

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

        elif entity.has_tag('incident'):

            return cs.map_emergency

        elif entity.has_tag('actor'):

            actor = entity.get_tag_value('actor')

            if actor in ('self', 'cursor'):
                return cs.highlight

        return cs.map_unknown

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

    @staticmethod
    def get_building_color(cs, building):

        if building in ('residential', 'terrace', 'apartment', 'apartments', 'garage', 'garages'):
            return cs.map_residential

        elif building in ('kindergarten', 'school'):
            return cs.map_public

        elif building in ('retail', 'commercial', 'shop', 'restaurant', 'fast_food', 'supermarket'):
            return cs.map_commercial

        elif building == 'power':
            return cs.map_infrastructure

        elif building in ('warehouse', 'industrial', 'office'):
            return cs.map_private

        elif building == 'hotel':
            return cs.map_public

        elif building in ('yes', 'roof'):
            return cs.map_structural

        return cs.map_unknown

