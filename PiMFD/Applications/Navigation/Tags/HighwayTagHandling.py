# coding=utf-8

"""
Handles the "highway" tag
"""
from PiMFD.Applications.Navigation.Tags.TagHandling import TagHandler

__author__ = 'Matt Eland'


class HighwayTagHandler(TagHandler):
    def get_color(self, entity, value, cs):

        # If it's got a bridge, we'll handle it a bit differently
        if entity.has_tag('bridge'):
            return cs.map_structural

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
        elif value == 'abandoned':
            return cs.map_structural
        elif value == ('unclassified', 'road'):
            return cs.map_unknown
        elif value in ('residential', 'living_street'):
            return cs.map_residential
        elif value in ('turning_circle', 'mini_roundabout', 'motorway_junction'):
            return cs.map_automotive
        elif value in ('street_lamp', 'construction'):
            return cs.map_infrastructure
        elif value in ('path', 'footway', 'cycleway', 'pedestrian', 'track'):
            return cs.map_pedestrian
        elif value == 'crossing':
            return cs.yellow
        elif value == 'service':
            return cs.map_service
        elif value == 'proposed':
            return cs.map_emergency

        return super(HighwayTagHandler, self).get_color(entity, value, cs)

    def get_description_text(self, entity, value):

        if value in ('residential', 'living_street'):
            return 'Residential Street'
        elif value == 'service':
            return 'Access Road'
        elif value == 'street_lamp':
            return 'Street Light'
        elif value == 'track':
            return 'Trail'
        elif value == 'pedestrian':
            return 'Pedestrian Road'
        elif value in ('path', 'footway'):
            return 'Path'
        elif value == 'steps':
            return 'Steps'
        elif value == 'bridleway':
            return 'Horse Trail'
        elif value == 'cycleway':
            return 'Bike Trail'
        elif value == 'raceway':
            return 'Raceway'
        elif value == 'proposed':
            return 'Proposed Road'
        elif value == 'construction':
            return 'Road Under Construction'
        elif value == 'crossing':
            return 'Crossing'
        elif value == 'bus_stop':
            return 'Bus Stop'
        elif value == 'traffic_signals':
            return 'Stoplight'
        elif value == 'stop':
            return 'Stop Sign'
        elif value in ('mini_roundabout', 'turning_circle'):
            return 'Roundabout / Cul du Sac'
        elif value in ('motorway', 'trunk'):
            return 'Highway'
        elif value == 'motorway_link':
            return 'On-Ramp / Off-Ramp'
        elif value in ('primary', 'secondary'):
            return 'Major Road'
        elif value == 'tertiary':
            return 'Side Road'
        elif value in ('unclassified', 'road', 'yes'):
            return 'Unclassified Road'
        elif value == 'abandoned':
            return 'Abandoned Road'

        return super(HighwayTagHandler, self).get_description_text(entity, value)