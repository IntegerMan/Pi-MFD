# coding=utf-8

"""
Handles the "amenity" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class AmenityTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        if value in ('pharmacy', 'veterinary', 'hospital', 'clinic'):
            return cs.map_health
        elif value in ('fuel', 'parking', 'car_wash', 'bicycle_parking', 'bicycle_repair_station', 'bicycle_rental',
                       'bus_station', 'car_rental', 'car_sharing', 'car_wash', 'ev_charging', 'charging_station',
                       'parking_entrance', 'parking_space', 'taxi'):
            return cs.map_automotive
        elif value in ('school', 'public_building', 'college', 'kindergarten', 'public_bookcase', 'university'):
            return cs.map_public
        elif value == 'place_of_worship':
            return cs.map_private
        elif value in ('restaurant', 'fast_food', 'supermarket', 'bar', 'bbq', 'biergarten', 'cafe', 'food_court',
                       'ice_cream', 'atm', 'bank'):
            return cs.map_commercial
        elif value == 'ferry_terminal':
            return cs.map_pedestrian
        elif value == 'boat_sharing':
            return cs.map_recreational
        elif value == 'fire_station':
            return cs.map_emergency
        elif value == 'grave_yard':
            return cs.gray
        elif value == 'post_office':
            return cs.map_government
        elif value == 'grit_bin':
            return cs.map_infrastructure
        elif value == 'drinking_water':
            return cs.map_water

        return cs.map_service

    def get_description_text(self, entity, value):

        if value == 'bar':
            return 'Bar'
        elif value == 'bbq':
            return 'Barbeque'
        elif value == 'biergarten':
            return 'Biergarten'
        elif value == 'cafe':
            return 'Cafe'
        elif value == 'drinking_water':
            return 'Drinkable Water Source'
        elif value == 'food_court':
            return 'Food Court'
        elif value == 'ice_cream':
            return 'Ice Cream Parlor'
        elif value == 'pub':
            return 'Pub'
        elif value in ('restaurant', 'restaraunt', 'restarant', 'restaurant'):
            return 'Restaurant'
        elif value == 'college':
            return 'College'
        elif value == 'kindergarten':
            return 'Preschool / Kindergarten'
        elif value == 'library':
            return 'Library'
        elif value == 'school':
            return 'School'
        elif value == 'university':
            return 'University'
        elif value == 'public_bookcase':
            return 'Public Bookcase'
        elif value == 'bicycle_parking':
            return 'Bike Parking'
        elif value == 'bicycle_repair_station':
            return 'Bike Repair Shop'
        elif value == 'bicycle_rental':
            return 'Bike Rental'
        elif value == 'boat_sharing':
            return 'Boat Sharing'
        elif value == 'car_rental':
            return 'Car Rental'
        elif value == 'car_sharing':
            return 'Car Sharing'
        elif value == 'car_wash':
            return 'Car Wash'
        elif value in ('ev_charging', 'charging_station'):
            return 'Car Charging Station'
        elif value == 'ferry_terminal':
            return 'Ferry Terminal'
        elif value == 'fuel':
            return 'Gas Station'
        elif value == 'grit_bin':
            return 'Salt Bin'
        elif value == 'parking':
            return 'Parking'
        elif value == 'parking_entrance':
            return 'Parking Entrance'
        elif value == 'parking_space':
            return 'Parking Space'
        elif value == 'taxi':
            return 'Taxi'
        elif value == 'atm':
            return 'ATM'
        elif value == 'bank':
            return 'Bank'
        elif value == 'bureau_de_change':
            return 'Currency Exchange'

        return super(AmenityTagHandler, self).get_description_text(entity, value)