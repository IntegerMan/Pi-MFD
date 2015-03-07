# coding=utf-8

"""
This file contains a data provider for navigation-related items.
"""
import pickle
import traceback

from PiMFD.Applications.Navigation.MapDataPage import MapDataPageProvider

from PiMFD.Applications.Navigation.TrafficDataPage import TrafficDataPageProvider
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.MapLocations import MapLocation
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic
from PiMFD.DataProvider import DataProvider
from PiMFD.UI.Widgets.DashboardWidget import TextDashboardWidget, DashboardStatus


__author__ = 'Matt Eland'


class NavigationDataProvider(DataProvider):
    """
    A DataProvider for the NavigationApplication.
    :param name: The name of the data provider
    """

    my_locations_file = 'mylocations.pickle'
    
    traffic_data_page = None
    

    def __init__(self, application, name="Navigation Data Provider"):
        super(NavigationDataProvider, self).__init__(name)

        self.application = application
        self.options = application.controller.options
        self.display = application.display
        
        self.traffic = MapTraffic(self.options)
        self.traffic_incidents = None
        self.traffic_widgets = None

        self.food_nodes = dict()
        self.camera_nodes = dict()
        self.gas_nodes = dict()
        self.shop_nodes = dict()
        self.leisure_nodes = dict()
        self.tourism_nodes = dict()
        
        self.gas_widget = None
        self.camera_widget = None
        self.food_widget = None

        self.traffic_data_provider = TrafficDataPageProvider(self)
        self.food_data_provider = MapDataPageProvider("Restaurant Data Provider", self.food_nodes)
        self.camera_data_provider = MapDataPageProvider("Camera Data Provider", self.camera_nodes)
        self.gas_data_provider = MapDataPageProvider("Gas Data Provider", self.gas_nodes)
        self.shop_data_provider = MapDataPageProvider("Shop Data Provider", self.shop_nodes)
        self.leisure_data_provider = MapDataPageProvider("Leisure Data Provider", self.leisure_nodes)
        self.tourism_data_provider = MapDataPageProvider("Tourism Data Provider", self.tourism_nodes)

        self.requested_data = False
        
        self.locations = None
        
        self.map = Maps(self)
        
        if self.options.profile:
            self.map.profile = True
            
        self.map.output_file = self.options.map_output_file

        self.map_context = MapContext(self.application, self.map, self)

        self.initialized = False

    def update(self, now):

        # Load locations if needed
        if not self.locations:
            self.load_locations()

        if not self.map.has_data and not self.requested_data:
            self.get_map_data()
            self.requested_data = True

        super(NavigationDataProvider, self).update(now)

    def register_shape(self, shape):

        if shape.has_tag_value("man_made", "surveillance"):
            self.camera_nodes[shape.id] = shape

        if shape.has_tag("shop"):
            self.shop_nodes[shape.id] = shape

        if shape.has_tag_value('amenity', 'restaurant') or shape.has_tag_value('amenity', 'fast_food') or shape.has_tag(
                'cuisine'):
            self.food_nodes[shape.id] = shape

        if shape.has_tag_value('amenity', 'fuel'):
            self.gas_nodes[shape.id] = shape

        if shape.has_tag('leisure'):
            self.leisure_nodes[shape.id] = shape
            
        if shape.has_tag('tourism'):
            self.tourism_nodes[shape.id] = shape

    def get_dashboard_widgets(self, display, page):

        widgets = []

        # Build out the widgets
        if self.traffic_incidents and not self.traffic_widgets:
            
            traffic_widgets = []

            for incident_key in self.traffic_incidents:
                
                incident = self.traffic_incidents[incident_key]
                
                if incident.description:
                    desc = incident.description[0:15]
                else:
                    desc = 'End: ' + incident.end_date

                widget = TextDashboardWidget(display, page, incident.name, desc)
                widget.data_context = incident

                widget.status = DashboardStatus.Caution
                if incident.severity:
                    sev = float(incident.severity) 
                    if sev <= 1:
                        widget.status = DashboardStatus.Passive
                    elif sev >= 4:
                        widget.status = DashboardStatus.Critical

                traffic_widgets.append(widget)
                widgets.append(widget)

            self.traffic_widgets = traffic_widgets
            
        # Create a Gas Widget
        if self.gas_data_provider and not self.gas_widget:
            self.gas_widget = TextDashboardWidget(display, page, 'Gas Stations', '')
            
        # Populate Gas Data
        if self.gas_data_provider and self.gas_widget:
            count = len(self.gas_data_provider.data_source)
            if count <= 0:
                self.gas_widget.value = 'No Gas Stations'
                self.gas_widget.status = DashboardStatus.Inactive
            elif count == 1:
                self.gas_widget.value = '1 Gas Station'
                self.gas_widget.status = DashboardStatus.Passive
                widgets.append(self.gas_widget)
            else:
                self.gas_widget.value = '{} Gas Stations'.format(count)
                self.gas_widget.status = DashboardStatus.Passive
                widgets.append(self.gas_widget)

        # Create a Cameras Widget
        if self.camera_data_provider and not self.camera_widget:
            self.camera_widget = TextDashboardWidget(display, page, 'Surveillance', '')

        # Populate Camera Data
        if self.camera_data_provider and self.camera_widget:
            count = len(self.camera_data_provider.data_source)
            if count <= 0:
                self.camera_widget.value = 'No Cameras'
                self.camera_widget.status = DashboardStatus.Inactive
            elif count == 1:
                self.camera_widget.value = '1 Camera'
                self.camera_widget.status = DashboardStatus.Passive
                widgets.append(self.camera_widget)
            else:
                self.camera_widget.value = '{} Cameras'.format(count)
                self.camera_widget.status = DashboardStatus.Passive
                widgets.append(self.camera_widget)

        return widgets

    def get_map_data(self, bounds=None, lat=None, lng=None):

        if bounds:
            self.map.fetch_area([bounds[0], bounds[1], bounds[2], bounds[3]])
        else:

            if not lat or not lng:
                if self.map.bounds:
                    lat = ((self.map.bounds[3] - self.map.bounds[1]) / 2.0) + self.map.bounds[1]
                    lng = ((self.map.bounds[2] - self.map.bounds[0]) / 2.0) + self.map.bounds[0]
                else:
                    lat = self.options.lat
                    lng = self.options.lng

            self.map.fetch_by_coordinate(lat, lng, self.map_context.map_zoom)

        self.initialized = True

    def next_map_mode(self):
        self.map_context.next_map_mode()

    def get_map_data_on_current_cursor_pos(self):

        # Build precursors that are needed for the map
        dim_coef = self.map.get_dimension_coefficients(
            (self.display.bounds.width, self.display.bounds.height))
        offset = self.display.get_content_center()

        # Figure out the Lat / Lng
        pos = self.map_context.cursor_pos
        lat, lng = self.map.translate_x_y_to_lat_lng(pos[0], pos[1], dim_coef=dim_coef, offset=offset)

        # Get the map data
        self.get_map_data(lat=lat, lng=lng)

        # Recenter the Cursor
        self.map_context.cursor_pos = self.display.get_content_center()

    def get_traffic(self, bounds):
        self.traffic.get_traffic(bounds, self)

    def handle_traffic_data(self, incidents):

        self.traffic_widgets = None
        if not self.traffic_incidents:
            self.traffic_incidents = dict()
            
        if incidents:
            for incident in incidents:
                self.traffic_incidents[incident.id] = incident

        self.map.handle_traffic_data(incidents)

    def add_location(self, location):
        self.locations.append(location)
        self.save_locations()

    def delete_location(self, location):
        self.locations.remove(location)
        self.save_locations()

    def save_locations(self):
        try:
            f = open(self.my_locations_file, "w")
            pickle.dump(self.locations, f)
            f.close()
        except:
            error_message = "Unhandled error saving my locations to file {0}\n".format(str(traceback.format_exc()))
            print(error_message)

    def load_locations(self):

        try:
            f = open(self.my_locations_file, "r")
            locations = pickle.load(f)
            f.close()

            if locations and len(locations) > 0:
                self.locations = locations

        except:
            error_message = "Unhandled error saving my locations to file {0}\n".format(str(traceback.format_exc()))
            print(error_message)

        # set some default values
        if not self.locations or len(self.locations) <= 0:
            default_location = MapLocation('Default Location', self.options.lat, self.options.lng)
            self.locations = [default_location]

    def get_data_pages(self):
        return [self.traffic_data_provider,
                self.food_data_provider,
                self.gas_data_provider,
                self.shop_data_provider,
                self.leisure_data_provider,
                self.tourism_data_provider,
                self.camera_data_provider]
        
            

