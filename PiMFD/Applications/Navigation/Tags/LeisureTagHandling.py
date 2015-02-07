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

            sport = entity.get_tag_value('sport')
            if sport:
                sports = {'9pin': 'Bowling Alley (9 Pin)',
                          '10pin': 'Bowling Alley',
                          'american_football': 'Football Field',
                          'aikido': 'Aikido Dojo',
                          'archery': 'Archery Range',
                          'athletics': 'Athletics Track',
                          'australian_football': 'Football Field (Aussie Rules)',
                          'base': 'Base Jumping Area',
                          'badminton': 'Badminton Court',
                          'bandy': 'Bandy Rink',
                          'baseball': 'Baseball Field',
                          'basketball': 'Orb Dribbling (Basketball Court)',
                          'beachvolleyball': 'Volleyball Court (Beach)',
                          'billiards': 'Billiards Parlor',
                          'bmx': 'BMX Course',
                          'bobsleigh': 'Bobsleigh Course',
                          'boules': 'Ball Gaming Course',
                          'bowls': 'Bowling Area',
                          'boxing': 'Boxing Match',
                          'canadian_football': 'Football Field (Canadian)',
                          'canoe': 'Canoe Course',
                          'chess': 'Chess',
                          'cliff_diving': 'Cliff Diving Area',
                          'climbing': 'Climbing Area',
                          'climbing_adventure': 'Adventure Climbing',
                          'cockfighting': 'Rooster Fighting',
                          'cricket': 'Cricket Pitch',
                          'croquet': 'Croquet Court',
                          'curling': 'Curling Rink',
                          'cycling': 'Biking Course',
                          'darts': 'Darts',
                          'diving': 'Diving Area',
                          'dog_racing': 'Dog Racing',
                          'equestrian': 'Horse Sports',
                          'fencing': 'Fencing Match',
                          'field_hockey': 'Field Hockey',
                          'football': 'Football',
                          'free_flying': 'Hangliding / Parasailing',
                          'gaelic_games': 'Gaelic Games Area',
                          'golf': 'Golf Course',
                          'gymnastics': 'Gymnastics',
                          'handball': 'Handball Court',
                          'hapkido': 'Hapkido Dojo',
                          'hockey': 'Hockey Rink',
                          'horseshoes': 'Horseshoes Court',
                          'horse_racing': 'Horse Racing',
                          'ice_hockey': 'Ice Hockey Rink',
                          'ice_skating': 'Ice Skating Rink',
                          'ice_stock': 'Bavarian Curling',
                          'judo': 'Judo Dojo',
                          'karting': 'Kart Racing',
                          'kitesurfing': 'Kite Surfing',
                          'korfball': 'Korfball Court',
                          'model_aerodrome': 'Radio Controlled Airfield',
                          'motocross': 'Motocross Racing',
                          'motor': 'Motorsport Course',
                          'multi': 'Multi-Sport Area',
                          'obstacle_course': 'Obstacle Course',
                          'orienteering': 'Orienteering Course',
                          'paddle_tennis': 'Paddle Tennis Court',
                          'paragliding': 'Paragliding Site',
                          'pelota': 'Ball Games Court',
                          'racquet': 'Raquetball Court',
                          'rc_car': 'RC Car Course',
                          'roller_skating': 'Roller Skating Rink',
                          'rowing': 'Rowing Course',
                          'rugby_league': 'Rugby League',
                          'rugby_union': 'Rugby Union',
                          'running': 'Running Track',
                          'safety_training': 'Safety Training',
                          'sailing': 'Sailing',
                          'scuba_diving': 'Scuba Diving',
                          'shooting': 'Shooting Range',
                          'skating': 'Skating Rink',
                          'skateboard': 'Skateboard Park',
                          'skiing': 'Ski Slope',
                          'soccer': 'Soccer Field',
                          'surfing': 'Surfing Area',
                          'swimming': 'Swimming Area',
                          'table_tennis': 'Ping Pong',
                          'table_soccer': 'Foosball',
                          'taekwondo': 'Taekwondo Dojo',
                          'team_handball': 'Handball Court',
                          'tennis': 'Tennis Court',
                          'toboggan': 'Toboggan Run',
                          'volleyball': 'Volleyball Court',
                          'water_polo': 'Water Polo',
                          'water_ski': 'Water Ski',
                          'weightlifting': 'Weightlifting Area',
                          'wrestling': 'Wrestling Area'
                }

                if value in sports:
                    return sports[value]

            return 'Sports Area'

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