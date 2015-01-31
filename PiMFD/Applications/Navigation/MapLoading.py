# coding=utf-8

from __future__ import print_function
from datetime import datetime
import traceback

from PiMFD.Applications.Navigation.MapEntities import MapPath
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
    annotations = None
    origin = None
    width = 0
    height = 0
    bounds = None
    last_data_received = None

    has_data = False
    status_text = "Loading Map Data..."

    output_file = None

    SIG_PLACES = 3
    GRID_SIZE = 0.001

    def __init__(self):
        super(Maps, self).__init__()

        self.locations = []
        self.waypoints = []
        self.annotations = []
        self.nodes = []

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

            self.last_data_received = datetime.now()

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

                location = MapSymbol(float(node['@lat']), float(node['@lon']))
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

                path = MapPath()
                path.id = waypoint['@id']
                path.name = None

                # Get points from existing nodes
                try:
                    for node_id in waypoint['nd']:
                        node = None
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

                # Don't perpetuate invalid objects
                if len(path.points) > 1:
                    path.calculate_lat_lng_from_points()
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

        elif str.startswith(str(tag_name), 'tiger:') or \
                        tag_name == 'source' or \
                str.startswith(str(tag_name), 'gnis:'):

            return False

        else:
            entity.tags.append((tag_name, tag_value))
            return True

    def fetch_by_coordinate(self, lat, lng, range):

        return self.fetch_area((
            float(lng) - range,
            float(lat) - range,
            float(lng) + range,
            float(lat) + range
        ))

    def get_dimension_coefficients(self, dimensions):

        width = dimensions[0]
        height = dimensions[1]

        w_coef = width / self.width / 2
        h_coef = height / self.height / 2

        return w_coef, h_coef

    def transpose(self, dimensions, offset):

        dim_coef = self.get_dimension_coefficients(dimensions)

        results = []
        results += self.transpose_ways(dim_coef, offset)
        results += self.transpose_locations(dim_coef, offset)

        return results

    def transpose_locations(self, dim_coef, offset):

        results = []

        for item in self.locations:

            # Determine relative lat / long to origin
            rel_lat = self.origin[0] - item.lat
            rel_lng = self.origin[1] - item.lng

            # Update the item's screen position
            item.x, item.y = self.translate_lat_lng_to_x_y(rel_lat, rel_lng, dim_coef, offset)

            results.append(item)

        return results

    def transpose_ways(self, dim_coef, offset):

        results = []

        for item in self.waypoints:

            # Determine relative lat / long to origin
            rel_lat, rel_lng = self.get_rel_lat_lng(item.lat, item.lng)

            line = MapLine(item)
            line.x, line.y = self.translate_lat_lng_to_x_y(rel_lat, rel_lng, dim_coef, offset)

            for waypoint in item.points:
                lat, lng = self.get_rel_lat_lng(waypoint[0], waypoint[1])

                screen = self.translate_lat_lng_to_x_y(lat, lng, dim_coef, offset)

                line.points.append(screen)

            results.append(line)

        return results

    def get_rel_lat_lng(self, lat, lng):

        # Determine relative lat / long to origin
        rel_lat = self.origin[0] - lat
        rel_lng = self.origin[1] - lng

        return rel_lat, rel_lng


    def translate_lat_lng_to_x_y(self, rel_lat, rel_lng, dim_coef, offset, multiplier=-1):

        # Scale the location accordingly
        y = (rel_lat * dim_coef[1]) + offset[1]
        x = (rel_lng * dim_coef[0] * multiplier) + offset[0]

        return x, y

    def gps_to_screen(self, lat, lng, dimensions, offset):

        # Determine relative lat / long to origin
        rel_lat, rel_lng = self.get_rel_lat_lng(lat, lng)

        dim_coef = self.get_dimension_coefficients(dimensions)
        return self.translate_lat_lng_to_x_y(rel_lat, rel_lng, dim_coef, offset)

    def set_screen_position(self, entity, dimensions, offset):
        entity.x, entity.y = self.gps_to_screen(entity.lat, entity.lng, dimensions, offset)
        return entity.x, entity.y

