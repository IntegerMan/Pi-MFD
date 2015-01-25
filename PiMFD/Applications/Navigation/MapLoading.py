# coding=utf-8

from __future__ import print_function
import traceback

from PiMFD.Applications.Navigation.MapEntities import MapLocation
from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


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
    locations = []
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
        self.height = (bounds[2] - bounds[0]) / 2
        self.width = (bounds[3] - bounds[1]) / 2
        self.origin = (
            bounds[1] + self.height,
            bounds[0] + self.width
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
        self.locations = []

        print("Fetching maps " + url)

        # TODO: What the heck? This looks to be infinitely calling the URL with no failover. That bad.
        while True:
            try:
                response = requests.get(url)
            except:
                error_message = "Unhandled error getting request {0}\n".format(str(traceback.format_exc()))
                print(error_message)
            else:
                break

        data = response.text.encode('UTF-8')

        self.status_text = 'Parsing...'

        print(data)

        osm_dict = xmltodict.parse(data)
        try:

            # Load Nodes
            for node in osm_dict['osm']['node']:
                id = node['@id']
                self.nodes[id] = node

                # Skip Invisible items
                if '@visible' in node and node['@visible'] == 'false':
                    continue

                # We don't care about it unless it has tags
                if 'tag' not in node:
                    continue

                is_valid = False

                location = MapLocation(float(node['@lat']), float(node['@lon']))
                location.id = id
                location.name = None

                if '@k' in node['tag']:
                    if self.process_tag(location, node['tag']):
                        is_valid = True
                else:
                    for tag in node['tag']:
                        if self.process_tag(location, tag):
                            is_valid = True

                if is_valid:
                    self.locations.append(location)

            # Load Waypoints
            for way in osm_dict['osm']['way']:
                waypoints = []
                for node_id in way['nd']:
                    node = self.nodes[node_id['@ref']]
                    waypoints.append((float(node['@lat']), float(node['@lon'])))
                self.ways.append(waypoints)

        except:
            error_message = "Unhandled error parsing map data {0}\n".format(str(traceback.format_exc()))
            print(error_message)

        self.has_data = len(self.nodes) > 0
        self.status_text = "Loaded {} Nodes of Map Data".format(len(self.nodes))

    def process_tag(self, location, tag):

        tag_name = tag["@k"]
        tag_value = tag["@v"]

        # Named Amenities
        if tag_name == "name":
            location.name = tag_value
            return True

        elif tag_name in (
                "amenity", "leisure", "man_made", "shop", "cuisine", "building", "power", "religion", "denomination",
                "website", "railway", "highway", "edu", "power", "railway"):

            location.tags.append((tag_name, tag_value))
            return True

        elif not str.startswith(str(tag_name), 'addr:'):
            print('ignoring pair: ' + tag_name + '/' + tag_value)

        return False

    def fetch_by_coordinate(self, lat, lng, range):

        return self.fetch_area((
            float(lng) - range,
            float(lat) - range,
            float(lng) + range,
            float(lat) + range
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
                lat = waypoint[1] - self.origin[1]
                lng = waypoint[0] - self.origin[0]
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

    def transpose_locations(self, dimensions, offset, flip_y=True):

        width = dimensions[0]
        height = dimensions[1]

        w_coef = width / self.width / 2
        h_coef = height / self.height / 2

        symbols = []

        for location in self.locations:

            # Determine relative lat / long to origin
            rel_lat = self.origin[0] - location.lat
            rel_lng = self.origin[1] - location.lng

            # Scale the location accordingly
            lat = (rel_lat * w_coef) + offset[1]
            lng = (rel_lng * h_coef)

            # We'll typically need to flip the longitude since 0, 0 is upper left corner on screens
            if flip_y:
                lng *= -1

            lng += offset[0]

            symbols.append(MapSymbol(lng, lat, location))

        return symbols

