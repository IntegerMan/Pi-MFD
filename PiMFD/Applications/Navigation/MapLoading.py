# coding=utf-8

from __future__ import print_function

"""
Contains code related to rendering maps to the screen
"""
from math import floor
import requests
import xmltodict

__author__ = 'Multiple'


class Maps(object):
    """
    A class used for requesting and managing Open Street Maps (OSM) map data
    """
    nodes = {}
    ways = []
    tags = []
    origin = None
    width = 0
    height = 0

    has_data = False
    status_text = "Loading Map Data..."

    SIG_PLACES = 3
    GRID_SIZE = 0.001

    def __init__(self):
        super(Maps, self).__init__()

    def float_floor_to_precision(self, value, precision):
        for i in range(precision):
            value *= 10
        value = floor(value)
        for i in range(precision):
            value /= 10
        return value

    def fetch_grid(self, coords):
        # lat = self.float_floor_to_precision(coords[0], self.SIG_PLACES)
        # lng = self.float_floor_to_precision(coords[1], self.SIG_PLACES)
        # print lat, lng
        lat = coords[0]
        lng = coords[1]

        return self.fetch_area([
            lat - self.GRID_SIZE,
            lng - self.GRID_SIZE,
            lat + self.GRID_SIZE,
            lng + self.GRID_SIZE
        ])

    def fetch_area(self, bounds):
        self.width = (bounds[2] - bounds[0]) / 2
        self.height = (bounds[3] - bounds[1]) / 2
        self.origin = (
            bounds[0] + self.width,
            bounds[1] + self.height
        )
        url = "http://www.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % (
            bounds[0],
            bounds[1],
            bounds[2],
            bounds[3]
        )

        # Clear out old data
        self.has_data = False
        self.nodes = {}
        self.ways = []
        self.tags = []

        print("Fetching maps " + url)

        # TODO: What the heck? This looks to be infinitely calling the URL with no failover. That bad.
        while True:
            try:
                response = requests.get(url)
            except:
                pass
            else:
                break

        data = response.text

        self.status_text = 'Parsing...'

        print('Received data: ' + data)

        osm_dict = xmltodict.parse(data.encode('UTF-8'))
        try:
            for node in osm_dict['osm']['node']:
                self.nodes[node['@id']] = node
                if 'tag' in node:
                    for tag in node['tag']:
                        try:
                            # Named Amenities
                            if tag["@k"] == "name":
                                amenity = ''
                                for tag2 in node['tag']:
                                    if tag2["@k"] == "amenity":
                                        amenity = tag2["@v"]
                                self.tags.append((float(node['@lat']), float(node['@lon']), tag["@v"], amenity))
                                # Personal Addresses - Removed
                                #if tag["@k"] == "addr:housenumber":
                                #	   for t2 in node['tag']:
                                #			   if t2["@k"] == "addr:street":
                                #					   self.tags.append((float(node['@lat']), float(node['@lon']),tag["@v"]+" "+t2["@v"]))
                        except Exception as e:
                            pass

            for way in osm_dict['osm']['way']:
                waypoints = []
                for node_id in way['nd']:
                    node = self.nodes[node_id['@ref']]
                    waypoints.append((float(node['@lat']), float(node['@lon'])))
                self.ways.append(waypoints)
        except Exception as e:
            print(e)

        self.has_data = len(self.nodes) > 0
        self.status_text = "Loaded {} Nodes of Map Data".format(len(self.nodes))

    def fetch_by_coordinate(self, coords, range):
        # return self.fetch_area((-83.0036, 40.1488, -82.9973, 40.1531))
        return self.fetch_area((
            float(coords[0]) - range,
            float(coords[1]) - range,
            float(coords[0]) + range,
            float(coords[1]) + range
        ))

    def transpose_ways(self, dimensions, offset, flip_y=True):
        width = dimensions[0]
        height = dimensions[1]
        w_coef = width / self.width / 2
        h_coef = height / self.height / 2
        transways = []
        for way in self.ways:
            transway = []
            for waypoint in way:
                lat = waypoint[1] - self.origin[0]
                lng = waypoint[0] - self.origin[1]
                wp = [
                    (lat * w_coef) + offset[0],
                    (lng * h_coef) + offset[1]
                ]
                if flip_y:
                    wp[1] *= -1
                    wp[1] += offset[1] * 2
                transway.append(wp)
            transways.append(transway)
        return transways

    def transpose_tags(self, dimensions, offset, flip_y=True):
        width = dimensions[0]
        height = dimensions[1]
        w_coef = width / self.width / 2
        h_coef = height / self.height / 2
        transtags = []
        for tag in self.tags:
            lat = tag[1] - self.origin[0]
            lng = tag[0] - self.origin[1]
            wp = [
                tag[2],
                (lat * w_coef) + offset[0],
                (lng * h_coef) + offset[1],
                tag[3]
            ]
            if flip_y:
                wp[2] *= -1
                wp[2] += offset[1] * 2
            transtags.append(wp)
        return transtags