# coding=utf-8

from __future__ import print_function
import traceback

from PiMFD.Applications.Navigation.MapEntities import MapLocation, MapPath
from PiMFD.Applications.Navigation.MapLines import MapLine
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
    locations = []
    waypoints = []
    origin = None
    width = 0
    height = 0

    has_data = False
    status_text = "Loading Map Data..."

    output_file = None

    SIG_PLACES = 3
    GRID_SIZE = 0.001

    def __init__(self):
        super(Maps, self).__init__()

        self.locations = []
        self.waypoints = []

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
        self.bounds = bounds
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

        self.waypoints = []
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

        # Interpret results. We may get a no data result if we were too greedy or too isolated.
        if not data or len(data) <= 0:

            # Ensure we don't do anything on no data
            print('No Data Returned')
            self.has_data = False
            return

        else:

            # Dump to disk for diagnostics
            if self.output_file:
                try:
                    f = open(self.output_file, "w")
                    f.write(data)
                    f.close()
                except:
                    error_message = "Unhandled error saving map data to file {0}\n".format(str(traceback.format_exc()))
                    print(error_message)


        osm_dict = xmltodict.parse(data)
        try:

            # Load Nodes
            for node in osm_dict['osm']['node']:

                # Extract ID and map the node
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
            for waypoint in osm_dict['osm']['way']:

                # Skip Invisible items
                if '@visible' in waypoint and waypoint['@visible'] == 'false':
                    continue

                path = MapPath(float(node['@lat']), float(node['@lon']))
                path.id = waypoint['@id']
                path.name = None

                # Get points from existing nodes
                try:
                    for node_id in waypoint['nd']:
                        if node_id == '@ref':
                            node = self.nodes[waypoint['nd']['@ref']]
                        elif '@ref' in node_id:
                            node = self.nodes[node_id['@ref']]
                        if node:
                            path.points.append((float(node['@lat']), float(node['@lon'])))
                except:
                    error_message = "Unhandled error handling points {0}\n".format(str(traceback.format_exc()))
                    print(error_message)

                # Get tags
                try:
                    if 'tag' in waypoint:
                        for tag in waypoint['tag']:
                            if tag == '@k':
                                self.process_tag(path, waypoint['tag'])
                                break
                            elif '@k' in tag:
                                self.process_tag(path, tag)
                            else:
                                for tag2 in tag:
                                    self.process_tag(path, tag2)
                except:
                    error_message = "Unhandled error handling tags {0}\n".format(str(traceback.format_exc()))
                    print(error_message)

                self.waypoints.append(path)

        except:
            error_message = "Unhandled error parsing map data {0}\n".format(str(traceback.format_exc()))
            print(error_message)

        self.has_data = len(self.nodes) > 0
        self.status_text = "Loaded {} Nodes of Map Data".format(len(self.nodes))

    def process_tag(self, entity, tag):

        tag_name = tag["@k"]
        tag_value = tag["@v"]

        # Name Field
        if tag_name == "name":
            entity.name = tag_value
            return True

        # Special amenities
        elif tag_name in (
                "amenity", "leisure", "man_made", "shop", "cuisine", "building", "power", "religion", "denomination",
                "website", "railway", "highway", "edu", "power", "railway", "oneway", "maxspeed", "ref", "layer",
                "natural", "area", "usage", "operator", "electrified", "gauge", "water", "sport", "access", "bridge",
                "abbr_name", "boundary", "admin_level", "ele", 'landuse', 'short_name', 'opening_hours', 'phone',
                "waterway", "clothes", "fee", "width", "border_type", "traffic_sign", "sidewalk", "barrier", "foot",
                "horse", "lanes", "bicycle", "tourism", "exit_to", "shortest_name", "hgv", "place", "footway",
                "cycleway", "name_1", "note", "aeroway", "proposed", "description", "brand", "expressway", "surface",
                "motorroad", "atm", "tower:type"):

            entity.tags.append((tag_name, tag_value))
            return True

        elif not str.startswith(str(tag_name), 'addr:') and not str.startswith(str(tag_name),
                                                                               'tiger:') and tag_name != 'source' and not str.startswith(
                str(tag_name), 'gnis:'):

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

        lines = []

        for way in self.waypoints:

            line = MapLine(way)

            tot_x = 0
            tot_y = 0

            for waypoint in way.points:

                lat = waypoint[1] - self.origin[1]
                lng = waypoint[0] - self.origin[0]

                wp = [
                    (lat * w_coef) + offset[0],
                    (lng * h_coef) + offset[1]
                ]

                if flip_y:
                    wp[1] *= -1
                    wp[1] += offset[1] * 2

                tot_x += wp[0]
                tot_y += wp[1]

                line.points.append(wp)

            # Calculate the center of the shape by looking at the average center of the points
            line.x = tot_x / max(1, float(len(line.points)))
            line.y = tot_y / max(1, float(len(line.points)))

            lines.append(line)

        return lines

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
            x = (rel_lat * w_coef) + offset[1]
            y = (rel_lng * h_coef)

            # We'll typically need to flip the longitude since 0, 0 is upper left corner on screens
            if flip_y:
                y *= -1

            y += offset[0]

            symbols.append(MapSymbol(y, x, location))

        return symbols

