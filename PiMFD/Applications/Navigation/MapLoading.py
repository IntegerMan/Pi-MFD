# coding=utf-8

from __future__ import print_function
from datetime import datetime
from threading import Thread
import traceback

from PiMFD.Applications.Navigation.MapLines import MapLine
from PiMFD.Applications.Navigation.MapSymbols import MapSymbol


"""
Contains code related to rendering maps to the screen
"""
from math import floor

try:
    import requests
except ImportError:
    requests = None

try:
    import xmltodict
except ImportError:
    xmltodict = None

__author__ = 'Multiple'


class MapLoadThread(Thread):
    def __init__(self, map_loader, bounds, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(MapLoadThread, self).__init__(group, target, name, args, kwargs, verbose)

        self.map_loader = map_loader
        self.bounds = bounds

    def request_map_data(self, bounds, map):

        map.height = (bounds[2] - bounds[0]) / 2
        map.width = (bounds[3] - bounds[1]) / 2
        map.bounds = bounds
        map.origin = (
            bounds[1] + map.height,
            bounds[0] + map.width
        )
        url = "http://www.openstreetmap.org/api/0.6/map?bbox=%f,%f,%f,%f" % (
            bounds[0],
            bounds[1],
            bounds[2],
            bounds[3]
        )
        # Store Lat / Lng so invokers can have context of what center point is
        map.lat = bounds[0] + (bounds[2] - bounds[0]) / 2.0
        map.lng = bounds[1] + (bounds[3] - bounds[1]) / 2.0
        # Clear out old data
        map.has_data = False
        map.nodes = {}
        map.shapes = []
        print("Fetching maps " + url)

        # Get the data from the web.
        try:
            response = requests.get(url)
            data = response.text.encode('UTF-8')

        except:
            error_message = "Error Getting Map Data: {0}\n".format(str(traceback.format_exc()))
            print(error_message)
            map.status_text = error_message
            map.has_data = False
            data = None

        return data

    def run(self):
        super(MapLoadThread, self).run()

        self.map_loader.status_text = 'Requesting Data...'

        data = self.request_map_data(self.bounds, self.map_loader)

        self.map_loader.status_text = 'Interpreting Map...'

        # Interpret results. We may get a no data result if we were too greedy or too isolated.
        if not data or len(data) <= 0:
            # Ensure we don't do anything on no data
            self.map_loader.status_text = 'No Data Received'
            self.map_loader.has_data = False
            return

        self.map_loader.last_data_received = datetime.now()

        # Dump to disk for diagnostics
        if self.map_loader.application.controller.options.save_map_to_disk:
            self.map_loader.save_map_data(data)

        self.map_loader.load_map_from_data(data)


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
    weather_data = None

    SIG_PLACES = 3
    GRID_SIZE = 0.001
    lat = None
    lng = None

    def __init__(self, data_provider):
        super(Maps, self).__init__()

        self.shapes = []
        self.annotations = []
        self.nodes = []
        self.application = data_provider.application
        self.data_provider = data_provider

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
        self.status_text = "Loading Map Data..."

        # Spawn a new thread and launch it
        thread = MapLoadThread(self, bounds)
        thread.start()

    def save_map_data(self, data):

        if self.output_file and data:
            try:
                f = open(self.output_file, "w")
                f.write(data)
                f.close()
            except:
                error_message = "Unhandled error saving map data to file {0}\n".format(str(traceback.format_exc()))
                print(error_message)

    def process_tag(self, entity, tag):

        tag_name = tag["@k"]
        tag_value = tag["@v"]

        # Name Field
        if tag_name == "name":
            entity.name = tag_value
            return True

        elif str.startswith(str(tag_name), 'tiger:') or tag_name in ('source', 'created_by'):
            return False

        else:
            entity.add_tag(tag_name, tag_value)
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

    def translate_shapes(self, dimensions, offset):

        dim_coef = self.get_dimension_coefficients(dimensions)

        results = []

        for item in self.shapes:

            # Determine screen position based on relative GPS offset from our map origin
            rel_lat, rel_lng = self.get_rel_lat_lng(item.lat, item.lng)
            item.x, item.y = self.translate_lat_lng_to_x_y(rel_lat, rel_lng, dim_coef, offset)

            # For lines, we'll need to translate our GPS lines to screen-relative lines - keeping the old GPS values
            # for future iterations
            if item.points and len(item.points) > 1:
                screen_points = []
                for waypoint in item.points:
                    lat, lng = self.get_rel_lat_lng(waypoint[0], waypoint[1])
                    screen = self.translate_lat_lng_to_x_y(lat, lng, dim_coef, offset)

                    screen_points.append(screen)

                item.screen_points = screen_points

            # The item is good, so return it to whatever is rendering things
            results.append(item)

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

    def translate_x_y_to_rel_lat_lng(self, x, y, dim_coef, offset, multiplier=-1):

        if dim_coef[0] == 0 or dim_coef[1] == 0:
            return 0, 0

        rel_lat = (y - offset[1]) / dim_coef[1]
        rel_lng = (x - offset[0]) / multiplier / dim_coef[0]

        return rel_lat, rel_lng

    def translate_rel_to_absolute_gps(self, rel_lat, rel_lng):
        # Determine relative lat / long to origin
        lat = self.origin[0] - rel_lat
        lng = self.origin[1] - rel_lng

        return lat, lng

    def translate_x_y_to_lat_lng(self, x, y, dim_coef, offset, multiplier=-1):

        rel_lat, rel_lng = self.translate_x_y_to_rel_lat_lng(x, y, dim_coef, offset, multiplier)

        return self.translate_rel_to_absolute_gps(rel_lat, rel_lng)

    def gps_to_screen(self, lat, lng, dimensions, offset):

        # Determine relative lat / long to origin
        rel_lat, rel_lng = self.get_rel_lat_lng(lat, lng)

        dim_coef = self.get_dimension_coefficients(dimensions)
        return self.translate_lat_lng_to_x_y(rel_lat, rel_lng, dim_coef, offset)

    def set_screen_position(self, entity, dimensions, offset):
        entity.x, entity.y = self.gps_to_screen(entity.lat, entity.lng, dimensions, offset)
        return entity.x, entity.y

    def handle_traffic_data(self, incidents):
        self.annotations = incidents

    def load_map_from_data(self, data):

        if 'service unavailable' in data.lower():
            print(data)
            self.has_data = False
            self.status_text = 'Map Server Offline'
            return

        if not xmltodict:
            self.status_text = "xmltodict not available".upper()
            return

        try:
            osm_dict = xmltodict.parse(data)

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
                    self.shapes.append(location)

            # Load Waypoints
            for waypoint in osm_dict['osm']['way']:

                # Skip Invisible items
                if '@visible' in waypoint and waypoint['@visible'] == 'false':
                    continue

                path = MapLine()
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
                    self.shapes.append(path)

        except:
            error_message = "Unhandled error parsing map data {0}\n".format(str(traceback.format_exc()))
            print(error_message)

        self.has_data = self.nodes and len(self.nodes) > 0
        self.status_text = "Loaded {} Nodes of Map Data".format(len(self.nodes))

        self.application.map_loaded(self.bounds)