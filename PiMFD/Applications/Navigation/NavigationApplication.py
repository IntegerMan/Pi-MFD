# coding=utf-8
"""
The navigation application
"""
import pickle
import traceback

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.Navigation.MapPages import MapPage, MapInfoPage
from PiMFD.Applications.Navigation.MapLocations import MapLocationsPage, MapLocation, MapLocationAddPage
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic
from PiMFD.Applications.Navigation.NavigationDataProvider import NavigationDataProvider
from PiMFD.Applications.Scheduling.Weather.WeatherPages import WeatherPage
from PiMFD.UI.Button import MFDButton


__author__ = 'Matt Eland'


class NavigationApp(MFDApplication):
    """
    The scheduling application. Contains pages related to scheduling and coordinates web-service communication.
    :type controller: PiMFD.Controller.MFDController The controller.
    """
    map_page = None
    info_page = None
    weather_page = None

    initialized = False

    locations = []

    traffic = None
    btn_map = None
    btn_page = None
    my_locations_file = 'mylocations.pickle'

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.traffic = MapTraffic(controller.options)

        self.data_provider = NavigationDataProvider(self)

        self.map_page = MapPage(controller, self)
        self.info_page = MapInfoPage(controller, self)
        self.locations_page = MapLocationsPage(controller, self, self.data_provider.map_context, self.map_page)
        self.weather_page = WeatherPage(controller, self, self.data_provider.map_context)
        self.always_render_background = True

        # Load locations
        self.load_locations()
        
        self.pages = list([self.map_page])
        self.btn_map = MFDButton(None, selected=True)
        self.btn_page = MFDButton(self.data_provider.map_context.get_page_mode_text())
        self.btn_info = MFDButton("INFO", enabled=False)
        self.btn_goto = MFDButton("GOTO")
        self.btn_back = MFDButton("BACK")
        self.btn_detail_action = MFDButton("", enabled=False)
        self.btn_save = MFDButton("SAVE")

    def get_buttons(self):

        if self.active_page is self.map_page:

            self.btn_map.text = self.map_page.get_button_text()
            self.btn_page.text = self.data_provider.map_context.get_page_mode_text()
            self.btn_info.enabled = self.data_provider.map_context.cursor_context

            return [self.btn_map, self.btn_page, self.btn_info, self.btn_goto]

        else:

            # If the page supports it, use it to get buttons
            buttons = self.active_page.get_lower_buttons()
            if buttons and len(buttons) > 0:
                return buttons
            
            if self.active_page is self.weather_page:
                return [self.btn_back]
            
            return [self.btn_back, self.btn_detail_action, self.btn_save]

    def select_page_by_index(self, index):

        if self.active_page and self.active_page.handle_lower_button(index):
            return
        
        if self.active_page is self.map_page:

            if index == 0:
                self.data_provider.map_context.next_map_mode()
            elif index == 1:
                self.data_provider.map_context.next_page_mode()
            elif index == 2:
                if self.data_provider.map_context.cursor_context:
                    if not self.data_provider.map_context.cursor_context.has_tag('weather'):
                        self.select_page(self.info_page)
                    else:
                        self.select_page(self.weather_page)
            elif index == 3:
                self.select_page(self.locations_page)

        elif self.active_page in (self.info_page, self.weather_page):

            if index == 0:
                self.select_page(self.map_page)

            elif index == 1:
                if self.active_page is self.info_page:
                    self.info_page.toggle_details()

            elif index == 2:  # Save
                add_page = MapLocationAddPage(self.controller, self, self.map_page)
                add_page.set_values_from_context(self.data_provider.map_context.cursor_context)
                self.select_page(add_page)

    def get_default_page(self):
        """
        Gets the default page within the application.
        :return: the default page within the application.
        """
        return self.map_page

    def get_button_text(self):
        """
        Gets text for the button representing this page.
        :return: the button text for the application button.
        """
        return 'NAV'

    def page_reselected(self, page):
        """
        Handles the page reselected event for this application.
        :param page: The page that was reselected.
        """
        super(NavigationApp, self).page_reselected(page)

    def handle_reselected(self):
        self.data_provider.get_map_data()
        super(NavigationApp, self).handle_reselected()

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """
        if not self.data_provider.initialized:
            self.data_provider.get_map_data()
            
    def show_map(self, lat, lng):
        
        self.select_page(self.map_page)
        self.data_provider.get_map_data(lat=lat, lng=lng)

    def map_loaded(self, bounds):

        if bounds:
            self.traffic.get_traffic(bounds, self.data_provider.map)

        # Find the first zip code
        zipcode = None
        for shape in self.data_provider.map.shapes:
            zipcode = shape.get_tag_value('addr:postcode')
            if not zipcode:
                zipcode = shape.get_tag_value('tiger:zip_left')
            if not zipcode:
                zipcode = shape.get_tag_value('tiger:zip_right')
            if zipcode:
                break

        # Get Weather Data for our current location
        if zipcode:
            self.controller.get_weather_data(zipcode, consumer=self)

    def weather_received(self, location, weather):
        self.data_provider.map.weather_data = weather

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
            default_location = MapLocation('Default Location', self.controller.options.lat, self.controller.options.lng)
            self.locations = [default_location]

    def initialize(self):

        self.controller.register_data_provider(self.data_provider)

        super(NavigationApp, self).initialize()


    

