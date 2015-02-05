# coding=utf-8

"""
Handles the "amenity" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class AmenityTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        """
        :type entity: MapEntity
        :type value: string
        :type cs: ColorScheme
        :rtype : tuple
        """
        if value in ('pharmacy', 'veterinary', 'hospital', 'clinic'):
            return cs.map_health
        elif value in ('fuel', 'parking', 'car_wash', 'bicycle_parking', 'bicycle_repair_station', 'bicycle_rental',
                       'bus_station', 'car_rental', 'car_sharing', 'car_wash', 'ev_charging', 'charging_station',
                       'parking_entrance', 'parking_space', 'taxi'):
            return cs.map_automotive
        elif value in ('school', 'public_building', 'college', 'kindergarten', 'public_bookcase', 'university',
                       'animal_boarding', 'animal_shelter', 'bench', 'clock', 'coworking_space', 'public_building',
                       'register_office', 'shelter', 'telephone', 'shower', 'toilets'):
            return cs.map_public
        elif value == 'place_of_worship':
            return cs.map_private
        elif value in ('restaurant', 'fast_food', 'supermarket', 'bar', 'bbq', 'biergarten', 'cafe', 'food_court',
                       'ice_cream', 'atm', 'bank', 'studio', 'marketplace', 'photo_booth', 'vending_machine'):
            return cs.map_commercial
        elif value in ('ferry_terminal', 'hunting_stand', 'game_feeding'):
            return cs.map_pedestrian
        elif value in ('boat_sharing', 'arts_centre', 'brothel', 'casino', 'cinema', 'community_centre', 'gambling',
                       'nightclub', 'planetarium', 'social_centre', 'stripclub', 'swingerclub', 'theatre', 'dojo',
                       'firepit', 'gym', 'sauna'):
            return cs.map_recreation
        elif value in ('fire_station', 'police', 'prison', 'ranger_station', 'rescue_station'):
            return cs.map_emergency
        elif value in ('grave_yard', 'crypt', 'creamatorium'):
            return cs.gray
        elif value in ('baby_hatch', 'clinic', 'dentist', 'clinic', 'doctors', 'hospital', 'nursing_home', 'pharmacy',
                       'social_facility', 'veterinary'):
            return cs.map_health
        elif value in ('post_office', 'baby_hatch', 'courthouse', 'embassy', 'post_box', 'townhall'):
            return cs.map_government
        elif value in ('grit_bin', 'recycling', 'waste_disposal'):
            return cs.map_infrastructure
        elif value in ('drinking_water', 'fountain', 'watering_place', 'water_point'):
            return cs.map_water

        return cs.map_service

    def get_description_text(self, entity, value):
        """
        :type entity: MapEntity
        :type value: string
        :rtype: string
        """

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
        elif value == 'baby_hatch':
            return 'Baby Donation Box'
        elif value == 'clinic':
            return 'Clinic'
        elif value == 'dentist':
            return 'Dentist'
        elif value == 'doctors':
            return "Doctor's Office"
        elif value == 'hospital':
            return "Hospital"
        elif value == 'nursing_home':
            return "Nursing Home"
        elif value == 'pharmacy':
            return 'Pharmacy'
        elif value == 'social_facility':
            return 'Social Services Office'
        elif value == 'veterinary':
            return 'Vetrinarian'
        elif value == 'arts_centre':
            return 'Arts Center'
        elif value == 'brothel':
            return 'House of Ill Repute'
        elif value == 'casino':
            return 'Casino'
        elif value == 'cinema':
            return 'Movie Theater'
        elif value == 'community_centre':
            return 'Community Center'
        elif value == 'fountain':
            return 'Fountain'
        elif value == 'gambling':
            return 'Gambling House'
        elif value == 'nightclub':
            return 'Nightclub'
        elif value == 'planetarium':
            return 'Planetarium'
        elif value == 'social_centre':
            return 'Social Center'
        elif value == 'stripclub':
            return 'Strip Club'
        elif value == 'studio':
            return 'Studio'
        elif value == 'swingerclub':
            return 'Den of Eternal Floor Cleaning'
        elif value == 'theatre':
            return 'Performance Theater'
        elif value == 'animal_boarding':
            return 'Animal Boarding'
        elif value == 'animal_shelter':
            return 'Animal Shelter'
        elif value == 'bench':
            return 'Bench'
        elif value == 'clock':
            return 'Clock'
        elif value == 'courthouse':
            return 'Courthouse'
        elif value == 'coworking_space':
            return 'Shared Working Space'
        elif value == 'crematorium':
            return 'Crematorium'
        elif value == 'crypt':
            return 'Crypt'
        elif value == 'dojo':
            return 'Martial Arts Center'
        elif value == 'embassy':
            return 'Embassy'
        elif value == 'fire_station':
            return 'Fire Station'
        elif value == 'firepit':
            return 'Fire Pit'
        elif value == 'grave_yard':
            return 'Graveyard'
        elif value == 'gym':
            return 'Gym'
        elif value == 'hunting_stand':
            return 'Hunting Stand'
        elif value == 'game_feeding':
            return 'Game Feeding Place'
        elif value == 'marketplace':
            return 'Marketplace'
        elif value == 'photo_booth':
            return 'Photo Booth'
        elif value == 'place_of_worship':
            return 'Place of Worship'
        elif value == 'police':
            return 'Police Station'
        elif value == 'post_box':
            return 'Mailbox'
        elif value == 'post_office':
            return 'Post Office'
        elif value == 'prison':
            return 'Prison'
        elif value == 'public_building':
            return 'Public Building'
        elif value == 'ranger_station':
            return 'Ranger Station'
        elif value == 'register_office':
            return "Register's Office"
        elif value == 'recycling':
            return 'Recycling Center'
        elif value == 'sauna':
            return 'Sauna'
        elif value == 'shelter':
            return 'Shelter'
        elif value == 'shower':
            return 'Public Shower / Bath'
        elif value == 'telephone':
            return 'Public Phone'
        elif value == 'toilets':
            return 'Public Toilets'
        elif value == 'townhall':
            return 'Town Hall'
        elif value == 'vending_machine':
            return 'Vending Machine'
        elif value == 'waste_disposal':
            return 'Waste Disposal'
        elif value == 'watering_place':
            return 'Animal Water Source'
        elif value == 'water_point':
            return 'Bulk Drinking Water Access'

        return super(AmenityTagHandler, self).get_description_text(entity, value)