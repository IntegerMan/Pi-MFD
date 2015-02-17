# coding=utf-8
"""
The navigation application
"""

from PiMFD.Applications.Application import MFDApplication
from PiMFD.Applications.Navigation.MapContexts import MapContext
from PiMFD.Applications.Navigation.MapPages import MapPage, MapInfoPage
from PiMFD.Applications.Navigation.MapLoading import Maps
from PiMFD.Applications.Navigation.NavLayers.TrafficLoading import MapTraffic
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

    map = None
    map_context = None
    traffic = None
    btn_map = None
    btn_page = None

    def __init__(self, controller):
        super(NavigationApp, self).__init__(controller)

        self.map = Maps()
        self.map_context = MapContext(self, self.map)
        self.traffic = MapTraffic(controller.options)

        self.map.output_file = controller.options.map_output_file

        self.map_page = MapPage(controller, self)
        self.info_page = MapInfoPage(controller, self)
        self.weather_page = WeatherPage(controller, self, self.map_context)
        self.always_render_background = True

        self.pages = list([self.map_page])
        self.btn_map = MFDButton(None, selected=True)
        self.btn_page = MFDButton(self.map_context.get_page_mode_text())
        self.btn_info = MFDButton("INFO", enabled=False)
        self.btn_back = MFDButton("BACK")
        self.btn_detail_action = MFDButton("", enabled=False)

    def get_buttons(self):

        if self.active_page is self.map_page:

            self.btn_map.text = self.map_page.get_button_text()
            self.btn_page.text = self.map_context.get_page_mode_text()
            self.btn_info.enabled = self.map_context.cursor_context

            return [self.btn_map, self.btn_page, self.btn_info]

        else:
            return [self.btn_back, self.btn_detail_action]

    def select_page_by_index(self, index):

        if self.active_page is self.map_page:

            if index == 0:
                self.map_context.next_map_mode()
            elif index == 1:
                self.map_context.next_page_mode()
            elif index == 2:
                if self.map_context.cursor_context:
                    if not self.map_context.cursor_context.has_tag('weather'):
                        self.select_page(self.info_page)
                    else:
                        self.select_page(self.weather_page)

        elif self.active_page in (self.info_page, self.weather_page):

            if index == 0:
                self.select_page(self.map_page)
            elif index == 1:
                if self.active_page is self.info_page:
                    self.info_page.toggle_details()

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
        self.get_map_data()
        super(NavigationApp, self).handle_reselected()

    def handle_selected(self):
        """
        Handles the selected event for this application.
        """
        if not self.initialized:
            # TODO: This should be in another thread so the UI can keep rendering
            self.get_map_data()

    def get_map_data(self, bounds=None, lat=None, lng=None):

        if bounds:
            self.map.fetch_area([bounds[0], bounds[1], bounds[2], bounds[3]])
        else:

            if not lat or not lng:
                if self.map.bounds:
                    lat = ((self.map.bounds[3] - self.map.bounds[1]) / 2.0) + self.map.bounds[1]
                    lng = ((self.map.bounds[2] - self.map.bounds[0]) / 2.0) + self.map.bounds[0]
                else:
                    lat = self.controller.options.lat
                    lng = self.controller.options.lng

            self.map.fetch_by_coordinate(lat, lng, self.map_context.map_zoom)
            bounds = self.map.bounds

        self.map.annotations = self.traffic.get_traffic(bounds)

        # Find the first zip code
        zip = None
        for shape in self.map.shapes:
            zip = shape.get_tag_value('addr:postcode')
            if zip:
                break

                # Get Weather Data for our current location
        if zip:
            self.map.weather_data = self.controller.get_weather_data(zip)

        self.initialized = True

    def get_map_data_on_current_cursor_pos(self):

        # Build precursors that are needed for the map
        dim_coef = self.map.get_dimension_coefficients((self.display.res_x, self.display.res_y))
        offset = ((self.display.res_x / 2.0), (self.display.res_y / 2.0))

        # Figure out the Lat / Lng
        pos = self.map_context.cursor_pos
        lat, lng = self.map.translate_x_y_to_lat_lng(pos[0], pos[1], dim_coef=dim_coef, offset=offset)

        # Get the map data
        self.get_map_data(lat=lat, lng=lng)

        # Recenter the Cursor
        self.map_context.cursor_pos = (self.display.res_x / 2.0, self.display.res_y / 2.0)

    def zoom_in(self):

        if self.map_context.zoom_in():
            self.get_map_data_on_current_cursor_pos()


    def zoom_out(self):

        if self.map_context.zoom_out():
            self.get_map_data()

    def next_map_mode(self):
        self.map_context.next_map_mode()
